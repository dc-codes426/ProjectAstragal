"""Standalone generator for SHA-256 hand-computation worksheets.
Reproduces the layout from askii21m/sha256-by-hand, but as a self-contained
LaTeX file with no external dependencies."""

IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
     0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
     0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
     0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
     0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
     0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
     0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
     0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
     0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
     0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
     0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
     0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
     0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def given(label, value, show_hex=True):
    bits = format(value, "032b")
    groups = [r"\kk".join(r"\fcell{%s}" % b for b in bits[i:i+8])
              for i in range(0, 32, 8)]
    return r"\givenrow{%s}{%s}{%s}" % (
        label, r"\hspace{1.6mm}".join(groups),
        "%08x" % value if show_hex else "")

doc = []

# ===== PREAMBLE =====
doc.append(r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[margin=12mm,top=16mm,bottom=16mm]{geometry}
\usepackage{amsmath}
\usepackage{fancyhdr}
\setlength{\parindent}{1.2em}

\newlength{\cw}\setlength{\cw}{4.4mm}
\newlength{\labw}\setlength{\labw}{22mm}

\newcommand{\cell}{\framebox[\cw][c]{\rule{0pt}{4.4mm}}}
\newcommand{\fcell}[1]{\framebox[\cw][c]{\raisebox{1mm}[4.4mm][0pt]{#1}}}
\newcommand{\kk}{\kern-\fboxrule}
\newcommand{\eight}{\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell\kk\cell}

\newcommand{\rowcells}[1]{%
\par\noindent\makebox[\labw][l]{\small #1}%
\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight\hspace{1.6mm}\eight}

\newcommand{\blankrow}[1]{\rowcells{#1}\par\vspace{0.6mm}}

\newcommand{\resultrow}[1]{\rowcells{#1}%
\hspace{3mm}\framebox[18mm][c]{\rule{0pt}{4.4mm}}\par\vspace{0.6mm}}

\newcommand{\givenrow}[3]{%
\par\noindent\makebox[\labw][l]{\small #1}#2%
\hspace{3mm}\makebox[18mm][c]{\ttfamily\fontsize{7.2}{8.6}\selectfont #3}%
\par\vspace{0.6mm}}

\newlength{\rulew}
\setlength{\rulew}{32\cw}
\addtolength{\rulew}{4.8mm}
\addtolength{\rulew}{-28\fboxrule}

\newcommand{\ruleline}{\par\vspace{0.8mm}\noindent\hspace{\labw}%
\rule{\rulew}{0.5pt}\par\vspace{0.8mm}}

\newcommand{\grp}[1]{\par\vspace{2.5mm}\noindent{\small\itshape #1}\par\vspace{1mm}}
\newcommand{\beforerows}{\par\vspace{3.5mm}}

\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\fancyhead[L]{\footnotesize\scshape SHA-256 worksheet}
\fancyhead[R]{\footnotesize\thepage}
\fancyfoot[C]{\footnotesize a row with a box takes the hexadecimal value of that row}

\begin{document}
""")

# ===== INTRO =====
doc.append(r"""
\begin{center}
{\LARGE SHA-256 Worksheets}\par\medskip
{\large blank grids for working the algorithm by hand}
\end{center}
\bigskip
\begin{center}\begin{minipage}{125mm}
Work each round top to bottom. A rotation needs no arithmetic: write the word
twice on scrap and read a 32-bit window at the stated offset. A shift is not a
rotation, so $\mathrm{SHR}$ rows drop the bits that fall off the right and fill
from the left with zeros. Rows above a rule are operands, the row below it is
the result, except in a $\Sigma$ or $\sigma$ block, where the first row is the
word the rotations are taken of and only the three rows under it are combined.

A block with a \textsf{carry} row
is an addition, taken in one pass from right to left, and the carry entering a
column can exceed 1 when several operands are summed. The carry leaving the
leftmost column is discarded, which is what reduces the sum modulo
$2^{32}$. Every other block is
bitwise, a column at a time: an exclusive or, except for Ch and Maj, whose
captions on the round sheets give the rule.

Each result has a box for its hexadecimal value. It is optional, but filling it
in makes checking faster, since you compare eight characters instead of
thirty-two bits. Operand rows have no box because the trace prints hexadecimal
only for a result, so there would be nothing to check against.
\end{minipage}\end{center}
\newpage
""")

# ===== MESSAGE SCHEDULE =====
doc.append(r"\section*{Message schedule}")
doc.append(r"Sixteen words from the padded block:")
doc.append(r"\beforerows")
for t in range(16):
    doc.append(r"\resultrow{$\mathrm{W}_{%d}$}" % t)
doc.append(r"\newpage")

for t in range(16, 64):
    doc.append(r"\section*{$\mathrm{W}_{%d}="
               r"\sigma_1(\mathrm{W}_{%d})+\mathrm{W}_{%d}"
               r"+\sigma_0(\mathrm{W}_{%d})+\mathrm{W}_{%d}$}"
               % (t, t-2, t-7, t-15, t-16))
    doc.append(r"\grp{$\sigma_1(\mathrm{W}_{%d})$}" % (t-2))
    doc.append(r"\blankrow{$\mathrm{W}_{%d}$}" % (t-2))
    for r in ("ROTR^{17}", "ROTR^{19}", "SHR^{10}"):
        doc.append(r"\blankrow{$\mathrm{%s}$}" % r)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$\sigma_1$}")

    doc.append(r"\grp{$\sigma_0(\mathrm{W}_{%d})$}" % (t-15))
    doc.append(r"\blankrow{$\mathrm{W}_{%d}$}" % (t-15))
    for r in ("ROTR^{7}", "ROTR^{18}", "SHR^{3}"):
        doc.append(r"\blankrow{$\mathrm{%s}$}" % r)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$\sigma_0$}")

    doc.append(r"\grp{Sum}")
    for lab in (r"$\sigma_1$", r"$\mathrm{W}_{%d}$" % (t-7),
                r"$\sigma_0$", r"$\mathrm{W}_{%d}$" % (t-16), "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$\mathrm{W}_{%d}$}" % t)
    doc.append(r"\newpage")

# ===== IV =====
doc.append(r"\section*{The initial registers}")
doc.append(r"These are the fractional parts of the square roots of the "
           r"first eight primes. Copy them into $a$ to $h$ before round 0:")
doc.append(r"\beforerows")
for i, nm in enumerate("abcdefgh"):
    doc.append(given(r"$%s=H_{%d}$" % (nm, i), IV[i]))
doc.append(r"\newpage")

# ===== COMPRESSION ROUNDS =====
for t in range(64):
    doc.append(r"\section*{Round %d\hfill\normalsize $K_{%d}=\mathtt{%08x}$}"
               % (t, t, K[t]))
    doc.append(r"\grp{$\Sigma_1(e)$}")
    doc.append(r"\blankrow{$e$}")
    for r in ("ROTR^{6}", "ROTR^{11}", "ROTR^{25}"):
        doc.append(r"\blankrow{$\mathrm{%s}$}" % r)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$\Sigma_1$}")

    doc.append(r"\grp{$\mathrm{Ch}(e,f,g)$: take $f$ where $e$ is 1, else $g$}")
    for lab in ("$e$", "$f$", "$g$"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{Ch}")

    doc.append(r"\grp{$T_1=h+\Sigma_1+\mathrm{Ch}+K_{%d}+\mathrm{W}_{%d}$}" % (t, t))
    for lab in ("$h$", r"$\Sigma_1$", "Ch"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(given("$K_{%d}$" % t, K[t], show_hex=False))
    for lab in (r"$\mathrm{W}_{%d}$" % t, "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$T_1$}")

    doc.append(r"\newpage")

    doc.append(r"\section*{Round %d, continued}" % t)
    doc.append(r"\grp{$\Sigma_0(a)$}")
    doc.append(r"\blankrow{$a$}")
    for r in ("ROTR^{2}", "ROTR^{13}", "ROTR^{22}"):
        doc.append(r"\blankrow{$\mathrm{%s}$}" % r)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$\Sigma_0$}")

    doc.append(r"\grp{$\mathrm{Maj}(a,b,c)$: whichever value occurs twice}")
    for lab in ("$a$", "$b$", "$c$"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{Maj}")

    doc.append(r"\grp{$T_2=\Sigma_0+\mathrm{Maj}$}")
    for lab in (r"$\Sigma_0$", "Maj", "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$T_2$}")

    doc.append(r"\grp{$e'=d+T_1$}")
    for lab in ("$d$", "$T_1$", "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$e'$}")

    doc.append(r"\grp{$a'=T_1+T_2$}")
    for lab in ("$T_1$", "$T_2$", "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$a'$}")

    doc.append(r"\grp{Then $h\leftarrow g$, $g\leftarrow f$, $f\leftarrow e$, "
               r"$d\leftarrow c$, $c\leftarrow b$, $b\leftarrow a$, and $e'$ "
               r"and $a'$ are the new $e$ and $a$.}")
    doc.append(r"\newpage")

# ===== FINAL DIGEST =====
doc.append(r"\section*{The digest}")
doc.append(r"Each register is added to the value it started from, the "
           r"$H_i$ loaded before round 0:")
for i, nm in enumerate("abcdefgh"):
    if i == 4:
        doc.append(r"\newpage")
        doc.append(r"\section*{The digest, continued}")
    doc.append(r"\grp{$H_{%d}\leftarrow H_{%d}+%s$}" % (i, i, nm))
    for lab in (r"$H_{%d}$" % i, "$%s$" % nm, "carry"):
        doc.append(r"\blankrow{%s}" % lab)
    doc.append(r"\ruleline")
    doc.append(r"\resultrow{$H_{%d}$}" % i)

doc.append(r"\newpage")
doc.append(r"\end{document}")

text = "\n".join(doc)
with open("/home/claude/sha256_askii_style.tex", "w") as f:
    f.write(text)
print("Lines:", text.count("\n"))
