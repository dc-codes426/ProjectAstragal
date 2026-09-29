---
organization: 'Project Astragal'
documentID: RESEARCH-What-Makes-a-Secret.md
title: 'What Makes a Secret'
version: 0.01
version_date: 2026-09-28
state: draft
---

# What Makes a Secret

*Research — draft*

Companion papers: [RESEARCH-Verification-over-Validation](RESEARCH-Verification-over-Validation.md) (how a user
can establish these properties) and [WHITEPAPER-Astragalus](../Whitepapers/WHITEPAPER-Astragalus.md) (a ceremony that does so).


## Abstract

Cryptographic secrets have been compromised again and again, in certified hardware, in widely
used open-source libraries, and in standards themselves, usually without the underlying
mathematics being broken at all. Here we propose the invariant properties that must hold
throughout the lifetime of any cryptographic secret: it must be unpredictable, accessible to its
owner, and inaccessible to everyone else. We test these properties against a corpus of ten
publicly documented generation failures, 2006-2025. For each case we identify the secret, where
in the pipeline the defect sat, which property failed, and how much entropy survived compared
with the nominal amount. Every exploit in the corpus is a
failure of unpredictability or of exclusivity, and every one began as a failure of
unpredictability at some generation event. The three properties are sufficient, but only once
tightened: unpredictability must hold against every party including the designer, entropy must
be measured at the narrowest point in the pipeline, and secrets derived from a root secret carry
the same properties as the root.


## 1 Introduction

COLDCARD is a hardware wallet built for people who take self-custody seriously. Its firmware
contained a guard written to prevent exactly one mistake: building without the hardware random
number generator.

```c
#ifndef MICROPY_HW_ENABLE_RNG
#  error "get a HW TRNG plz"
#endif
```

The board configuration defined that macro as zero. `#ifndef` asks whether a macro is defined, not
what it is defined as, so the guard passed and every build compiled cleanly. The cryptographic
library fell back to a deterministic software generator, seeded from the chip's unique ID, a
timer, and the clock. The hardware generator sat on the same chip, working, and unused. Seeds
meant to carry 128 or 256 bits of entropy came from a space an attacker could search: under
2^40.7 candidates on older models, given the chip's ID, and at most 2^32 on later ones.

Nothing in the cryptography failed. The elliptic curve was as hard as ever. SHA-256, BIP-39, and
BIP-32 did exactly what they specify. Yet for anyone holding an affected seed, the effect was the
same as if the mathematics had been broken: an adversary could compute their keys.

That is the pattern of this corpus. Almost none of its failures solved a hard problem. ROCA came
closest, and even it worked only because key generation had already given away most of the
entropy. Cryptography promises that finding a key takes more work than any adversary can do, but
the promise has a condition: the key must be chosen from a space as large as its width. Every
case here broke the condition, not the promise. The mathematics held, and the protection failed
anyway.

A secret is only as strong as the weakest step between its entropy and its use. The failures in
the corpus were not obscure. Several were in certified hardware, several were in open-source code
read by many people, and every one produced output of the correct width that passed ordinary
tests. In each case the nominal strength of the secret - 256 bits, FIPS certified, open source -
differed from its actual strength, and nobody with a stake in the secret could see the
difference.

This paper asks a narrow question: what properties must a secret have, and which of them failed in
each real exploit?


## 2 Definitions

### 2.1 Secret

A secret is a value whose worth depends on who does and does not know it. The scope here is key
material, seeds, and nonces.

### 2.2 Entropy and security level

The entropy of a secret is not the width of its output. A 256-bit value drawn from 2^32
possibilities has 32 bits of entropy, however it is formatted. Entropy here means min-entropy,
H = -log2(p), where p is the probability of the adversary's single best guess. It is the measure
that matters to an attacker who tries the likeliest candidates first.

Entropy is always relative to an adversary's knowledge. A value that is unpredictable to one
party may be fully determined for another who holds a constant, a timestamp, or part of the
value itself.

The security level is the number of candidates an adversary must test to recover the secret,
stated in bits. This paper does not fix one. The amount of entropy "unpredictable" requires is a
parameter, and any process that generates a secret must state it. A standard example is a 256-bit
secret whose storage is split so that any single share leaves 124 bits unknown to its holder.

The security level can be lower than the secret's total entropy. An adversary who holds part of
the secret, such as one share in a distributed storage scheme, faces only the entropy that
remains unknown to them. The stated security level must hold against every such adversary.

### 2.3 Adversary

The adversary includes outside attackers, implementers, standards bodies, and anyone in the
supply chain. The adversary is assumed to know the protocol, the code, any constants, the
approximate time of generation, and all public data, including every public key and, for
cryptocurrency, the full chain.

### 2.4 The invariants

| ID | Invariant | Definition |
|----|-----------|------------|
| I1 | Unpredictable | No party other than the user can reproduce the secret with work below the stated security level. |
| I2 | Accessible to the user | The user can recover and use the secret when needed. |
| I3 | Inaccessible to others | No other party holds the secret, or anything that determines it. |

I2 is stated for completeness. It is the property the owner notices immediately when it fails,
and no case in the corpus involves it.

### 2.5 Exploit

An exploit is any event in which the secret becomes recoverable by a party that I3 excludes.

### 2.6 How I1 and I3 relate

I1 is about derivation: no one else can compute the secret. I3 is about possession: no one else
holds it. A failure of I1 implies a failure of I3, because any party able to predict the secret
can hold it whenever it chooses. The converse does not hold. A secret can be perfectly
unpredictable and still leak.

A case can therefore break both, and the useful question is where the failure started. If I1
failed, the secret was compromised at the moment it was generated. If only I3 failed, the secret
was sound when generated and was exposed later.

### 2.7 When the invariants hold, and when they can be checked

I1 is fixed at generation. Nothing that happens later can make a secret more or less
predictable. I3 must hold for the secret's whole life.

The two differ in when they can be checked. I1 cannot be verified from the output at all, even
at generation: a predictable value and an unpredictable one look the same. It can only be
established through the process that produced it. I3 can be verified only at generation, when
the user can account for every copy. After that, unless the user has kept the secret on their
person for its entire life, they cannot confirm that no one else has it.

Whether the invariants hold is a property of the secret. Whether anyone can verify that they
hold is a property of the process, and is outside this paper.


## 3 Method

Cases were selected on three criteria: a public technical disclosure exists, the defect can be
identified in code or design, and the entropy loss can be quantified.

Each case is analysed with the same frame:

1. What was the secret?
2. Where in the pipeline was the defect?
   source -> conditioning/mixing -> construction -> derivation/use
3. Which invariant failed, and which failed first?
4. What was the nominal entropy, and what was the effective entropy?

Code-level detail, and the provenance of every snippet ([VERBATIM], [DECOMPILED], or
[RECONSTRUCTED]), is in the incident reports in
[Research/Incident_Reports](../Research/Incident_Reports/README.md), one per case.


## 4 The Corpus

### 4.1 Debian OpenSSL (CVE-2008-0166)

Report: [IR-2008-Debian-OpenSSL-PRNG](../Research/Incident_Reports/incident_report_2008_Debian_OpenSSL.md)

Secret: SSH, TLS, OpenVPN, and DNSSEC keys. A patch meant to silence Valgrind removed the call that
mixed caller-supplied entropy into OpenSSL's pool. The pool kept counting entropy it no longer
received. The only remaining input was the process ID, about 15 bits. Stage: mixing. I1 failed at
generation.

### 4.2 Mining Your Ps and Qs (2012)

Report: [IR-2012-Mining-Ps-and-Qs](../Research/Incident_Reports/incident_report_2012_Mining_Ps_and_Qs.md)

Secret: RSA and DSA keys on headless network devices. Devices generated keys at first boot, before
the kernel pool held any entropy, so identical devices produced identical or related keys. Repeated
keys gave one device's owner another's key outright. Moduli sharing a single prime were factored by
a batch GCD across the whole corpus of public keys: 0.50% of TLS hosts and 0.03% of SSH hosts.
Repeated DSA nonces exposed 1.03% of SSH hosts' keys. Stage: source. I1 failed at generation.

### 4.3 Android SecureRandom (CVE-2013-7372)

Report: [IR-2013-Android-SecureRandom](../Research/Incident_Reports/incident_report_2013_Android_SecureRandom.md)

Secret: Bitcoin private keys and the ECDSA nonces used to sign with them. Android's SecureRandom
could return output from an unseeded PRNG without any error. Wallets signed two transactions with
the same nonce, and the private key followed by arithmetic from two public signatures. Stage:
source, then use. I1 failed for the nonce, which broke I3 for the key.

### 4.4 Dual_EC_DRBG

Report: [IR-2013-Dual-EC-DRBG](../Research/Incident_Reports/incident_report_2013_Dual_EC_DRBG.md)

Secret: all output of a NIST-standardised generator. Whoever knows the scalar d relating the two
published points P and Q can recover the generator's internal state from about 30 bytes of output,
with roughly 2^16 work. The code has no bug and the output passes every statistical test. The
weakness is entirely in where two constants came from. Stage: design. I1 failed against exactly one
party.

### 4.5 Juniper ScreenOS (CVE-2015-7756)

Report: [IR-2015-Juniper-ScreenOS](../Research/Incident_Reports/incident_report_2015_Juniper_ScreenOS.md)

Secret: VPN session keys. ScreenOS was designed to pass Dual_EC output through an X9.31 generator,
which would have hidden it. A global variable reused as a loop counter meant the X9.31 stage never
ran, so raw Dual_EC output reached the IKE nonce. An unknown party later replaced Q, and updated the
self-test to match. Stage: mixing and design. I1 failed against the holder of the substituted Q.

### 4.6 ROCA (CVE-2017-15361)

Report: [IR-2017-ROCA-Infineon-RSALib](../Research/Incident_Reports/incident_report_2017_ROCA.md)

Secret: RSA keys in smart cards, TPMs, and national ID cards. Infineon's library built primes in a
fixed algebraic form to speed up generation. For 512-bit RSA this left about 99 bits of entropy per
prime instead of 256, and the structure let anyone fingerprint an affected key from its public
modulus alone. The devices were certified to FIPS 140-2 and CC EAL5+. Stage: construction. I1
failed at generation.

### 4.7 Randstorm

Report: [IR-2023-Randstorm](../Research/Incident_Reports/incident_report_2023_Randstorm.md)

Secret: Bitcoin keys generated in browsers, roughly 2011-2015. BitcoinJS drew randomness from JSBN's
SecureRandom, which filled its pool from Math.random() and the clock. One pool served every key
generated on the page. Effective entropy varies by browser and version. Stage: source. I1 failed at
generation.

### 4.8 Profanity

Report: [IR-2022-Profanity](../Research/Incident_Reports/incident_report_2022_Profanity.md)

Secret: Ethereum private keys from a vanity address generator. A 256-bit key was derived from a
single 32-bit seed, and the search stepped from it reversibly, so any address the tool produced led
back to its seed. Stage: source and use. I1 failed at generation: 32 bits of entropy in a 256-bit
key.

### 4.9 Milk Sad (CVE-2023-39910)

Report: [IR-2023-Milk-Sad](../Research/Incident_Reports/incident_report_2023_Milk_Sad.md)

Secret: BIP-39 wallet entropy from Libbitcoin Explorer's `bx seed`. A Mersenne Twister was seeded
with 32 bits of the system clock. The function returned as many bits as the caller asked for, and
never more than 32 bits of entropy. Stage: source. I1 failed at generation.

### 4.10 COLDCARD

Report: [IR-2026-Coldcard-Exploit](../Research/Incident_Reports/incident_report_2026_Coldcard.md)

Secret: seeds and every other value drawn from the device's random number generator. A
preprocessor guard tested whether a macro was defined, not whether it was enabled. The macro was
defined as zero, so the build fell back silently to a deterministic software generator while the
hardware RNG sat unused. On later models, good hardware entropy was reduced to 32 bits by the
interface that consumed it. Block's analysis puts affected keyspaces below 2^40.7 on older models
with a known chip ID, and at most 2^32 on later ones. Stage: source and mixing. I1 failed at
generation.

### 4.11 Summary

| Case | Stage | Failed first | Nominal | Effective |
|---|---|---|---|---|
| Debian | mixing | I1 | full pool | ~15 bits |
| Ps and Qs | source | I1 | 1024+ bits | none (repeated keys); factored (shared primes) |
| Android | source, use | I1 (nonce), then I3 (key) | 256 bits | none (repeated nonce) |
| Dual_EC | design | I1, against the holder of d | 256 bits | ~16 bits for the holder of d |
| Juniper | mixing, design | I1, against the holder of Q | X9.31 cascade | raw Dual_EC |
| ROCA | construction | I1 | 256 bits per prime | ~99 bits per prime (RSA-512) |
| Randstorm | source | I1 | 256 bits | varies by browser |
| Profanity | source, use | I1 | 256 bits | 32 bits |
| Milk Sad | source | I1 | 128-256 bits | 32 bits |
| COLDCARD | source, mixing | I1 | 128-256 bits | below 2^40.7 / 2^32 |


## 5 Analysis

### 5.1 I1 failures

Every case failed I1. The mechanisms fall into four groups:

- **The source never had entropy.** Ps and Qs, Android, Randstorm.
- **Entropy existed but was discarded or narrowed.** Debian, Milk Sad, Profanity, COLDCARD.
- **The space of outputs was structured.** ROCA.
- **Entropy existed, but not against every party.** Dual_EC, Juniper.

### 5.2 I3 failures

Every I1 failure is also an I3 failure (2.6), so those are not counted again. Three patterns are
worth naming:

- **Repeated keys.** In Ps and Qs, another device held the secret outright. The failure began as
  I1, and ended with another party in possession.
- **Trapdoors.** In Dual_EC and Juniper, I1 failed for exactly one party, which put I3 in that
  party's hands from the moment of generation.
- **Leakage through a derived secret.** In Android and in the DSA results of Ps and Qs, the
  long-term key may have been sound when generated. It leaked because a nonce failed I1. Seen from
  the key, this is an I3 failure during use. Seen from the nonce, which is a secret generated
  separately, it is an I1 failure at generation.

Every I3 failure in the corpus started as an I1 failure at some generation event. That follows
partly from how the corpus was chosen, since every case is a generation defect, and is not a
claim about secrets in general.

### 5.3 I2

No case involves I2.


## 6 Refining the Invariants

### 6.1 I1 must hold against every party

That includes the designer, the implementer, and whoever supplied the constants. Dual_EC's output
was unpredictable to everyone except one party. "Unpredictable" without "to whom" is not a property
at all.

### 6.2 Entropy is measured at the narrowest point

Milk Sad, Profanity, and COLDCARD all emitted full-width output from a 32-bit bottleneck, and
Debian's pool reported entropy it did not have. Output width and internal entropy estimates say
nothing. The secret has the entropy of the narrowest step it passed through.

### 6.3 Derived secrets carry the same invariants

Nonces, masks, and temporary keys are secrets generated in their own right, and a failure of any of
them can expose the root. Android shows this, and so does the list of functions downstream of
COLDCARD's generator.

### 6.4 Uniqueness is not a separate invariant

Ps and Qs looks like a failure of uniqueness, but two parties sharing a key is already a failure of
I1 and I3. No fourth property is needed.

### 6.5 There is no I4

Once refined, I1-I3 describe every exploit in the corpus. "The user can establish that the
invariants hold" is a natural candidate for a fourth, but it is a property of the process, not of
the secret (2.7).


## 7 Limitations

- Survivorship. Only disclosed failures appear here. An undetected trapdoor, by construction,
  does not.
- Some code in the incident reports is [RECONSTRUCTED] or [DECOMPILED], not original source.
- Cryptocurrency cases are over-represented. The chain is public, so failures there are both
  exploitable and visible.
- Effective-entropy figures come from each source's own threat assumptions, such as a known chip
  ID or a known creation window.


## 8 Conclusion

A secret must be unpredictable to every party but its owner, accessible to its owner, and held by
no one else. In the corpus, the second never failed, and the other two failed together: every
exploit began when a secret, root or derived, was generated with less entropy, against some
party, than its width implied. Unpredictability is settled at generation, and exclusivity must
hold for the secret's whole life but can only be checked at its start. Generation is therefore
where a secret is made or lost. How a user can confirm, for their own secret, that it was made
correctly is the subject of the companion paper.


## Appendix A Case x invariant matrix

(To be completed from section 4.)

## Appendix B Effective-entropy calculations

(Per case, with assumptions stated. To be completed from the primary sources.)

## References

1. Debian bug #363516: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=363516
2. DSA-1571-1: https://www.debian.org/security/2008/dsa-1571
3. Cox, "Lessons from the Debian/OpenSSL Fiasco": https://research.swtch.com/openssl
4. Heninger, Durumeric, Wustrow, Halderman, "Mining Your Ps and Qs", USENIX Security 2012:
   https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/heninger
5. https://factorable.net/
6. Android Developers Blog, "Some SecureRandom Thoughts":
   https://android-developers.googleblog.com/2013/08/some-securerandom-thoughts.html
7. CVE-2013-7372: https://nvd.nist.gov/vuln/detail/CVE-2013-7372
8. Bernstein, Lange, Niederhagen, "Dual EC: A Standardized Back Door":
   https://eprint.iacr.org/2015/767.pdf
9. Green, "The Many Flaws of Dual_EC_DRBG":
   https://blog.cryptographyengineering.com/2013/09/18/the-many-flaws-of-dualecdrbg/
10. Checkoway et al., "A Systematic Analysis of the Juniper Dual EC Incident", CCS 2016:
    https://eprint.iacr.org/2016/376.pdf
11. Green, "On the Juniper backdoor":
    https://blog.cryptographyengineering.com/2015/12/22/on-juniper-backdoor/
12. Nemec et al., "The Return of Coppersmith's Attack", CCS 2017:
    https://crocs.fi.muni.cz/public/papers/rsa_ccs17
13. Estonian Information System Authority, "ROCA Vulnerability and eID: Lessons Learned":
    https://www.ria.ee/sites/default/files/documents/2022-11/Roca-vulnerability-and-eID-lessons-learned-2018.pdf
14. Unciphered, Randstorm disclosure:
    https://www.unciphered.com/disclosure-of-vulnerable-bitcoin-wallet-library-2/
15. 1inch Network, Profanity disclosure:
    https://1inch.com/blog/post/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool
16. Amber Group, "Exploiting the Profanity Flaw":
    https://medium.com/amber-group/exploiting-the-profanity-flaw-e986576de7ab
17. SlowMist, "The Real Cause of the Wintermute Exploit":
    https://slowmist.medium.com/the-real-cause-of-the-wintermute-exploit-10da7e404b3b
18. Milk Sad technical disclosure: https://milksad.info/disclosure.html
19. Block Engineering, "Predictable RNG Fallback and 32-Bit Reseed in COLDCARD Firmware":
    https://engineering.block.xyz/blog/predictable-rng-fallback-and-32-bit-reseed-in-coldcard-firmware
20. Coinkite security advisory: https://blog.coinkite.com/coldcard-mk3-seed-generation-warning/
21. Wizardsardine, "Coldcard: the technical autopsy of an entropy failure":
    https://wizardsardine.com/blog/coldcard-vuln-deep-dive/
