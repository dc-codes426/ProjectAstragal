---
organization: 'Project Astragal'
documentID: RESEARCH-Verification-over-Validation.md
title: 'Verification over Validation'
version: 0.01
version_date: 2026-09-28
state: draft
---

# Verification over Validation

*Research — outline draft*

Companion papers: [RESEARCH-What-Makes-a-Secret](RESEARCH-What-Makes-a-Secret.md) (the "secret
paper": the properties a secret must have) and
[WHITEPAPER-Astragalus](../Whitepapers/WHITEPAPER-Astragalus.md) (the "method whitepaper": a ceremony
that establishes them). This paper asks how a user can know those properties hold for their own
secret.


## Working Notes

### Draft requirements

The starting hypothesis is the following requirements for a secret generation ceremony:

- **R1** — Use redundant, independent\* entropy sources. Each source should contribute the full
  target amount of entropy.
- **R2** — Encode the resulting entropy according to a defined algorithm and format.
- **R3** — Verify that the result of the encoding is correct, given the random number inputs to
  the encoding process. The verification must be performed by the user, and must be independent\*
  of the orginial encoding. The verification must cover I2 and I3.
- **R4** — The user must monitor the process throughout.

\* Must be independent in kind and order.

This paper can flesh out:

- what independent means, throughout the stack
- what verification is. Audits are not verification. Code review are not verification.
  Verification of process is not verification of object properties.
- What it means for the user to monitor throughout.

### Working thesis

- Start from the invariants (secret paper), a strict definition of verification, and the corpus.
- From those, derive the requirements a ceremony must meet for the user to establish I1-I3 for
  their own secret.
- R1-R4 above are the starting hypothesis. Section 5 tests each against the principles, and
  requirements are revised, added, or removed as the derivation dictates.
- Expected shape of the result: I1 cannot be verified, but it can be reduced to properties that
  can be (independent sources, witnessed generation, a verified mix). I3 can be verified only at
  generation. Only verification by the user counts.


## Abstract

- The problem: every broken generator in the corpus had passed some form of validation.
- The distinction: verification examines a specific object or execution. Validation argues about a
  process in general.
- The method: derive ceremony requirements from first principles, and test each one against the
  corpus.
- The result: a requirement set (section 5.6) that names no technology. Choosing the means that
  meet it is left to the method whitepaper.


## 1 Introduction

- The secret paper establishes I1-I3 as properties of the secret. Whether a user can establish
  them is a separate question, about process.
- Software generally relies on validation, because verifying each output is usually too expensive.
- Seed generation is an exception:
  - there is one output, made once;
  - it is small;
  - the mixing and encoding are cheap enough to run more than once, independently.
- Contributions:
  1. Definitions of verification, independence, and monitoring precise enough to derive
     requirements from. The independence definition must be complete enough that the method can
     say "independent" without further qualification.
  2. An assurance record for the corpus.
  3. The derivation of each ceremony requirement.


## 2 First Principles

### 2.1 Taken from the secret paper

- I1 unpredictable, I2 accessible to the user, I3 inaccessible to others.
- I1 failing implies I3 failing.
- I1 is fixed at generation. I3 must hold for the secret's lifetime but can be verified only at
  generation. I2 is trivial.

### 2.2 The process model

Everything that follows needs one vocabulary. The ceremony is divided into processes, and each
process has objects as its inputs and outputs.

- **Process:** a transformation with a defined boundary, defined inputs, and defined outputs.
  Examples: a source (its input is physical entropy and its output is a random number); mixing;
  encoding; one execution of the encoding's verification; output; destruction.
- **Execution:** one particular run of a process.
- **Object:** anything that crosses a process boundary. Examples: a random number, the XOR result,
  the hash, the mnemonic, the output record. Objects have properties, and properties can be
  verified.
- The secret is an object. The invariants in the secret paper are properties of that object. The
  two papers divide along this line: the secret paper is about the object, and this paper is about
  the processes that produce it.
- **Carriers:** the paper and the devices that hold objects are objects too. Some properties that
  matter for I3 belong to carriers, not to the secret: amnesiac, destroyed, offline.
- **Commit:** an output object is committed when it crosses the process boundary into a carrier
  that the process can no longer alter, in view of the user.
- Why carve the system this way: verification needs an object with a property to examine (2.3a).
  Validation needs a process to argue about (2.3c). Independence is a relation between processes
  (2.4). Where the boundaries are drawn decides what can be verified.
- Relationship to the method whitepaper: whitepaper 1.3 applies this model to the ceremony
  (Entropy Generation, then Encoding). It should cite this section for the definitions.

### 2.3 Verification

- **Definition:** confirming, through objective evidence that the user examines, that a specific
  object has a specific property.
- Three targets of assurance, which should be kept apart:
  - **a.** An output object: the secret or an intermediate value. Example: recomputing the
    mnemonic.
  - **b.** The execution: this particular run of the process. Example: watching the dice roll.
  - **c.** The process: every run of the process. This is validation, not verification.

  Assurance about (c) does not carry over to (b), and assurance about (b) does not carry over to
  (a).
- What is not verification, and why:
  - Audits and certification: someone else validated the process (c).
  - Code review, even by the user: this validates the process (c). It says nothing about whether
    the reviewed code is what actually ran (b), or about what it produced (a).
  - Tests and KATs: these check that the process is consistent, not that its output is secret
    (P4).
  - Open source: makes the process available for someone to validate. It is not evidence that
    anyone did.
- Only the user can verify for the user. Everything else is trust, and section 7 lists what trust
  remains.

### 2.4 Independence

Goal: a definition complete enough that the method and protocol can say "independent" and mean
all of this.

**Definition:** two elements are independent if no common cause affects both of their results
(independence in kind), and no information passes between them before both results are committed
(independence in order).

#### 2.4.1 Elements (in terms of the process model, 2.2)

- Elements are processes or executions:
  - entropy source processes, compared with one another;
  - executions of the same process, such as the encoding and its verification, compared with one
    another.
- Result: the element's output objects. For a source, its random number. For an execution, its
  XOR result, hash, and mnemonic.
- Committed: as defined in 2.2.

#### 2.4.2 Independence in kind: no common cause

- An element's result depends on everything in its dependency closure:
  - physical mechanism
  - hardware design and fabrication
  - firmware
  - operating system and libraries
  - compiler and toolchain
  - algorithm implementation
  - constants and reference data (e.g., a word list)
  - specification
  - supply chain (vendor, distribution channel)
  - environment (clock, boot state, power)
  - operator
- Two elements are independent in kind if their dependency closures do not overlap, apart from
  exceptions that are stated explicitly:
  - Sources: no exceptions. They share nothing.
  - Executions: the specification must be shared. That is the point of checking one against the
    other. Nothing below the specification may be shared: not the implementation, not the
    reference data, not the toolchain.
  - The operator: a stated exception, and one inherent to the secret. I2 and I3 are both defined
    relative to the user. The user is the one party the secret must be accessible to, so the user
    cannot be excluded from any element. What the operator exception does not cover: a device,
    tool, or reference that the user brings into more than one element. Those remain subject to
    the test.
- Corpus evidence:
  - Shared library: Debian and its derivatives; JSBN across many wallets; Infineon RSALib across
    passports, TPMs, and eIDs.
  - Shared state inside one program: Juniper, where X9.31 and Dual_EC were coupled through one
    global variable.
  - Shared environment: Ps and Qs (the same boot state), and the clock seeds in Milk Sad and
    Randstorm. Two sources seeded from the same clock are one source.
  - Shared constants: Dual_EC.
  - Shared firmware between a source and the mixing step: COLDCARD, where the dice contribution
    was mixed by the same firmware that held the faulty RNG.

#### 2.4.3 Independence in order: no information flow before commitment

- Neither element may receive the other's input, intermediate values, or result before its own
  result is committed.
- A committed result may not be revised afterwards. Re-rolling or regenerating after seeing
  another result is a form of selection.
- Why this matters for sources: a faulty or malicious element that sees source A can choose its
  own output B to cancel A. With XOR, B = target XOR A fixes the secret at the target. Order is
  what stops the last source from choosing the secret.
- Why this matters for executions: an execution that sees the other's result can reproduce it,
  whether by copying or by a device echoing its input. Agreement then proves nothing.
- Consequence: the protocol's rule that each source is committed before any other is entered is
  independence in order. It does not need to be a separate requirement.

#### 2.4.4 Establishing independence

- Independence in order can be verified by monitoring (2.5): the user observes when each result
  is committed and what each element has been given.
- Independence in kind requires the user to know each element's dependency closure. How a user
  can establish that, and which means make it easiest, is for the method whitepaper.

### 2.5 Monitoring

- **Definition:** the user witnesses every step at which secret material, or anything that
  determines it, exists. Nothing happens out of the user's view.
- Monitoring is verification of the execution (2.3b). It is not verification of the output.
- What can and cannot be monitored:
  - A die roll can be seen.
  - A device's internal computation cannot be seen. The user can monitor only what goes in, what
    comes out, and whether the device is offline.
- Monitoring is how I3 is verified at generation: the user can account for every copy.
- Consequence for devices: a device's internal state can never be verified, only bounded. Its
  outputs are checked against an independent execution, its transmission is blocked by an
  enclosure the user tests, and its state-retaining components are destroyed. Amnesia cannot be
  verified; destruction can.


## 3 The Assurance Record in the Corpus

The evidence that validation is not sufficient.

### 3.1 Assurance questions

Asked of each case:

- **a.** How was the defect found, by whom, and what did they need (only public data, or access
  to the device)?
- **b.** Did any assurance mechanism exist (tests, KAT, certification, code guard, open source)?
  Why did it not catch the defect?

| Case         | Found by                         | Assurance in place (to fill)     |
|--------------|----------------------------------|----------------------------------|
| Debian       | code review, ~2 yrs later        | open source, distro review       |
| Ps and Qs    | internet scan of public keys     | -                                |
| Android      | public chain                     | platform CSPRNG API              |
| Dual_EC      | cryptanalysis of the standard    | NIST standard                    |
| Juniper      | code audit after the Q change    | FIPS, KAT                        |
| ROCA         | statistics of public keys        | FIPS 140-2, CC EAL5+             |
| Randstorm    | researcher analysis              | open source                      |
| Profanity    | researcher analysis; exploited   | open source                      |
| Milk Sad     | victims' funds swept             | open source                      |
| COLDCARD     | third-party code review          | open source, #error guard        |

(To be checked against the primary sources.)

### 3.2 Why validation failed

Patterns grouped by what went wrong:

- **The failure produced no evidence.**
  - **P1 Silent failure.** No error was raised, and the output was well-formed.
    *Debian, Android, Milk Sad, COLDCARD guard.*
  - **P2 Width mismatch.** The interface was wider than the entropy passing through it.
    *Debian counter, Milk Sad, Profanity, COLDCARD 32-bit reseed.*
- **The check existed but did not work.**
  - **P3 The safeguard existed and was defeated.**
    *Juniper X9.31 loop, COLDCARD #ifndef, Juniper KAT updated along with Q.*
  - **P4 Testing the output cannot detect the failure.** Statistical tests pass, and a KAT tests
    consistency, not secrecy.
    *Dual_EC, and every deterministic PRNG in the corpus.*
- **Someone else performed the check.**
  - **P5 Assurance by credential did not help.**
    *ROCA (FIPS 140-2, CC EAL5+), Juniper (FIPS), open source (Debian, libbitcoin, COLDCARD).*
- **The checks were not actually independent.**
  - **P7 Shared dependency.** One defect propagated through everything built on it.
    *Debian derivatives, BitcoinJS/JSBN, Infineon across passports, TPMs, and eIDs.*

### 3.3 What verification looked like

- **P6 Asymmetric detection.** The attacker can check candidate keys offline against public data.
  The user has no equivalent check.
  *Ps and Qs, ROCA fingerprinting, Milk Sad, Profanity, chain-visible nonce reuse.*
- **P8 The user could not see what their input contributed.**
  *COLDCARD "Dice Rolls" (safe, but the user could not confirm it) vs. "Dice Rolls Only" (the user
  can confirm it externally).*
- The attackers in the corpus were verifying outputs. The users had no equivalent option.


## 4 What Can Be Verified, per Invariant

| Invariant | Output                 | Execution                                          | When                       |
|-----------|------------------------|----------------------------------------------------|----------------------------|
| I1        | No (P4)                | Partly: physical sources yes, device internals no  | Generation only            |
| I2        | Yes, by reconstruction | Yes                                                | Generation, then on demand |
| I3        | No                     | Yes, by monitoring every copy (2.5)                | Generation only            |

The gap to close: I1 cannot be verified from the output. Section 5 closes it through requirements.


## 5 Deriving the Requirements

Each subsection follows the same pattern:

- the principle it follows from;
- the requirement that results;
- the corpus cases it would have stopped;
- how it compares with the draft R-number.

### 5.1 R1, redundant and independent sources

Follows from I1 not being verifiable (section 4).

- If a secret combines several sources, it is unpredictable as long as at least one source is
  unpredictable and the sources are independent (2.4).
- Each source must provide the full target entropy. Otherwise the guarantee depends on which
  source is the good one.
- Corpus: every source-stage and design-stage failure (Debian, Ps and Qs, Android, Dual_EC,
  Randstorm, Milk Sad, Profanity, COLDCARD).
- Proposed changes to draft R1:
  - "should contribute" becomes "must contribute".
  - "independent\*" becomes simply "independent", as defined in 2.4. Order, including
    commit-before-entry, is part of that definition.

### 5.2 R2, a defined encoding

Follows from verification needing something to compare against.

- An execution cannot be verified without a specification to check it against.
- Candidate refinements:
  - The algorithm must have no constants whose origin cannot be checked (Dual_EC).
  - The specification must be complete enough that two implementations sharing nothing below it
    (2.4.2) produce the same result. Without that, an independent second execution is not
    possible.

### 5.3 R3, the user verifies the encoding

Follows from 2.3a: the output of mixing and encoding can be verified.

- Verify by running the process twice, the two executions independent (2.4), and comparing the
  results.
- Hand computation is not required. What is required is that the verification be independent.
  Which means achieve that most strongly is for the method whitepaper.
- Corpus: Juniper (the post-processing stage never ran), COLDCARD reseed, and P8.
- Draft R3 says the verification "must cover I2 and I3." Examine whether it can: encoding
  verification establishes I1's mixing condition. It does not establish I2 or I3.
  - Candidate: split I2 and I3 into their own requirements (5.5).

### 5.4 R4, the user monitors throughout

Follows from 2.5 and from I3 being verifiable only at generation.

- Specify what "monitor" means for physical steps and for device steps, separately.
- Specify what "throughout" covers: from the first source to the destruction of the last
  intermediate value.
- Corpus: nothing in the corpus was monitored by the user. This requirement follows from first
  principles, not from the cases.

### 5.5 Candidate requirements the derivation brings out

- **R5 (I3): account for every copy.** Every device and document that held secret material must
  be accounted for: either retained as the output record, or destroyed. "Amnesiac" does not
  qualify, because it cannot be verified (2.5). Corresponds to the protocol's Destruction step.
- **R6 (I2): verify the output.** Check the retained output record against the verified mnemonic
  before the working copies are destroyed. Corresponds to the protocol's Output step.
- Resolved: commit-before-entry is not a separate requirement. It is independence in order
  (2.4.3).
- Resolved: hand computation is not a requirement. Independent verification is (5.3).

### 5.6 Resulting requirement set

Filled in as the derivation proceeds.


## 6 From Requirements to Means

- The requirements in section 5 name no technology. Any means that satisfies them conforms.
- What makes a means better or worse is how cheaply the user can establish independence in kind
  (2.4.4) and monitor the execution (2.5). This paper does not rank the means.
- Handoff to the method whitepaper, which argues that physical entropy and hand computation are
  the strongest way to establish independence.


## 7 What Remains Trusted

- The design of SHA-256. Its constants are derived from primes, so the user can recheck where they
  came from; it is still a cryptographic assumption.
- The BIP-39 word list: two printed copies from independent sources (protocol).
- Fairness of the physical source: the user witnesses it but does not verify it. The pairwise
  discard rule removes bias between rolls, but not dependence between them.
- The user, the stated exception to independence in kind (2.4.2), which is inherent to the
  secret. An error that the user carries into both executions, such as a mis-transcribed input,
  will pass the comparison. Such an error changes the secret, but does not by itself make it
  predictable (I1) or give it to anyone else (I3).
- The enclosure's shielding. The user tests it, but only across the frequencies their test
  covers.
- The security of the ceremony environment.
- I3 after the ceremony ends.


## 8 Limitations

- The corpus shows that validation failed. It cannot show that verification would have succeeded,
  because there is no counterfactual.
- The requirements assume a user willing to carry out two independent executions and monitor the
  whole ceremony. What that costs depends on the means chosen (method whitepaper).
- It covers a single user holding a single secret. Multi-party custody and institutional settings
  are not addressed.
- It covers generation only, up to the ceremony's output. Storage and use afterwards are not
  addressed: I3 cannot be verified after generation (secret paper 2.7), so requirements for that
  period would rest on trust, not verification. They belong to a lifecycle standard.


## 9 Conclusion

- Restate the derived requirement set.
- The attackers in the corpus verified. The users trusted validation performed by others. The
  requirements close that gap at the point of generation.


## Appendix A Assurance record per case (expanded from 3.1)

## Appendix B Worked example: applying the independence test (2.4) to a pair of sources and a pair of executions

## Appendix C Draft R1-R4 vs. derived requirements, side by side

## References
