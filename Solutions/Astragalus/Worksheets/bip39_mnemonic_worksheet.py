"""BIP-39 Mnemonic Derivation — compact single-operator version."""

import os, urllib.request

WORDLIST_PATH = "/home/claude/bip39_english.txt"
if not os.path.exists(WORDLIST_PATH):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt",
        WORDLIST_PATH)
with open(WORDLIST_PATH) as f:
    WORDS = [w.strip() for w in f if w.strip()]

doc = []

doc.append(r"""\documentclass[9pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[margin=10mm,top=14mm,bottom=12mm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{array}
\setlength{\parindent}{0em}
\setlength{\parskip}{1pt}

\newlength{\cw}\setlength{\cw}{4.4mm}
\newlength{\labw}\setlength{\labw}{24mm}

\newcommand{\cell}{\framebox[\cw][c]{\rule{0pt}{4.4mm}}}
\newcommand{\fcell}[1]{\framebox[\cw][c]{\raisebox{1mm}[4.4mm][0pt]{#1}}}
\newcommand{\kk}{\kern-\fboxrule}
\newcommand{\eight}{\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell}
\newcommand{\eleven}{\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell}

\newcommand{\resultrow}[1]{%
\par\noindent\makebox[\labw][l]{\small #1}%
\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight%
\hspace{2mm}\framebox[16mm][c]{\rule{0pt}{4.4mm}}\par\vspace{0.4mm}}

\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\footnotesize\scshape BIP-39 Mnemonic Derivation}
\fancyhead[R]{\footnotesize\thepage}
\fancyfoot[C]{\footnotesize\scshape security-sensitive --- destroy after use}

\begin{document}
""")

# ===== TITLE =====
doc.append(r"""
\begin{center}
{\Large\scshape BIP-39 Mnemonic Derivation}\\[2pt]
{\small Controlled Calculation --- 256-bit entropy to 24-word seed phrase}
\end{center}
\vspace{2mm}
\noindent
\begin{tabular}{|l|p{45mm}|l|p{45mm}|l|p{30mm}|}
\hline
\textbf{Doc.\ No.} & BIP39-MCR-001 & \textbf{Prepared by} & & \textbf{Date} & \\
\hline
\end{tabular}
\vspace{1mm}

\noindent
\begin{tabular}{|l|p{140mm}|}
\hline
\textbf{Inputs} & (1) Entropy Worksheet \rule{30mm}{0.4pt}\quad
(2) SHA-256 Worksheet \rule{30mm}{0.4pt} \\
\hline
\end{tabular}
\vspace{3mm}
""")

# ===== SECTION 1: ENTROPY =====
doc.append(r"""
\noindent{\bfseries\sffamily Section 1: Entropy Register (bits 1--256)}
\hfill{\footnotesize Source: Entropy Worksheet, 32 bits/row}
\par\vspace{0.5mm}\noindent\rule{\textwidth}{0.5pt}\par\vspace{2mm}
""")

for word in range(8):
    bit_start = word * 32 + 1
    bit_end = bit_start + 31
    # Compact bit labels
    doc.append(r"\noindent\makebox[\labw][l]{\footnotesize\ttfamily %d--%d}" % (bit_start, bit_end))
    doc.append(r"\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight")
    doc.append(r"\hspace{2mm}\framebox[16mm][c]{\rule{0pt}{4.4mm}}")
    doc.append(r"\par\vspace{0.4mm}")

# ===== SECTION 2: CHECKSUM =====
doc.append(r"""
\vspace{3mm}
\noindent{\bfseries\sffamily Section 2: Checksum (bits 257--264)}
\hfill{\footnotesize Source: SHA-256 Worksheet, first 8 bits of $H_0'$}
\par\vspace{0.5mm}\noindent\rule{\textwidth}{0.5pt}\par\vspace{2mm}
""")

doc.append(r"\noindent\makebox[\labw][l]{\footnotesize\ttfamily 257--264}")
doc.append(r"\eight")
doc.append(r"\par\vspace{1mm}")
doc.append(r"{\footnotesize\itshape Complete sequence: bits 1--256 (entropy) then 257--264 (checksum) = 264 bits total.}")

# ===== SECTION 3: BINARY TO DECIMAL =====
doc.append(r"""
\vspace{3mm}
\noindent{\bfseries\sffamily Section 3: Binary-to-Decimal Conversion (24 $\times$ 11-digit binary numbers)}
\par\vspace{0.5mm}\noindent\rule{\textwidth}{0.5pt}\par\vspace{1mm}

\noindent{\footnotesize Partition the 264 bits into 24 consecutive 11-digit binary numbers.
Convert each to decimal using place values
1024,\,512,\,256,\,128,\,64,\,32,\,16,\,8,\,4,\,2,\,1
(sum the place values where the digit is 1). The decimal is a wordlist index (0--2047).}
\vspace{2mm}
""")

place_values = [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]

for w in range(24):
    bit_start = w * 11 + 1
    bit_end = bit_start + 10

    # Compact header
    doc.append(r"\noindent{\small\bfseries W.%d}" % (w + 1))
    doc.append(r"\hspace{2mm}{\footnotesize bits %d--%d}" % (bit_start, bit_end))

    if bit_end > 256:
        doc.append(r"\hfill{\footnotesize\itshape includes checksum bits}")

    doc.append(r"\par\vspace{0.5mm}")

    # Bit position labels + cells on one line cluster
    doc.append(r"\noindent\makebox[\labw][l]{}")
    for i in range(11):
        bit_num = bit_start + i
        if i > 0:
            doc.append(r"\kk")
        doc.append(r"\makebox[\cw][c]{\fontsize{4.5pt}{5pt}\selectfont %d}" % bit_num)
    doc.append(r"\hspace{4mm}{\footnotesize decimal}\hspace{2mm}\framebox[16mm][c]{\rule{0pt}{4.4mm}}")
    doc.append(r"\hspace{2mm}{\footnotesize word}\hspace{2mm}\framebox[30mm][l]{\rule{0pt}{4.4mm}}")
    doc.append(r"\par\vspace{0.3mm}")

    # Cells
    doc.append(r"\noindent\makebox[\labw][l]{}")
    doc.append(r"\eleven")
    doc.append(r"\par\vspace{0.3mm}")

    # Place values (tiny, as reference)
    doc.append(r"\noindent\makebox[\labw][l]{}")
    for i, pv in enumerate(place_values):
        if i > 0:
            doc.append(r"\kk")
        doc.append(r"\makebox[\cw][c]{\fontsize{3.8pt}{4.2pt}\selectfont\color{black!50} %d}" % pv)
    doc.append(r"\par\vspace{2mm}")

# ===== SECTION 4: FINAL MNEMONIC =====
doc.append(r"""
\vspace{2mm}
\noindent{\bfseries\sffamily Section 4: Mnemonic Record}
\par\vspace{0.5mm}\noindent\rule{\textwidth}{0.5pt}\par\vspace{2mm}

\begin{center}
\begin{tabular}{|c|p{30mm}||c|p{30mm}||c|p{30mm}||c|p{30mm}|}
\hline
\textbf{\#} & \textbf{Word} &
\textbf{\#} & \textbf{Word} &
\textbf{\#} & \textbf{Word} &
\textbf{\#} & \textbf{Word} \\
\hline
""")
for row in range(6):
    cells = []
    for col in range(4):
        n = col * 6 + row + 1
        cells.append(f"{n} & ")
    doc.append(" & ".join(cells) + r" \\ \hline")

doc.append(r"""
\end{tabular}
\end{center}

\vspace{3mm}
\noindent{\footnotesize\textbf{Disposition.} Destroy all working papers
(this document, entropy worksheet, SHA-256 worksheet) by cross-cut shredding
or burning after verifying the seed phrase is functional.}

\newpage
""")

# ===== SECTION 5: WORDLIST =====
doc.append(r"""
\noindent{\bfseries\sffamily Section 5: BIP-39 English Wordlist (0--2047)}
\par\vspace{0.5mm}\noindent\rule{\textwidth}{0.5pt}
\vspace{2mm}
""")

WORDS_PER_COL = 136
COLS_PER_PAGE = 4
WORDS_PER_PAGE = WORDS_PER_COL * COLS_PER_PAGE

for page_start in range(0, 2048, WORDS_PER_PAGE):
    doc.append(r"\noindent")
    for col in range(COLS_PER_PAGE):
        col_start = page_start + col * WORDS_PER_COL
        col_end = min(col_start + WORDS_PER_COL, 2048)
        if col_start >= 2048:
            break
        sep = "" if col == 0 else r"\hfill"
        doc.append(sep + r"\begin{minipage}[t]{0.24\textwidth}")
        doc.append(r"\fontsize{6.5pt}{7.8pt}\selectfont\ttfamily")
        doc.append(r"\begin{tabular}[t]{@{}r@{\;\;}l@{}}")
        for i in range(col_start, col_end):
            doc.append(f"{i:>4} & {WORDS[i]} \\\\")
        doc.append(r"\end{tabular}")
        doc.append(r"\end{minipage}")
    if page_start + WORDS_PER_PAGE < 2048:
        doc.append(r"\newpage")

doc.append(r"\end{document}")

text = "\n".join(doc)
with open("/home/claude/bip39_compact.tex", "w") as f:
    f.write(text)
print("Lines:", text.count("\n"))
