---
Organization: 'Project Astragal'
documentID: IR-2013-Dual-EC-DRBG.md
title: 'Incident Report - 2013 Dual_EC_DRBG'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2013 Dual_EC_DRBG
================================================================================

SUMMARY
A NIST-standardized PRNG whose security depends on the provenance of two constants. Whoever
generated those constants can predict all output from roughly 32 bytes of observed output.

THE ALGORITHM
Dual_EC operates on an elliptic curve with two published points P and Q. With internal state s:

        s_{i+1} = x( s_i · P )
        r_i     = lsb_240( x( s_i · Q ) )        // 30 bytes emitted as output

WHY IT FAILS
Suppose an attacker knows d such that

        d · Q = P

Then, from output r_i, the attacker recovers the next state:

    1. r_i is the low 30 bytes of x(s_i · Q). Guess the missing 2 bytes - 2^16 candidates.
    2. For each candidate x-coordinate r, test whether a point R exists with x(R) = r.
       Roughly half of candidates are valid x-coordinates on the curve.
    3. For each valid R, compute
              x( d · R ) = x( d · s_i · Q ) = x( s_i · (d·Q) ) = x( s_i · P ) = s_{i+1}
    4. Confirm the candidate by generating the next output and matching it against the two bytes
       that were guessed.

In practice this yields one to three candidate states. The work is 2^16-ish, not cryptographic. From
s_{i+1} the attacker has the entire future output stream.

The trapdoor is generated in the natural direction: pick d, set Q = d^-1 · P, publish Q. The
standard neither requires nor provides any verifiable derivation of the constants.

Note the shape of this defect. The generator is not broken. The code is not buggy. The output passes
every statistical test. The vulnerability is entirely in the provenance of two numbers, and no
amount of testing the implementation can detect it.

TIMELINE OF THE ARGUMENT
Shumow and Ferguson presented the trapdoor structure at the CRYPTO 2007 rump session. Documents
reported in September 2013 were read as confirming deliberate insertion. NIST withdrew Dual_EC from
SP 800-90A in Rev. 1. Reuters reported a $10 million contract under which Dual_EC became the default
in RSA BSAFE; RSA disputed the characterization.

REFERENCES
- Bernstein, Lange, Niederhagen, "Dual EC: A Standardized Back Door":
  https://eprint.iacr.org/2015/767.pdf
- Green, "The Many Flaws of Dual_EC_DRBG":
  https://blog.cryptographyengineering.com/2013/09/18/the-many-flaws-of-dualecdrbg/

