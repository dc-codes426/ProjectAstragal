INCIDENT REPORTS
Technical accounts of real-world entropy and key-generation failures. The focus is the defect itself:
what the code did, why it failed, and how much entropy survived. Dates and loss figures appear only
where they carry technical meaning.

Frontmatter fields and general document standards are defined in the project-wide policy. This file
covers only the conventions specific to this directory.


NAMING
Filename:       incident_report_<year>_<Name>.md
Example:        incident_report_2008_Debian_OpenSSL.md

<year> is the year the defect became public (disclosure, advisory, or publication), not the year it
was introduced. Where that is ambiguous, pick one and state the reasoning in the report.

<Name> is the common name of the incident, with words separated by underscores.

documentID follows IR-<year>-<Name>.md, with words separated by hyphens. The existing reports are not
yet consistent on whether a descriptive suffix is added (e.g. IR-2026-Coldcard-Exploit.md); this is
pending a decision in the project-wide policy.


STRUCTURE
Each report opens with a banner:

    ================================================================================
    Incident Report - <year> <Name>
    <optional line: CVE identifiers, advisory numbers, or paper authors and venue>
    ================================================================================

Sections are in capitals, with no markup. SUMMARY comes first and REFERENCES comes last. In between,
use whichever sections fit the incident. The common ones are:

    SUMMARY             A few sentences on the defect.
    THE CODE            The defective code, with a provenance marker (below).
    WHY IT FAILS        The mechanism: why the code does not do what it appears to do.
    RESULTING KEYSPACE  How much entropy survived, quantified where possible.
    SCOPE               Affected versions, products, and functionality.
    REFERENCES          Primary sources, with URLs.

Where there is no single code defect, MECHANISM may take the place of THE CODE / WHY IT FAILS.
Incident-specific sections (e.g. THE FALLBACK GENERATOR, THE 2012 CHANGE) are added as needed.


CODE PROVENANCE
Every code snippet is marked on the line above it with where it came from:

    [VERBATIM]      quoted from the cited primary source
    [DECOMPILED]    reconstructed from a binary by the cited researchers, not original source
    [RECONSTRUCTED] paraphrase of a pattern described in published analysis; not a literal quote

followed by the file path or source it refers to, e.g.

    [VERBATIM] crypto/rand/md_rand.c:247, inside ssleay_rand_add()

Code is indented eight spaces beneath its marker.
