---
Organization: 'Project Astragal'
documentID: IR-2012-Mining-Ps-and-Qs.md
title: 'Incident Report - 2012 Mining Your Ps and Qs'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2012 Mining Your Ps and Qs
Heninger, Durumeric, Wustrow, Halderman - USENIX Security 2012
================================================================================

SUMMARY
Not a single code defect but a systemic one: headless embedded devices generate their host keys on
first boot, before the kernel entropy pool has been seeded. Identical devices in identical states
produce identical or related keys.

MECHANISM
On Linux, /dev/urandom will return output whether or not the pool has been seeded. It does not block
and it signals nothing. A device with no keyboard, no mouse, no user, and often no disk has almost
no entropy sources available at first boot; interrupt timing on a freshly-booted embedded system is
close to deterministic.

Devices of the same model, booting for the first time, executing the same firmware in the same
sequence, therefore drew from near-identical pool state.

TWO FAILURE PATTERNS
Repeated keys. Two devices produce the same keypair outright. Either can impersonate the other, and
anyone holding one device holds the other's key.

Shared factors. Two devices diverge slightly - typically because entropy arrived between the
generation of the first prime and the second. Both moduli then share exactly one prime:

        N1 = p * q1
        N2 = p * q2

        gcd(N1, N2) = p          -->   q1 = N1/p,  q2 = N2/p

Both private keys fall out immediately. Critically, this scales: a batched GCD across the whole
collected corpus is efficient, so the attack cost is not per-key. An attacker needs no access to
either device - only their public keys, which are published by definition.

FINDINGS
- 5.57% of TLS hosts and 9.60% of SSH hosts shared keys with at least one other host.
- RSA private keys recovered for 0.50% of TLS hosts and 0.03% of SSH hosts via shared factors.
- DSA private keys recovered for 1.03% of SSH hosts, via repeated signature nonces arising from the
  same entropy shortage.

REFERENCES
- Paper and materials: https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/heninger
- https://factorable.net/

