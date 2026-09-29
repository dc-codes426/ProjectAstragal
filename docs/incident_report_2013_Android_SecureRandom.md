---
Organization: 'Project Astragal'
documentID: IR-2013-Android-SecureRandom.md
title: 'Incident Report - 2013 Android SecureRandom'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2013 Android SecureRandom
CVE-2013-7372
================================================================================

SUMMARY
Android's Java Cryptography Architecture could return SecureRandom output from an improperly
initialized PRNG, silently and without error. Bitcoin wallets on affected devices generated weak
keys and, worse, reused ECDSA nonces.

MECHANISM
Android's SecureRandom, derived from Apache Harmony, could fail to seed the underlying OpenSSL PRNG.
Any call into SecureRandom, KeyGenerator, KeyPairGenerator, KeyAgreement or Signature could therefore
return output that was not cryptographically strong. No exception was raised and no return value
indicated the condition; the output was well-formed.

Google's remediation guidance was for applications to seed the PRNG explicitly:

    [RECONSTRUCTED] the pattern recommended in the Android Developers Blog post

        SecureRandom sr = new SecureRandom();
        byte[] seed = readFromUrandom(32);   // /dev/urandom
        sr.setSeed(seed);

That is, applications were told to supply the entropy the platform was supposed to have supplied.

THE SECOND FAILURE: REPEATED ECDSA NONCES
Weak key generation was the lesser problem. Affected wallets also produced ECDSA signatures with
colliding r values, meaning the same nonce k was used for two different messages. This is
algebraically fatal and requires no search at all.

For signatures (r, s1) over message hash z1 and (r, s2) over z2, sharing nonce k, with curve order n:

        s1 = k^-1 (z1 + r*d)  mod n
        s2 = k^-1 (z2 + r*d)  mod n

Subtracting eliminates d:

        k = (z1 - z2) * (s1 - s2)^-1   mod n

and then d falls out directly:

        d = (s1*k - z1) * r^-1         mod n

A repeated r is visible to anyone reading the chain. Two signatures are sufficient. The private key
is recovered by arithmetic, not by brute force.

SCOPE
Android prior to 4.4. Affected wallet applications included Bitcoin Wallet, the blockchain.info
Android app, BitcoinSpinner and Mycelium.

REFERENCES
- Android Developers Blog, "Some SecureRandom Thoughts":
  https://android-developers.googleblog.com/2013/08/some-securerandom-thoughts.html
- CVE-2013-7372: https://nvd.nist.gov/vuln/detail/CVE-2013-7372

