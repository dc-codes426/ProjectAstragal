---
Organization: 'Project Astragal'
documentID: IR-2023-Milk-Sad.md
title: 'Incident Report - 2023 Milk Sad'
version: 0.01
version_date: 2026-09-28
state: draft
---

================================================================================
Incident Report - 2023 Milk Sad
CVE-2023-39910
================================================================================

SUMMARY
The "bx seed" command, used to generate wallet entropy, drew from a Mersenne Twister seeded with 32
bits of the system clock. Named for the first two words of the mnemonic produced by seed value 0.

THE CODE
    [VERBATIM] src/utility.cpp

        data_chunk new_seed(size_t bit_length)
        {
            size_t fill_seed_size = bit_length / byte_bits;
            data_chunk seed(fill_seed_size);
            pseudo_random_fill(seed);
            return seed;
        }

    [VERBATIM] pseudo_random.cpp

        const auto get_clock_seed = []() NOEXCEPT
        {
            const auto now = high_resolution_clock::now();
            return static_cast<uint32_t>(now.time_since_epoch().count());
        };

        if (twister.get() == nullptr)
        {
            twister.reset(new std::mt19937(get_clock_seed()));
        }

WHY IT FAILS
Note the shape of new_seed(): it takes a bit_length parameter and sizes its output buffer
accordingly. A caller requesting 256 bits receives 256 bits. The function is honest about its output
width and silent about its input width.

The entropy actually reaching that buffer is bounded by the twister's seed, and get_clock_seed()
casts the clock value to uint32_t. Requesting more output does not request more entropy - it
stretches the same 32 bits further. There is no interface through which a caller could discover this,
and no error path that fires.

RESULTING KEYSPACE
2^32 - roughly 4.3 billion seeds - regardless of the requested length. Narrowing by approximate
wallet creation time reduces it further. The full space is enumerable on consumer hardware in days,
and each candidate is checkable against the public chain without contacting the victim.

Note also the naming. "pseudo_random" is an accurate name for the function. It was called from a
seed-generation path anyway.

SCOPE
Libbitcoin Explorer 3.0.0 through 3.6.0. Because a BIP-39 mnemonic derived this way is used across
chains, exposure was not limited to Bitcoin.

REFERENCES
- Full technical disclosure: https://milksad.info/disclosure.html
- CVE-2023-39910

