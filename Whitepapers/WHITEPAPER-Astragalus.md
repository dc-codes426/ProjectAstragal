---
organization: 'Project Astragal'
documentID: WHITEPAPER-Astragalus.md
title: 'Project Astragalus - a Verifiable seed generation architecture'
version: 0.01
version_date: 2026-09-28
state: draft
---

# Project Astragal: A Verifiable Seed Generation Architecture

*Whitepaper — draft*

## 1 Purpose and scope

Here we define the invariant properties required for a seed used in cryptographic applications, and establish why they are necessary. We then describe the requirements of a seed generation ceremony to satisfy those invariants by construction. Finally, we demonstrate that physical, non-digital methods of entropy generation are the only way to meet those requirements with certainty. This document specifies the general ceremony method that follows from these arguments.

This method covers one event: the generation of a secret. It ends when the ceremony has produced a single written copy of the mnemonic and destroyed every other copy. It does not cover how the secret is stored, backed up, distributed, inherited, or used afterwards. Those are lifecycle concerns, and they are excluded deliberately, not overlooked. Generation is the only point at which I1 is fixed and the only point at which I3 can be verified. Everything after it rests on trust decisions that differ between users and change over time. A lifecycle standard may build on this method. This method makes no claims about one.

### 1.1 Scope and terminology

The word "seed" is used loosely in this field and precisely in BIP-39, and the difference is exactly where Astragal stops.

```text
sources  ->  entropy  ->  mnemonic  ||  seed  ->  master key  ->  addresses
|--------- Astragal ---------|     |---------- out of scope ---------|
```

Astragal's scope runs from the independent sources the user operates, through the entropy their combination produces, to the mnemonic that encodes it, written down once as the ceremony's output. What BIP-39 itself calls the seed - the 64-byte output of PBKDF2-HMAC-SHA512 over the mnemonic - lies outside it, as do BIP-32 master key derivation, derivation paths, and address encoding. No tier implements anything to the right of that line; the next paragraph says why. Storage, backup, and use of the mnemonic after the ceremony are also outside it (section 1).

Where this document says "seed generation" without qualification, the referent is the mnemonic and the entropy behind it. The boundary is not a matter of taste. Everything inside it is hand-computable; PBKDF2's 2048 iterations are not, by any arrangement of paper. The claim a user can establish for themselves is therefore one sentence long - my mnemonic encodes my trials, and no one source of them could have chosen it - and the architecture should not imply a longer one.

A note on the name. An astragalus is the talus - the ankle bone of a hoofed animal - and it is what people threw for several thousand years before anyone thought to cut a cube. It is the ancestor of the die. Two of its properties are the ones this architecture is trying to recover. The throw happened in front of everyone with a stake in the result, and the bone was plainly not fair, so nobody could pretend that question had been settled somewhere the participants were unable to see. A sealed noise source inverts both.

### 1.2 Process Approach

This method adopts a process approach, whereby the ceremony is a process with physical entropy input and an encoded secret output, with the properties named in the section below. The ceremony process is further split into three sub-processes:

- **A) Entropy Generation** - generating a random 256-bit bitwise number. The process input is abstract - physical entropy. The process output is specific - one 256-bit random bitwise number. This is performed at least twice, independently, to generate two or more 256-bit random bitwise numbers.
- **B) Encoding** - the two or more random numbers as an output of independent process A executions are mixed by bitwise XOR. Finally, the resulting bitwise number is encoded in a mnemonic using BIP-39. The input is two or more bitwise numbers. The output is an encoded BIP-39 mnemonic.
- **C) Output** - the verified mnemonic is written down once, and every other copy made during the ceremony is destroyed. The input is one BIP-39 mnemonic. The output is a single written copy of it.

XOR is the mixing algorithm because of one property: if at least one input is uniformly random and independent of the others, the output is uniformly random, whatever the other inputs are. A source that is biased, broken, or malicious cannot reduce the entropy of the result, provided it cannot see the other sources before its own output is committed. A source that can see the others can cancel them: given source A, a malicious source B = target XOR A fixes the secret at the target. This is why the sources must be independent in order as well as in kind. XOR is also computable by hand, bit by bit, so the user can perform the mix themselves.

## 2 The invariants

| ID | Invariant | Definition |
|----|-----------|------------|
| I1 | Unpredictable | Given knowledge of the protocol, materials, and methods used, no adversary is able to recreate the secret. This property requires the secret to carry a stated amount of entropy. |
| I2 | Accessible by the user | The user may access the secret for its intended use. |
| I3 | Not accessible by any other party | No one but the user possesses the secret. |

This document provides the minimum ceremony requirements to establish these three invariant properties of the resulting secret at the point of generation. Preserving I2 and I3 after the ceremony is a lifecycle concern (section 1).

### 2.1 Additional Secret Properties

In addition to the invariants that define any secret, we define a secret to hold 256-bits, encoded via a BIP-39 mnemonic. The reason for defining these is not secret invariant. A "secret" can hold any amount of entropy and be encoded in any format. However, standards are important, and the provenance of the mathematical properties used is important. Therefore, this method scopes the secret to specifically 256-bits encoded by BIP-39, by construction.

The ceremony outputs the secret as a single written copy of the mnemonic. How the secret is stored and used afterwards is outside this method.

## 3 Verification over Validation

**Verification** is the confirmation, through objective evidence, of a certain property of an object. Third-party audits are not verification. Verification of a process is not verification of an output of that process.

**Validation** is an extensive evaluation of a process to ensure that it always produces the intended output, by construction.

Verification is superior to validation in terms of assurance. The field of software generally defaults to validation over verification. Programmers have good reason for doing so - verification of an object in software is often prohibitively expensive. However, cryptographic seed generation is one process where verification of outputs are not prohibitively expensive compared to validation. A properly constructed seed generation ceremony allows the user to independently verify that, when the ceremony ends, they and only they hold the secret.

The unpredictability invariant is the one case where verification of the property is not possible. In this case, we opt for verification of process, and redundancy. A properly constructed ceremony includes two sources of entropy, each contributing the target amount of entropy. The ceremony should also allow the user to witness that the entropy was generated correctly, even if the user can't verify the output itself. The ceremony should also include independent user verification that the multiple entropy sources were combined and encoded properly. The mixing and encoding must be verified in order to assuredly satisfy the unpredictability invariant.

## 4 Ceremony Requirements

- **R1** — Use redundant, independent\* entropy sources. Each source should contribute the full target amount of entropy.
- **R2** — Encode the resulting entropy according to a defined algorithm and format.
- **R3** — Verify that the result of the encoding is correct, given the random number inputs to the encoding process. The verification must be performed by the user, and must be independent\* of the original encoding. The verification must cover I2 and I3.
- **R4** — The user must monitor the process throughout.

\* Must be independent in kind and order.

## 5 Physical Non-digital Entropy

The method we propose utilizes rudimentary technology for both ceremony processes. One random number may come from HRNG. But at least one random number must come from a non-digital source. This includes dice, cards, and coins, each reasonably controlled to assure proper execution and non-bias. Additionally, the encoding or the encoding verification must be performed by pen-and-paper.

The reason for requiring non-digital methods may seem like it is to prevent bugs from threatening the secret invariants. However, protection from hardware or software bugs is handled by independent encoding and entropy sources. The reason for non-digital methods is more specific. It is the most justifiable way to assure that the independence requirement is satisfied. Seemingly independent sources of entropy may share the same fatal flaws in hardware or software. Seemingly independent devices for encoding the entropy may share code package dependencies, where a fatal flaw would impact the encoding and the verification. As we have seen, labeling the product as "open-source" does not assure this level of security to the user. Any ceremony claiming the method described in this paper must include independent user verification that alternative entropy sources and encoding methods are truly independent, all the way throughout the stack. The ceremony may require the user to have advanced technical knowledge in software and hardware, and procedurally walk them through the code review, spec review. It must also include attestation that the device used in the ceremony is what it claims, and runs software it claims to run. Or, the ceremony can have the user throw dice.

### 5.1 The Encoding Device

The encoding is executed twice: once by hand and once by a device. The device is the one element of the ceremony, apart from the user and their paper, that holds the whole secret. I3 therefore depends on the device being offline and amnesiac.

The user cannot verify either property by examining the device. Both are claims about its internals, and anything the user could do to inspect them without destroying it, such as reading its memory or running a self-test, runs on the silicon in question. Open-source designs, audits, vendor signatures, and certification move this trust to someone else; they do not remove it. The corpus includes devices certified to FIPS 140-2 and CC EAL5+ (ROCA). Even an open silicon design can be altered at fabrication, below the level that optical inspection can detect.

The method therefore does not verify the device's internals. It verifies every path by which the secret could leave the device:

- **Output:** the device's results are compared with the hand execution. A faulty or malicious device cannot alter the result without detection.
- **Transmission:** the device is operated only inside an enclosure that prevents it from transmitting, which the user tests, and it is never powered outside that enclosure while it may hold ceremony material.
- **Retention:** every component capable of retaining state is destroyed at the end of the ceremony, in view of the user.

With these paths closed, what the chip contains is irrelevant to I1 and I3. Attestation of hardware, firmware, and software is not required.

Destruction is the only way to verify amnesia. A device that has held the secret and survives must be trusted not to retain it, and must then be kept offline for the life of the secret, which no test covers. Keeping it unpowered does not help: it is then a second copy of the secret, and the ceremony's output is defined as exactly one. Destruction replaces a property the user cannot verify with an event the user witnesses.

Destruction need not cover the whole device, only the components capable of retaining state. A device can be designed so that these form a small replaceable module, and the rest of the device is reused.

A device that holds the secret after the ceremony, such as a wallet, cannot serve as the encoding device. The separation is deliberate. When one device generates, verifies, and stores a secret, the user cannot check any of those functions independently of the others. The corpus shows the result: in COLDCARD, the same firmware produced the entropy, mixed in the user's dice, and held the seed, and the user had no way to confirm what their dice had contributed.

A device used only as an entropy source is held to a different standard. It should be offline and amnesiac by design, but the user need not verify either property, and the device need not be destroyed. It never holds the whole secret, and the method's standard is no single point of failure: if the device fails in any way, including by leaking its output, the result is the failure of one source, which the redundant sources protect against (R1).

A device that never holds the whole secret would not need to be destroyed. Multi-party computation could, in principle, perform the encoding across several devices, each holding only part of the secret. This method does not adopt it. It would satisfy the invariants only if each device's share meets the stated security level against that device, and the devices are independent in kind and in order.

The ceremony's claims end at the output record. Entering the secret into any device afterwards is a new trust decision, outside this method: I3 cannot be verified after generation. The destruction requirement ensures that the ceremony itself adds no trusted device, so whatever the user trusts afterwards is the only trust involved. Trust begins where verification ends.

## 6 Threat Model

The threat model is malicious nation-states, independent adversarial hackers, and compromised supply chains. As long as independence is maintained throughout the stack of the entropy source and the verifications, no single malicious party can compromise the secret during the ceremony.

The threat model ends where the ceremony ends. Threats to the output record and to the secret after the ceremony, including theft, loss, coercion, and the devices the secret is later entered into, are lifecycle concerns outside this method (section 1).

> **Note:** The encoding device is contained and destroyed rather than trusted (section 5.1). What remains trusted is the enclosure's shielding, which the user tests, and the security of the ceremony environment.

## 7 Summary

We describe the Astragalus Method for Bitcoin seed generation.

---

## Editor's notes

Needs citation:

- derivation of the secret invariant properties.
- derivation of the ceremony requirements. Independence. Provenance.
- verification over validation
