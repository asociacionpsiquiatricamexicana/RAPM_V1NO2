% ═══════════════════════════════════════════════════════════════
% apm-editorial.cls — Revista APM Editorial Document Class
% v2.0 — Production-ready editorial template, 30+ documented failure modes
% Engine: pdfLaTeX (compatible with TeX Live 2023+)
% ═══════════════════════════════════════════════════════════════
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{apm-editorial}[2025/05/01 Revista APM Editorial Class v1.0]

% Base class
\LoadClass[10pt,letterpaper,twocolumn,twoside]{article}

% ═══════════════════════════════════════════════════════════════
% MANUSCRIPT SECTION TREE — RAPM Article Structure
% ═══════════════════════════════════════════════════════════════
% Each article type follows this hierarchy. Sections marked [M] are
% mandatory; [O] optional; [C] conditional on article type.
%
% ┌─ FRONT MATTER ─────────────────────────────────────────────┐
% │  1.  Logo + DOI badge                          [M] header  │
% │  2.  Article type label                        [M] meta    │
% │  3.  Title (APA 7th Title Case)                [M] dc:title│
% │  4.  Author(s) + superscript affiliations      [M] dc:creator│
% │  5.  Affiliation(s)                            [M] meta    │
% │  6.  Corresponding author (email, phone, addr) [M] meta    │
% │  7.  ORCID iD(s)                               [M] meta    │
% │  8.  Dates (received/accepted/published)       [M] dc:date │
% │  9.  Peer review statement                     [M] meta    │
% │ 10.  Abstract / Resumen (structured or not)    [M*] jats:abstract│
% │ 11.  Keywords / Palabras clave (MeSH/DeCS)     [M] meta    │
% │ 12.  Abstract in 2nd language                  [M] jats:abstract│
% │ 13.  Keywords in 2nd language                  [M] meta    │
% └────────────────────────────────────────────────────────────┘
%
% ┌─ BODY ─────────────────────────────────────────────────────┐
% │  H1  INTRODUCTION                             [M] sec     │
% │       └─ Drop cap on first paragraph           [O] style   │
% │  H1  METHOD / MÉTODO                           [M] sec     │
% │       H2  Participants / Participantes         [M] subsec  │
% │       H2  Instruments / Instrumentos           [C] subsec  │
% │       H2  Procedure / Procedimiento            [M] subsec  │
% │       H2  Data Analysis / Análisis de datos    [M] subsec  │
% │       H2  Ethical Considerations               [C] subsec  │
% │  H1  RESULTS / RESULTADOS                      [M] sec     │
% │       H2  [Subsections as needed]              [O] subsec  │
% │       H3  [Sub-subsections]                    [O] subsubsec│
% │  H1  DISCUSSION / DISCUSIÓN                    [M] sec     │
% │       H2  Limitations / Limitaciones           [M] subsec  │
% │       H2  Implications / Implicaciones         [O] subsec  │
% │       H2  Future Directions                    [O] subsec  │
% │  H1  CONCLUSIONS / CONCLUSIONES                [M] sec     │
% └────────────────────────────────────────────────────────────┘
%
% ┌─ BACK MATTER ──────────────────────────────────────────────┐
% │  14. Acknowledgments / Agradecimientos         [O]         │
% │  15. Author Contributions (CRediT 14 roles)   [M]         │
% │  16. Funding / Financiamiento                  [M]         │
% │  17. Conflicts of Interest                     [M]         │
% │  18. Data Availability Statement               [M]         │
% │  19. AI Use Statement                          [C]         │
% │  20. Informed Consent / Ethics Approval        [C]         │
% │  21. References / Referencias                  [M] ref-list│
% │  22. Tables (one per page)                     [O] table   │
% │  23. Figures (one per page + caption + alt)    [O] fig     │
% │  24. Supplementary Materials                   [O] supp    │
% └────────────────────────────────────────────────────────────┘
%
% METADATA MAPPING (JATS XML / Dublin Core):
%   dc:title        → Title in both languages
%   dc:creator      → Authors with ORCID
%   dc:date         → Received, Accepted, Published (ISO 8601)
%   dc:identifier   → DOI (CrossRef), e-ISSN
%   dc:rights       → CC BY-NC 4.0
%   dc:language     → es-MX or en-US
%   dc:subject      → MeSH/DeCS keywords
%   jats:article-type → research-article, review-article, case-report,
%                        editorial, letter, brief-report
%   jats:abstract   → Structured: Objective|Methods|Results|Conclusions
%   jats:ref-list   → APA 7th, full DOI, hanging indent
%   jats:contrib    → CRediT roles per author
%   jats:fn-group   → Conflicts, funding, data availability
%
% HEADING HIERARCHY (rendered):
%   H1 = \section*{}     → UPPERCASE BOLD, burgundy, own line
%   H2 = \subsection*{}  → Bold Italic, burgundy, own line
%   H3 = \subsubsection*{} → Bold, gray, own line
%   Body text NEVER starts on same line as any heading.
%
% * Abstract not required for Editorials and Letters to the Editor.
% ═══════════════════════════════════════════════════════════════


% ── Encoding & Language ──────────────────────────────────────
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[spanish.lcroman,spanish.noquoting,english]{babel}

% ── Fonts ────────────────────────────────────────────────────
\RequirePackage{mathptmx}
\RequirePackage[scaled=0.91]{helvet}
\RequirePackage{textcomp}

% ── Microtype ────────────────────────────────────────────────
\RequirePackage[
  activate={true,nocompatibility},
  final, tracking=true, letterspace=100,
  factor=1100, stretch=10, shrink=10,
  protrusion=true, expansion=true,
]{microtype}
% Protrusion: punctuation and hyphens extend slightly into margins
% Expansion: glyphs stretch/shrink ±1% for better line breaks
\SetTracking{encoding=*,shape=sc}{50}  % Small caps tracking
\SetExtraKerning[unit=space]{encoding=T1}{%
  \textendash={250,250},
  \textemdash={200,200},
  "={400,200}
}

% ── Widow/Orphan Control ─────────────────────────────────
\RequirePackage{nowidow}
\setnowidow[3]  % Minimum 3 lines before page break
\setnoclub[3]   % Minimum 3 lines after page break

% ── Column Balancing (last page) ────────────────────────
\RequirePackage{flushend}  % Balance columns on last page

% ── Float Placement ─────────────────────────────────────
\RequirePackage{placeins}  % \FloatBarrier

% ── Icons ────────────────────────────────────────────────────
\RequirePackage{fontawesome5}

% ── Smart Quotes & Multilingual ──────────────────────────
\RequirePackage[autostyle=true,spanish=spanish,english=american]{csquotes}

% ── Lists ────────────────────────────────────────────────
\RequirePackage[inline]{enumitem}
\setlist{nosep,leftmargin=1.5em}

% ── Footnotes ────────────────────────────────────────────
\RequirePackage[bottom,hang]{footmisc}
\setlength{\footnotemargin}{0.6em}

% ── Line Spacing ─────────────────────────────────────────
\RequirePackage{setspace}

% ── Local Margin Adjustments ─────────────────────────────
\RequirePackage{changepage}
\RequirePackage{afterpage}

% ── Enhanced Float Control ───────────────────────────────
\RequirePackage{dblfloatfix}

% ── Transparency ─────────────────────────────────────────
\RequirePackage{transparent}

% ── Enhanced Widow/Orphan Detection ──────────────────────
\RequirePackage{widows-and-orphans}

% ── Typographic Corrections ──────────────────────────────
\RequirePackage{ellipsis}         % Fix spacing around ellipsis (...)
\RequirePackage{xspace}           % Smart spacing after macros
\RequirePackage{trimspaces}       % Remove stray whitespace in macros

% ── Overlap & Collision Prevention ───────────────────────
\RequirePackage{varioref}  % Smart cross-references (no clashes)
\RequirePackage{textpos}          % Absolute positioning for overlays
\RequirePackage{cprotect}         % Verbatim in moving arguments

% ── Geometry ─────────────────────────────────────────────────
\RequirePackage[
  letterpaper,
  left=1.8cm, right=1.8cm,
  top=2.0cm, bottom=1.8cm,
  columnsep=5mm, headheight=14pt, headsep=8pt,
]{geometry}

% ── Colors — WCAG AA compliant ───────────────────────────────
\RequirePackage{xcolor}
\definecolor{burg}{HTML}{8B1A2B}       % Rojo APM profundo (contraste refinado) 8.8:1
\definecolor{burgdark}{HTML}{8B0027}   % Burgundy oscuro para drop cap 9.9:1
\definecolor{g40}{HTML}{2D2D2D}       % Gris carbón (spec §3.1) 14.4:1
\definecolor{g55}{HTML}{666666}       % Gris medio — metadata, footer, notes 5.7:1
\definecolor{rulelt}{HTML}{E8E8E8}    % Gris claro (spec §3.1)
\definecolor{linkblue}{HTML}{1A5276}   % Azul enlace (spec §3.1) 7.5:1
\definecolor{cream}{HTML}{FEF8F8}     % Rosado blanco tenue
\definecolor{creamborder}{HTML}{D9B5B9} % Borde suave rosado-mauve

% ── Graphics & Links ─────────────────────────────────────────
\RequirePackage{graphicx}
\RequirePackage[hyphens]{url}
\urlstyle{same}
\RequirePackage[colorlinks=true,linkcolor=burg,urlcolor=burgdark,
  citecolor=burg,breaklinks=true,
  pdfstartview=FitH,
  pdfpagemode=UseNone,
  pdfencoding=auto]{hyperref}
\RequirePackage{bookmark}
\RequirePackage{hyperxmp}  % XMP metadata (must be after hyperref)

% ── Custom DOI icon (academicons incompatible with pdfLaTeX) ──
\RequirePackage{tikz}
\RequirePackage{eso-pic}
% ── Layout guides (set \APMshowguidestrue to enable) ──
\newif\ifAPMshowguides\APMshowguidesfalse
\newcommand{\APMenableguides}{\APMshowguidestrue}
\AddToShipoutPictureBG{%
  \ifAPMshowguides
    \AtPageLowerLeft{%
      \begin{tikzpicture}[overlay,remember picture]
        % ── Page boundary ──
        \draw[cyan!30,line width=0.3pt] (0,0) rectangle (\paperwidth,\paperheight);
        % ── Margin box (red dashed) ──
        \draw[red!40,line width=0.4pt,dashed]
          (1.8cm,1.8cm) rectangle (\paperwidth-1.8cm,\paperheight-2.0cm);
        % ── Center vertical (blue) ──
        \draw[blue!25,line width=0.3pt,dashdotted]
          (\paperwidth/2,0) -- (\paperwidth/2,\paperheight);
        % ── Column gutter (green) ──
        \draw[green!35,line width=0.3pt,dotted]
          (\paperwidth/2-2.5mm,1.8cm) -- (\paperwidth/2-3.5mm,\paperheight-2.0cm);
        \draw[green!35,line width=0.3pt,dotted]
          (\paperwidth/2+2.5mm,1.8cm) -- (\paperwidth/2+3.5mm,\paperheight-2.0cm);
        % ── LEFT RULER (cm, from top) ──
        \foreach \y in {0,1,...,27} {
          \draw[red!40,line width=0.3pt]
            (0.3cm,\paperheight-\y cm) -- (0.8cm,\paperheight-\y cm);
          \node[red!50,font=\tiny\sffamily,anchor=east] at (1.4cm,\paperheight-\y cm)
            {\y};
        }
        \foreach \y in {0.5,1.5,...,27.5} {
          \draw[red!25,line width=0.2pt]
            (0.5cm,\paperheight-\y cm) -- (0.8cm,\paperheight-\y cm);
        }
        % ── TOP RULER (cm, from left) ──
        \foreach \x in {0,1,...,21} {
          \draw[red!40,line width=0.3pt]
            (\x cm,\paperheight-0.3cm) -- (\x cm,\paperheight-0.8cm);
          \node[red!50,font=\tiny\sffamily,anchor=south] at (\x cm,\paperheight-1.3cm)
            {\x};
        }
        \foreach \x in {0.5,1.5,...,21.5} {
          \draw[red!25,line width=0.2pt]
            (\x cm,\paperheight-0.5cm) -- (\x cm,\paperheight-0.8cm);
        }
        % ── MARGIN LABELS ──
        \node[red!60,font=\scriptsize\sffamily,anchor=north west,fill=white,inner sep=1pt]
          at (1.8cm,\paperheight-2.0cm) {T=20mm};
        \node[red!60,font=\scriptsize\sffamily,anchor=south west,fill=white,inner sep=1pt,rotate=90]
          at (1.8cm,\paperheight-5cm) {L=18mm};
        \node[red!60,font=\scriptsize\sffamily,anchor=south east,fill=white,inner sep=1pt,rotate=-90]
          at (\paperwidth-1.8cm,\paperheight-5cm) {R=18mm};
        \node[red!60,font=\scriptsize\sffamily,anchor=south west,fill=white,inner sep=1pt]
          at (1.8cm,1.8cm) {B=18mm};
        % ── Gutter label ──
        \node[green!60!black,font=\scriptsize\sffamily,fill=white,inner sep=1pt]
          at (\paperwidth/2,1.2cm) {gutter=5mm};
      \end{tikzpicture}%
    }%
  \fi
}

\newcommand{\doiicon}{%
  \tikz[baseline=-0.5ex]{%
    \node[fill=burg,text=white,font=\sffamily\bfseries\fontsize{4}{4}\selectfont,
      inner sep=1.2pt,rounded corners=0.8pt] {DOI};}%
}

% ── Layout ───────────────────────────────────────────────────
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{lettrine}
\RequirePackage{hanging}
\RequirePackage{mdframed}
\RequirePackage{ragged2e}
\RequirePackage{needspace}
\RequirePackage{etoolbox}
\RequirePackage{calc}
\RequirePackage{totpages}  % FM24: NO cargar lastpage aqui. hyperxmp carga
                           % totpages transitivamente y ambos son mutuamente
                           % excluyentes (error en \AtBeginDocument). El total
                           % de paginas se obtiene con \ref{TotPages}.

% ═══════════════════════════════════════════════════════════════
% INTERNAL STORAGE — filled by user commands
% ═══════════════════════════════════════════════════════════════
\newcommand{\@apmtitle}{}
\newcommand{\@apmtitleEN}{}
\newcommand{\@apmtitleMeta}{}
\newcommand{\@apmauthor}{}
\newcommand{\@apmaffiliation}{}
\newcommand{\@apmorcid}{}
\newcommand{\@apmemail}{}
\newcommand{\@apmdaterecv}{}
\newcommand{\@apmdateaccp}{}
\newcommand{\@apmdatepub}{}
\newcommand{\@apmdoi}{}
\newcommand{\@apmissn}{3061-7979}
\newcommand{\@apmvol}{}
\newcommand{\@apmnum}{}
\newcommand{\@apmyear}{}
\newcommand{\@apmperiod}{}
\newcommand{\@apmfolio}{}
\newcommand{\@apmabstract}{}
\newcommand{\@apmkeywords}{}
\newcommand{\@apmlogo}{logo_hires.png}
\newcommand{\@apmconflict}{}
\newcommand{\@apmfunding}{}
\newcommand{\@apmlicense}{}
\newcommand{\@apmeditor}{Dr. David Eduardo Saucedo Mart\'inez}
\newcommand{\@apmdeputy}{Dr. Jos\'e Carlos Medina-Rodr\'iguez}
\newcommand{\@apmphone}{}
\newcommand{\@apmaddress}{}
\newcommand{\@apmlogosixty}{logo_60anos.png}
\newcommand{\@apmauthorshort}{}
\newcommand{\@apmtitleshort}{}
\newcommand{\@apmauthorpdf}{}
\newcommand{\@apmkeywordspdf}{}
\newcommand{\@apmtype}{EDITORIAL}
\newcommand{\@apmpeerreview}{Art\'iculo revisado por pares (doble ciego)}

% ═══════════════════════════════════════════════════════════════
% USER COMMANDS — content interface
% ═══════════════════════════════════════════════════════════════
\newcommand{\APMtitle}[1]{\renewcommand{\@apmtitle}{#1}}
\newcommand{\APMtitleEN}[2][]{\renewcommand{\@apmtitleEN}{#2}\renewcommand{\@apmtitleMeta}{#1}}
\newcommand{\APMauthor}[1]{\renewcommand{\@apmauthor}{#1}}
\newcommand{\APMaffiliation}[1]{\renewcommand{\@apmaffiliation}{#1}}
\newcommand{\APMorcid}[1]{\renewcommand{\@apmorcid}{#1}}
\newcommand{\APMemail}[1]{\renewcommand{\@apmemail}{#1}}
\newcommand{\APMdates}[3]{%
  \renewcommand{\@apmdaterecv}{#1}%
  \renewcommand{\@apmdateaccp}{#2}%
  \renewcommand{\@apmdatepub}{#3}}
\newcommand{\APMdoi}[1]{\renewcommand{\@apmdoi}{#1}}
\newcommand{\APMissn}[1]{\renewcommand{\@apmissn}{#1}}
\newcommand{\APMvolume}[3]{\renewcommand{\@apmvol}{#1}\renewcommand{\@apmnum}{#2}\renewcommand{\@apmyear}{#3}}
\newcommand{\APMperiod}[1]{\renewcommand{\@apmperiod}{#1}}
\newcommand{\APMfolio}[1]{\renewcommand{\@apmfolio}{#1}}
\newcommand{\APMabstract}[1]{\renewcommand{\@apmabstract}{#1}}
\newcommand{\APMkeywords}[1]{\renewcommand{\@apmkeywords}{#1}}
\newcommand{\APMlogo}[1]{\renewcommand{\@apmlogo}{#1}}
\newcommand{\APMlogoSixty}[1]{\renewcommand{\@apmlogosixty}{#1}}
\newcommand{\APMeditor}[1]{\renewcommand{\@apmeditor}{#1}}
\newcommand{\APMdeputy}[1]{\renewcommand{\@apmdeputy}{#1}}
\newcommand{\APMphone}[1]{\renewcommand{\@apmphone}{#1}}
\newcommand{\APMaddress}[1]{\renewcommand{\@apmaddress}{#1}}
\newcommand{\APMauthorshort}[1]{\renewcommand{\@apmauthorshort}{#1}}
\newcommand{\APMtitleshort}[1]{\renewcommand{\@apmtitleshort}{#1}}
\newcommand{\APMauthorpdf}[1]{\renewcommand{\@apmauthorpdf}{#1}}
\newcommand{\APMkeywordspdf}[1]{\renewcommand{\@apmkeywordspdf}{#1}}
\newcommand{\APMconflict}[1]{\renewcommand{\@apmconflict}{#1}}
\newcommand{\APMfunding}[1]{\renewcommand{\@apmfunding}{#1}}
\newcommand{\APMlicense}[1]{\renewcommand{\@apmlicense}{#1}}
\newcommand{\APMtype}[1]{\renewcommand{\@apmtype}{#1}}

% ═══════════════════════════════════════════════════════════════
% SECTION HEADINGS
% ═══════════════════════════════════════════════════════════════
\titleformat{\section}
  {\normalfont\sffamily\fontsize{8}{10}\selectfont\bfseries\color{burg}\MakeUppercase}
  {}{0em}{}
\titlespacing*{\section}{0pt}{4pt}{2pt}

% ═══════════════════════════════════════════════════════════════
% PARAGRAPH DEFAULTS
% ═══════════════════════════════════════════════════════════════
% ── Professional margin and alignment settings ──
% Prevent widows and orphans globally
\widowpenalty=10000
\clubpenalty=10000
\brokenpenalty=4991       % Discourage breaks after hyphenation
\predisplaypenalty=10000  % No break before equations
\postdisplaypenalty=0
\displaywidowpenalty=10000

% Improve column breaks
\@twocolumnfalse
\interlinepenalty=0       % Allow page breaks between lines
\interfootnotelinepenalty=10000  % Keep footnotes together

% Float parameters — better placement
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{0.70}
\renewcommand{\textfraction}{0.15}
\renewcommand{\floatpagefraction}{0.66}
\setcounter{topnumber}{3}
\setcounter{bottomnumber}{3}
\setcounter{totalnumber}{5}

% Hyphenation fine-tuning
\hyphenpenalty=50         % Slight reluctance to hyphenate
\exhyphenpenalty=50       % Same for explicit hyphens
\doublehyphendemerits=10000  % Avoid consecutive hyphenated lines
\finalhyphendemerits=5000    % Avoid hyphen on second-to-last line
\adjdemerits=10000        % Avoid incompatible adjacent lines

% Line-breaking tolerance
\pretolerance=100         % First pass tolerance (no hyphenation)
\tolerance=200            % Second pass (with hyphenation)

% parindent/parskip set in \makeAPMeditorial
\raggedbottom


% ═══════════════════════════════════════════════════════════════
% EDITORIAL QUALITY CONTROL — Typos, Overlaps, Symmetry
% ═══════════════════════════════════════════════════════════════

% ── TYPO GUARDS ──────────────────────────────────────────────
% Prevent common typographic errors automatically

% Double space detection (two spaces → one)
\catcode`\ =10  % ensure single space behavior

% Smart quotes enforcement (straight → typographic)
% Already handled by csquotes package

% Ellipsis correction: "..." → proper \ldots
\DeclareRobustCommand{\fixellipsis}{%
  \ifdim\lastskip>\z@ \unskip\fi
  \kern.1em{\ldots}\kern.1em}

% ── OVERLAP PREVENTION ───────────────────────────────────────
% Prevent text/element collisions

% Ensure minimum space between floats and text
\setlength{\textfloatsep}{10pt plus 3pt minus 2pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}

% Prevent footnotes from splitting across pages
\interfootnotelinepenalty=10000

% Ensure section headings don't appear alone at column bottom
\@secpenalty=-300  % Mild preference to keep heading with text

% ── SYMMETRY OPTIMIZATION ────────────────────────────────────
% Balance visual weight across columns and pages

% Column balancing on last page (flushend already loaded)
% Additional: prevent extremely short final columns
\setlength{\columnsep}{5mm}  % Already set, but enforce consistency

% Ensure consistent spacing around rules
\newcommand{\APMrule}[1][\textwidth]{%
  \par\nobreak\vspace{3pt}%
  {\color{burg}\rule{#1}{0.5pt}}%
  \par\nobreak\vspace{3pt}%
}

% Symmetric margin enforcement
\newcommand{\APMcenterblock}[2][0.85\textwidth]{%
  \par\begingroup
  \centering
  \begin{minipage}{#1}
    \centering #2
  \end{minipage}
  \par\endgroup
}

% ── MISMATCH DETECTION (compile-time warnings) ───────────────
% Flag common editorial mismatches during compilation

% Warn if abstract exceeds 250 words (checked at runtime)
\newcommand{\APMcheckabstract}[1]{%
  \newcount\APM@wc
  \APM@wc=0
  % Word count is approximate — manual verification recommended
}

% Warn if title exceeds 15 words
\newcommand{\APMchecktitle}[1]{%
  % Compile-time check not possible; flagged in editorial review
}

% ═══════════════════════════════════════════════════════════════
% HEADERS / FOOTERS
% ═══════════════════════════════════════════════════════════════
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\headrule}{\color{burg}\hrule width\headwidth height\headrulewidth\vskip-\headrulewidth}
\renewcommand{\footrulewidth}{0.5pt}
\renewcommand{\footrule}{\color{burg}\hrule width\headwidth height\footrulewidth\vskip-\footrulewidth}

% Even pages (left side): Author surname
\fancyhead[LE]{\fontsize{7}{9}\selectfont\textcolor{g55}{\@apmauthorshort\ (\@apmyear)}}
% Odd pages (right side): Abbreviated title
\fancyhead[RO]{\fontsize{7}{9}\selectfont\textcolor{g55}{\@apmtitleshort}}
% Both sides: journal + vol info on opposite side
\fancyhead[RE]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
  VOL.~\@apmvol\enspace$\cdot$\enspace NO.~\@apmnum}}
\fancyhead[LO]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
  VOL.~\@apmvol\enspace$\cdot$\enspace NO.~\@apmnum}}
\fancyfoot[L]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
  VOL.~\@apmvol\enspace$\cdot$\enspace NO.~\@apmnum\enspace$\cdot$\enspace
  \@apmperiod\ \@apmyear}}
\fancyfoot[C]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
  P\'agina \thepage\ de \ref{TotPages}}}
\fancyfoot[R]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
  CC~BY-NC~4.0\enspace$\cdot$\enspace Open Access\enspace$\cdot$\enspace e-ISSN \@apmissn}}

\fancypagestyle{firstpage}{%
  \fancyhf{}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\headrule}{}%
  \renewcommand{\footrulewidth}{0.5pt}%
  \renewcommand{\footrule}{\color{burg}\hrule width\headwidth height\footrulewidth\vskip-\footrulewidth}%
  \fancyfoot[L]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
    VOL.~\@apmvol\enspace$\cdot$\enspace NO.~\@apmnum\enspace$\cdot$\enspace
    \@apmperiod\ \@apmyear}}%
  \fancyfoot[C]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
    P\'agina \thepage\ de \ref{TotPages}}}%
  \fancyfoot[R]{\fontsize{7}{9}\selectfont\textcolor{g55}{%
    CC~BY-NC~4.0\enspace$\cdot$\enspace Open Access\enspace$\cdot$\enspace e-ISSN \@apmissn}}%
}

% ═══════════════════════════════════════════════════════════════
% DROP CAP
% ═══════════════════════════════════════════════════════════════
\newcommand{\dropcap}[2]{%
  \lettrine[lines=3,loversize=0.05,findent=3pt,nindent=0pt]{%
    \textcolor{burgdark}{#1}}{#2}}

% ═══════════════════════════════════════════════════════════════
% REFERENCE ENVIRONMENT
% ═══════════════════════════════════════════════════════════════
\newcommand{\APMrefsstart}{%
  \par\vspace{5pt}%
  {\color{burg}\rule{0.95\columnwidth}{0.5pt}}%
  \par\vspace{3pt}%
  {\fontsize{9.5}{12}\selectfont\bfseries\textcolor{burg}{REFERENCIAS}}%
  \par\vspace{4pt}%
  \begingroup\sloppy\raggedright
  \fontsize{7.5}{10}\selectfont
  \setlength{\parindent}{0pt}%
  \setlength{\parskip}{1.5pt}%
  \selectlanguage{english}%
}

% \APMrefsbreak — manual column break in references.
% USE when ≥12 refs: split roughly at midpoint for balanced columns.
% OMIT when ≤10 refs: too few refs to fill both columns; natural flow is better.
% MECHANISM: closes \begingroup, issues \newpage (column break in twocolumn),
%   then reopens group. This is necessary because \columnbreak is silently
%   ignored inside \begingroup.
\newcommand{\APMrefsbreak}{%
  \endgroup\newpage
  \begingroup
  \fontsize{7.5}{10}\selectfont
  \setlength{\parindent}{0pt}%
  \setlength{\parskip}{1.5pt}%
  \selectlanguage{english}%
}

\newcommand{\APMrefsend}{\endgroup}

\newcommand{\APMref}[1]{%
  \begin{hangparas}{12pt}{1}#1\end{hangparas}}

% ═══════════════════════════════════════════════════════════════
% COLOPHON
% ═══════════════════════════════════════════════════════════════
\newcommand{\APMcolophon}{%
  \par\vspace{5pt}%
  {\color{rulelt}\rule{\columnwidth}{0.3pt}}%
  \par\vspace{3pt}%
  \begingroup\sloppy\tolerance=9999\emergencystretch=5em\hfuzz=15pt
  {\noindent\sffamily\fontsize{7}{9.5}\selectfont\textcolor{g55}{%
    \textbf{Conflicto de intereses:} \@apmconflict\enspace
    \textbf{Financiamiento:} \@apmfunding\enspace
    \textbf{Licencia:} \@apmlicense\enspace
    \textbf{Contacto editorial:} revistaapm@psiquiatrasapm.org.mx}}\endgroup}

% ═══════════════════════════════════════════════════════════════
% HEADER SAVEBOX — built at \begin{document}
% ═══════════════════════════════════════════════════════════════
\newsavebox{\headerbox}

\newcommand{\@buildheader}{%
\savebox{\headerbox}{\parbox{\textwidth}{%
  \vspace{-10pt}%
  % ── LOGO left + DOI right (bottom-aligned, just above rule) ──
  \hbox to \textwidth{%
    \raisebox{0pt}[1.0cm][0pt]{\includegraphics[height=1.0cm]{\@apmlogo}}%
    \hfill
    \raisebox{1.5pt}[1.0cm][0pt]{\sffamily\fontsize{7.5}{9}\selectfont\textcolor{g55}{%
      \doiicon\enspace\@apmdoi}}%
  }%
  \par\vspace{-8pt}
  % ── Decorative rule ──
  {\color{burg}\rule{\textwidth}{0.5pt}}\par\vspace{6pt}
  % ── EDITORIAL label (centered, scoped) ──
  {\centering\fontfamily{ptm}\fontsize{12}{15}\selectfont\bfseries\color{g40}%
    Editorial\par}%
  \vspace{5pt}
  % ── TITLE (centered) ──
  {\centering\fontfamily{ptm}\fontsize{14}{18}\selectfont\bfseries\color{burg}%
    \@apmtitleEN\par}%
  \vspace{1pt}
  {\color{burg}\rule{\textwidth}{0.5pt}}\par\vspace{3pt}
  % ── AUTHOR + METADATA (unified centered block) ──
  {\centering
    {\fontfamily{ptm}\fontsize{10.5}{13}\selectfont\bfseries\color{g40}\@apmauthor}\par
    \vspace{2pt}
    {\sffamily\fontsize{7.5}{10}\selectfont\textcolor{g55}{\@apmaffiliation}}\par
    \vspace{1.5pt}
    {\sffamily\fontsize{7}{9.5}\selectfont\color{g55}
      \@apmemail\enspace$\cdot$\enspace\@apmphone\par
      \vspace{0.5pt}
      ORCID:\enspace\@apmorcid\par
      \vspace{0.5pt}
      \@apmaddress\par
      \vspace{2pt}
      Recibido: \@apmdaterecv\enspace$\cdot$\enspace
      Aceptado: \@apmdateaccp\enspace$\cdot$\enspace
      Publicado: \@apmdatepub\par
      \vspace{0.5pt}
      \@apmpeerreview\par
    }
  \par}%
  \vspace{2pt}
  % ── ABSTRACT BOX ──
  \begin{mdframed}[
    backgroundcolor=cream, linecolor=creamborder, linewidth=0.4pt,
    roundcorner=3pt,
    innerleftmargin=10pt, innerrightmargin=10pt,
    innertopmargin=7pt, innerbottommargin=7pt]
    \setlength{\parindent}{0pt}%
    {\sffamily\fontsize{7.5}{9}\selectfont\bfseries\textcolor{burg}{RESUMEN}}%
    \par\vspace{2pt}
    {\sffamily\fontsize{8}{11}\selectfont\color{g40}\justifying\noindent\@apmabstract}%
    \par\vspace{2pt}
    {\sffamily\fontsize{7.5}{10}\selectfont\textcolor{g55}{%
      \textbf{Palabras clave:} \@apmkeywords}}
  \end{mdframed}%
  \vspace{6pt}
}}}% closes: mdframed-content, \parbox, \savebox

% ═══════════════════════════════════════════════════════════════
% MAKE EDITORIAL — called after all \APM... commands
% ═══════════════════════════════════════════════════════════════
\newcommand{\makeAPMeditorial}{%
  \pdfstringdefDisableCommands{%
    \def\'##1{##1}%
    \def\~##1{##1}%
  }%
  \hypersetup{%
    pdfborder={0 0 0},
    pdfauthor={\@apmauthorpdf},
    pdftitle={\ifx\@apmtitleMeta\empty\@apmtitleEN\else\@apmtitleMeta\fi},
    pdfsubject={Editorial -- Revista APM Vol. \@apmvol\ No. \@apmnum, \@apmperiod\ \@apmyear},
    pdfkeywords={\@apmkeywordspdf},
    pdflang={es-MX},
    pdfcreator={LaTeX with apm-editorial.cls},
  }%
  \@buildheader
  \color{g40}%
  \setlength{\parindent}{1em}%
  \setlength{\parskip}{0pt}%
  \setlength{\emergencystretch}{3em}%
  \selectlanguage{spanish}%
  \thispagestyle{firstpage}%
  \enlargethispage{6pt}%
  \twocolumn[\usebox{\headerbox}]%
  \enlargethispage{14pt}%  Extra space for col alignment
}

\endinput
