---
Organization: 'Project Astragal'
documentID: IR-2008-Debian-OpenSSL-PRNG.md
title: 'Incident Report - 2008 Debian OpenSSL Predictable PRNG'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2008 Debian OpenSSL Predictable PRNG
CVE-2008-0166 / DSA-1571-1
================================================================================

SUMMARY
A patch intended to silence Valgrind warnings removed the call that mixed caller-supplied entropy
into OpenSSL's PRNG pool. The pool retained its entropy *estimate* but stopped receiving entropy.

THE CODE
Valgrind flagged reads of uninitialized memory at two sites in crypto/rand/md_rand.c. Kurt Roeckx
identified them in Debian bug #363516 as:

    [VERBATIM] crypto/rand/md_rand.c:247, inside ssleay_rand_add()

        MD_Update(&m,buf,j);

    [VERBATIM] crypto/rand/md_rand.c:467, inside ssleay_rand_bytes()

        #ifndef PURIFY
            MD_Update(&m,buf,j); /* purify complains */
        #endif

Both were removed.

WHY IT FAILS
The two call sites look identical and are not.

The site at line 467 is inside ssleay_rand_bytes(), where OpenSSL mixes the contents of the output
buffer back into the pool before overwriting it. That buffer genuinely may hold uninitialized stack
memory. Upstream had already guarded this one with #ifndef PURIFY, acknowledging it as a
belt-and-braces measure. Removing it is defensible.

The site at line 247 is inside ssleay_rand_add(). That is the function behind the public RAND_add()
API - the single path by which every real entropy source enters the pool. When a caller passes bytes
from /dev/urandom, a PID, a timestamp, or any other source, `buf` is that data. Valgrind flagged it
only because some callers deliberately pass uninitialized memory as an *additional* source, and
Valgrind cannot distinguish an intentional read of uninitialized memory from an accidental one.

Removing line 247 therefore did not remove a marginal entropy source. It removed the mixing step
itself. RAND_add() continued to increment the pool's entropy counter while contributing nothing to
the pool's state.

Tim Hudson of OpenSSL, in the same bug thread, distinguished the two cases explicitly - the first
change was safer, the second "most certainly was not."

RESULTING KEYSPACE
The only remaining input reaching the generator was the process ID. With the Linux default PID
maximum of 32,768, the generator had roughly 15 bits of entropy. For a fixed architecture, key type
and key size, the full set of derivable keys is on the order of 32,767 candidates and can be
pre-computed and distributed - which it promptly was.

SCOPE
Debian's openssl package from 0.9.8c-1, and every Debian-derived distribution. Affects SSH host and
user keys, TLS certificates and keys, OpenVPN keys, and DNSSEC keys generated on affected systems.
Keys generated elsewhere and merely used on affected systems were unaffected.

REFERENCES
- Debian bug #363516 (the originating thread): https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=363516
- DSA-1571-1: https://www.debian.org/security/2008/dsa-1571
- Cox, "Lessons from the Debian/OpenSSL Fiasco": https://research.swtch.com/openssl

