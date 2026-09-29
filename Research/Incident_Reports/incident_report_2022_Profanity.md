---
Organization: 'Project Astragal'
documentID: IR-2022-Profanity.md
title: 'Incident Report - 2022 Profanity'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2022 Profanity
================================================================================

SUMMARY
The tool seeded a 256-bit private key search from a 32-bit value, then iterated deterministically
and reversibly from it.

THE CODE
    [RECONSTRUCTED] from published analyses (1inch, Amber Group, SlowMist); the archived repository
    is the authoritative source.

        cl_ulong4 seed;
        std::random_device rd;
        std::mt19937_64 eng(rd());                       // <-- rd() yields 32 bits
        std::uniform_int_distribution<cl_ulong> distr;
        for (size_t i = 0; i < 4; ++i)
            seed.s[i] = distr(eng);                      // 4 x 64 bits, all determined by 32

WHY IT FAILS
std::random_device::operator() returns an unsigned int - 32 bits. std::mt19937_64 is a deterministic
function of its seed. Constructing the engine from a single rd() call therefore admits at most 2^32
distinct engine states, and every one of the four 64-bit words in the 256-bit seed is a function of
that one 32-bit value.

The private key is 256 bits wide and drawn from a 2^32 space - about 4.3 billion candidates.

The second half of the problem is that Profanity's GPU search iterates from the initial key by
repeated addition of a known constant, in order to enumerate candidate addresses cheaply. That
iteration is reversible. Given *any* address the tool produced, an attacker can walk backwards to
the initial key of that run, then search the 32-bit seed space to confirm it. Exposure is not limited
to the first key generated - every address the tool ever emitted leaks its own run's starting point.

SCOPE
Any Ethereum address generated with Profanity, regardless of vanity prefix length. The author
archived the repository following disclosure.

REFERENCES
- 1inch Network disclosure:
  https://1inch.com/blog/post/a-vulnerability-disclosed-in-profanity-an-ethereum-vanity-address-tool
- Amber Group, "Exploiting the Profanity Flaw":
  https://medium.com/amber-group/exploiting-the-profanity-flaw-e986576de7ab
- SlowMist, "The Real Cause of the Wintermute Exploit":
  https://slowmist.medium.com/the-real-cause-of-the-wintermute-exploit-10da7e404b3b

