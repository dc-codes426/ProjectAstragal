---
Organization: 'Project Astragal'
documentID: IR-2023-Randstorm.md
title: 'Incident Report - 2023 Randstorm'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2023 Randstorm
================================================================================

SUMMARY
BitcoinJS obtained randomness from the JSBN library's SecureRandom(), which filled its entropy pool
from Math.random() - not a CSPRNG in the browsers of that era, and in some versions carrying very
little state.

THE CODE
    [VERBATIM] jsbn rng.js, pool initialization

        // Mix in a 32-bit integer into the pool
        function rng_seed_int(x) {
          rng_pool[rng_pptr++] ^= x & 255;
          rng_pool[rng_pptr++] ^= (x >> 8) & 255;
          rng_pool[rng_pptr++] ^= (x >> 16) & 255;
          rng_pool[rng_pptr++] ^= (x >> 24) & 255;
          if(rng_pptr >= rng_psize) rng_pptr -= rng_psize;
        }

        // Mix in the current time (w/milliseconds) into the pool
        function rng_seed_time() {
          rng_seed_int(new Date().getTime());
        }

        // Initialize the pool with junk if needed.
        if(rng_pool == null) {
          rng_pool = new Array();
          rng_pptr = 0;
          var t;
          if(navigator.appName == "Netscape" && navigator.appVersion < "5" && window.crypto) {
            // Extract entropy (256 bits) from NS4 RNG if available
            var z = window.crypto.random(32);
            for(t = 0; t < z.length; ++t)
              rng_pool[rng_pptr++] = z.charCodeAt(t) & 255;
          }
          while(rng_pptr < rng_psize) {  // extract some randomness from Math.random()
            t = Math.floor(65536 * Math.random());
            rng_pool[rng_pptr++] = t >>> 8;
            rng_pool[rng_pptr++] = t & 255;
          }
          rng_pptr = 0;
          rng_seed_time();
        }

Note: current copies of rng.js carry an additional leading branch using
window.crypto.getRandomValues(). That branch was added later. In the affected era the Netscape-4
branch above was the only hardware-backed path, and it was dead code in every browser then in use -
so the Math.random() loop was the sole source.

WHY IT FAILS
Three compounding problems.

The comment "extract some randomness from Math.random()" is doing all the work, and Math.random() in
that era was typically an xorshift or LCG variant with small state, not seeded from any secure
source, and in several browser versions seeded from the clock.

rng_seed_time() adds `new Date().getTime()` - millisecond wall-clock. To an attacker who knows
approximately when a wallet was created, this is worth a handful of bits, not 32.

The pool is initialized once per page load, at script evaluation time, and the resulting SecureRandom
instance was reused for every key generated on that page. Multiple keys from one session are
therefore not independent.

SCOPE
Wallets generated in browsers roughly 2011-2015, via BitcoinJS directly or as a dependency in web
wallet and paper-wallet generators. Degree of weakness varies by browser and version, so affected
keys are not uniformly recoverable. BitcoinJS discontinued JSBN use in March 2014.

REFERENCES
- Unciphered disclosure: https://www.unciphered.com/disclosure-of-vulnerable-bitcoin-wallet-library-2/

