---
Organization: 'Project Astragal'
documentID: IR-2015-Juniper-ScreenOS.md
title: 'Incident Report - 2015 Juniper ScreenOS'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2015 Juniper ScreenOS
CVE-2015-7756 (VPN decryption); CVE-2015-7755 (hardcoded admin password, unrelated to RNG)
================================================================================

SUMMARY
ScreenOS used Dual_EC, but was designed to post-process its output through an ANSI X9.31 generator,
which would have neutralized the trapdoor. A variable-reuse bug caused the X9.31 stage to be skipped
entirely, so raw Dual_EC output was emitted. Years later, an unidentified party changed the Q
constant.

THE CODE
Decompiled by Checkoway et al. from ScreenOS 6.2.0r1. Identifiers were assigned by the researchers;
the binary contains no symbol names.

    [DECOMPILED] Listing 1, Checkoway et al., CCS 2016

        void prng_reseed(void) {
            blocks_generated_since_reseed = 0;
            if (dualec_generate(prng_temporary, 32) != 32)
                error_handler("FIPS ERROR: PRNG failure, unable to reseed\n", 11);
            memcpy(prng_seed, prng_temporary, 8);
            prng_output_index = 8;
            memcpy(prng_key, &prng_temporary[prng_output_index], 24);
            prng_output_index = 32;
        }

        void prng_generate(void) {
            int time[2];
            time[0] = 0;
            time[1] = get_cycles();
            prng_output_index = 0;
            ++blocks_generated_since_reseed;
            if (!one_stage_rng())
                prng_reseed();
            for (; prng_output_index <= 0x1F; prng_output_index += 8) {
                // FIPS checks removed for clarity
                x9_31_generate_block(time, prng_seed, prng_key, prng_block);
                // FIPS checks removed for clarity
                memcpy(&prng_temporary[prng_output_index], prng_block, 8);
            }
        }

WHY IT FAILS
Two coupled issues.

First, prng_reseed() and prng_generate() share the static buffer prng_temporary.

Second - and this is the defect - prng_output_index is a global, and it is used for two unrelated
purposes. prng_reseed() uses it as a scratch offset while carving the 32-byte Dual EC output into an
8-byte seed and a 24-byte key, leaving it set to 32 on exit. prng_generate() uses the same global as
the induction variable of the loop that runs X9.31.

So the sequence in prng_generate() is:

        prng_output_index = 0;              // set to 0
        if (!one_stage_rng())
            prng_reseed();                  // ... which leaves it at 32
        for (; prng_output_index <= 0x1F; prng_output_index += 8) {   // 32 <= 31 is false

The loop body never executes. prng_temporary still holds the raw Dual EC output written by
prng_reseed(), and that is what the caller receives. The X9.31 cascade - the thing that made Dual EC
safe in this design - is skipped on every call that reseeds.

In the default configuration one_stage_rng() always returns true, so reseeding happens on every
call, so the X9.31 stage is *never* reached.

Checkoway et al. note that had prng_reseed() used a local variable instead of the global, sharing
prng_temporary would have been harmless. They further note the loop variable in prng_generate()
changed from a local to the global between the last ScreenOS 6.1.0 release and the first 6.2.0.

WHY THIS WAS EXPLOITABLE
Dual EC emits 30 of the 32 bytes of the point, and exploitation degrades exponentially with each
missing byte. From version 6.2, ScreenOS built its 32-byte IKE nonce from two successive Dual EC
invocations - 30 bytes from the first, 2 from the second. As the researchers observe, this is close
to ideal for the attacker: the first 30 bytes narrow the state, and the remaining 2 confirm it,
typically leaving one to three candidates.

The attack chain: recover PRNG state from the phase-1 IKE nonce, predict the Diffie-Hellman private
key, compute the shared secret, decrypt.

THE 2012 CHANGE
Juniper had substituted its own Q for the NIST constant in 2008. In ScreenOS 6.2.0r15 and 6.3.0r12,
Q was changed again. Analysis of the modified binaries found no other alteration in the affected
path - the change was the constant itself, plus the corresponding update to the Dual EC Known Answer
Test so that self-tests would still pass.

REFERENCES
- Checkoway et al., "A Systematic Analysis of the Juniper Dual EC Incident", CCS 2016:
  https://eprint.iacr.org/2016/376.pdf
- Green, "On the Juniper backdoor":
  https://blog.cryptographyengineering.com/2015/12/22/on-juniper-backdoor/

