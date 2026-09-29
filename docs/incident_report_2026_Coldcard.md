---
Organization: 'Project Astragal'
documentID: IR-2026-Coldcard-Exploit.md
title: 'Incident Report - 2026 Coldcard Exploit'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2026 Coldcard Exploit
================================================================================

SUMMARY
A preprocessor guard tested whether a macro was *defined* rather than whether it was *enabled*. The
board configuration defined it as zero. The guard passed, and the cryptographic library bound to
MicroPython's deterministic software fallback instead of the STM32 hardware RNG - which was present
and working the whole time.

THE CODE

    [VERBATIM] ngu/random.c - the guard intended to prevent exactly this

        #ifndef MICROPY_HW_ENABLE_RNG
        #  error "get a HW TRNG plz"
        #endif

    [VERBATIM] stm32/COLDCARD_MK4/mpconfigboard.h (and the equivalent in COLDCARD/ and COLDCARD_Q1/)

        #define MICROPY_HW_ENABLE_RNG       (0)

WHY IT FAILS
#ifndef tests existence, not value. The macro is defined - to zero - so #ifndef is false, the #error
does not fire, and compilation proceeds silently down the fallback path.

The guard was not missing. It was written, it was correct in intent, its error message names the
exact failure it was meant to prevent, and it was structurally incapable of firing. Every build
emitted a clean compile.

Elsewhere in the same tree the macro is consumed with #if, which does test the value. The two idioms
are one character apart and behave identically for every value except zero.

THE FALLBACK GENERATOR
    [VERBATIM] ports/stm32/rng.c - MicroPython's Yasmarang, as seeded on this platform

        STATIC uint32_t pyb_rng_yasmarang(void) {
            static bool seeded = false;
            static uint32_t pad = 0, n = 0, d = 0;
            static uint8_t dat = 0;

            if (!seeded) {
                seeded = true;
                rtc_init_finalise();
                pad = *(uint32_t *)MP_HAL_UNIQUE_ID_ADDRESS ^ SysTick->VAL;
                n = RTC->TR;
                d = RTC->SSR;
            }
            // deterministic state transformation follows
        }

Seed material, in full:
- MP_HAL_UNIQUE_ID_ADDRESS - the MCU's unique identifier. Fixed per chip, readable, not secret.
- SysTick->VAL - a counter with on the order of 80,000 possible values on Mk2/Mk3, 120,000 on later
  devices (~2^16.3 and ~2^16.9 respectively).
- RTC->TR and RTC->SSR - wall-clock time and sub-second register, correlated with boot timing and
  potentially static across a cold boot.

After initialization it is a pure state machine. It collects no further entropy, ever.

THE PARTIAL RESEED (Mk4/Q/Mk5 only)
    [VERBATIM] shared/mk4.py

        def rng_seeding():
            import callgate, ngu, ustruct

            a = callgate.read_rng(1)        # SE1
            b = callgate.read_rng(2)        # SE2

            n = ngu.hash.sha256d(a+b)
            n, = ustruct.unpack('I', n[0:4])

            ngu.random.reseed(n)

Note the last two lines. A SHA256d digest is 32 bytes. `ustruct.unpack('I', n[0:4])` takes four of
them. Those 32 bits replace a single word of Yasmarang state.

Good entropy was available - the secure elements are hardware RNGs and were queried successfully.
The interface for consuming it was 32 bits wide, so 28 of the 32 bytes were discarded.

RESULTING KEYSPACE
Per Block's analysis:
- Mk2/Mk3 (no reseed), with known UID: under 2^40.7 candidates. If the RTC is stable during a cold
  boot, potentially as low as 2^16.3 - SysTick alone.
- Mk4/Q/Mk5 with successful reseed: at most 2^32 distinguishable streams, ~2^31 average enumeration.
- Treating all timer fields as independent gives a loose ceiling around 2^73.27, which Block states
  is explicitly *not* 73-bit cryptographic security, because the fields are correlated.

Coinkite's advisory describes the outcome as roughly 72 bits rather than the intended 128.

SCOPE
Mk2/Mk3 firmware v4.0.1-v4.1.9; Mk4/Mk5 before 5.6.0; Q before 1.5.0Q. Mk1 and pre-v4 firmware used
the STM32 hardware RNG directly and were outside the regression.

Affected functionality is everything downstream of ngu.random: new and ephemeral seeds, random
paper-wallet and secp256k1 private keys, Seed XOR split masks, device cloning and USB encryption ECDH
keys, Key Teleport temporary keys and passwords, Web2FA TOTP shared secrets and per-request nonces,
Secure Notes password generation, and HSM local-code material.

THE TWO DICE PATHS
COLDCARD shipped two dice workflows with materially different exposure.

"Dice Rolls" - the default and recommended path. Firmware combines 32 bytes from the generator, 32
fresh bytes from SE1 and 8 from SE2, applies double SHA-256, then mixes in the required user input.
Per Coinkite's advisory, seeds created with at least 50 fair independent rolls received at least 128
bits from the dice alone and were unaffected.

The user cannot verify this. The device's contribution is not displayed, so there is no relationship
between the entered rolls and the resulting seed that can be checked from outside the device. That
the mixing was implemented correctly - in the same firmware where the entropy source was not - was
not a property any user could confirm.

"Dice Rolls Only" - documented as an advanced workflow. The SHA-256 accumulator starts from an empty
string and takes only the rolls:

        seed = BIP39( sha256( ASCII string of rolls ) )

50 rolls for 12 words, 99 for 24. Verifiable externally:

        $ echo -n 123456 | sha256sum

with Coldcard's own caveat that funded-wallet rolls should never be entered into a computer.

REFERENCES
- Block Engineering, "Predictable RNG Fallback and 32-Bit Reseed in COLDCARD Firmware":
  https://engineering.block.xyz/blog/predictable-rng-fallback-and-32-bit-reseed-in-coldcard-firmware
- Coinkite security advisory: https://blog.coinkite.com/coldcard-mk3-seed-generation-warning/
- Wizardsardine, "Coldcard: the technical autopsy of an entropy failure":
  https://wizardsardine.com/blog/coldcard-vuln-deep-dive/
- Coldcard, "Verifying Dice Roll Math": https://coldcard.com/docs/verifying-dice-roll-math/

