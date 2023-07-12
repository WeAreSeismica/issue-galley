% Documentclass seismica.cls
% for Seismica, a community-driven, Diamond Open Access journal publishing peer-reviewed research in seismology and earthquake science.
% Current version with inputs from:
% Théa Ragon, Hannah Mark, Wasja Bloch, Thomas Lecocq

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{seismica}[2022 LaTeX2e document class]

\newif\if@onecolumn
\@onecolumnfalse
\DeclareOption{onecolumn}{\@onecolumntrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\if@onecolumn
\LoadClass[10pt,twoside,a4paper,onecolumn]{article}
\else
\LoadClass[10pt,twoside,a4paper,twocolumn]{article}
\fi

\RequirePackage[headsep=0.7cm,top=2cm,bottom=1.5cm,left=1.5cm,right=1.5cm,footskip=0.7cm]{geometry}
\setlength{\columnsep}{0.8cm}
\RequirePackage[table]{xcolor}
\definecolor{seismicacolor1light}{RGB}{38,81,143}
\definecolor{seismicacolor1}{RGB}{18,52,103}
\definecolor{seismicacolor2}{RGB}{77,185,123}
\definecolor{seismicacolor3}{RGB}{222,60,75}
\definecolor{seismicacolor4}{RGB}{205,204,36}
\definecolor{codebackcolor}{RGB}{243,243,243}
\RequirePackage[unicode,
bookmarks=true,
linkcolor=seismicacolor1light,
citecolor=seismicacolor1light,
hidelinks,
hyperfootnotes=false]{hyperref}
\hypersetup{colorlinks,linkcolor=seismicacolor1light}
\hypersetup{colorlinks,citecolor=seismicacolor1light}
\hypersetup{colorlinks,urlcolor=gray}
\RequirePackage{url}
\def\UrlBreaks{\do\/\do-\do_}

\RequirePackage{polyglossia}
\RequirePackage{fontspec}
\setmainlanguage[]{english}
%% extra options for Arabic (not supported by polyglossia)
\newfontfamily\arabicfont[Script=Arabic]{Arial} %{Noto Naskh Arabic}
\newcommand{\textarabic}[1]{\bgroup\textdir TRT\arabicfont #1\egroup} % Arabic inside LTR
\newcommand{\n}[1]{\bgroup\textdir TLT #1\egroup} % for digits inside Arabic text
\newenvironment{Arabic}{\textdir TRT\pardir TRT\arabicfont}{\hfill} % Arabic paragraph

\RequirePackage{graphicx}
\RequirePackage{titlesec}
\RequirePackage{titling}
\RequirePackage{abstract}
\RequirePackage{fancyhdr}
\RequirePackage{bookmark}
\RequirePackage{caption} 
%\RequirePackage[natbibapa,sectionbib,doi]{apacite}   ### TO DO!! Conflict with... ???
%\bibliographystyle{apacite}
\RequirePackage[round]{natbib}
\bibliographystyle{abbrvnat_seismica_upcasetitle}
%\bibliographystyle{abbrvnat_seismica}
\RequirePackage{doi}
\RequirePackage{academicons}
\RequirePackage[noblocks]{authblk}
\setcounter{Maxaffil}{0}
\RequirePackage{changepage}
\RequirePackage[savepos]{zref}
\RequirePackage{datatool}
\RequirePackage{etoolbox}
\RequirePackage{physics}
\RequirePackage{comment}
\RequirePackage{listings}
\RequirePackage[autostyle=false, style=english]{csquotes}
\RequirePackage{newunicodechar}

% fonts and math
\RequirePackage{amsmath}
\RequirePackage{lmodern}

\RequirePackage[autostyle=false, style=english]{csquotes}
\RequirePackage[opentype,default,tabular,lining]{sourcesanspro}
\RequirePackage[opentype,tabular,lining]{sourceserifpro}
\RequirePackage[opentype,lining]{sourcecodepro}

\newcommand{\sff}{\sourcesanspro}
\newcommand{\rmf}{\sourceserifpro}
\newcommand{\sflight}{\sourcesansprolight}
\newcommand{\rmlight}{\sourceserifprolight}
\urlstyle{sf}

% source sans pro does not handle +2010
\newunicodechar{^^^^2010}{-}

% Redefine thanks symbol for compatibility with fonts
\def\@fnsymbol#1{\ensuremath{\ifcase#1\or *\or \dagger\or \ddagger\or
		\mathsection\or \mathparagraph\or \|\or **\or \dagger\dagger
		\or \ddagger\ddagger \else\@ctrerr\fi}}

%-------------------------------------------------------------------------------
%                Configuration for authors
%-------------------------------------------------------------------------------

% package authblk
\renewcommand*{\Authsep}{, }
\renewcommand*{\Authand}{, }
\renewcommand*{\Authands}{, }
\renewcommand*{\Authfont}{\bfseries\sff}    % make author names boldface    
\setlength{\affilsep}{0.2cm}   % set the space between author and affiliation
\renewcommand*{\Affilfont}{\normalfont\sflight\small}
\renewcommand\AB@affilsepx{, \protect\Affilfont}

% package academicons
\newcommand{\orcid}[1]{
	\href{https://orcid.org/#1}{\textcolor[HTML]{A6CE39}{\aiOrcid}}}

%-------------------------------------------------------------------------------
%                information box
%-------------------------------------------------------------------------------
\RequirePackage[absolute]{textpos}
\RequirePackage{longtable,booktabs,tabularx,colortbl}

% Article info
\def\receiveddate#1{\def\@receiveddate{#1}}
\def\accepteddate#1{\def\@accepteddate{#1}}
\def\publisheddate#1{\def\@publisheddate{#1}}
\def\thevolume#1{\def\@thevolume{#1}}
\def\thenumber#1{\def\@thenumber{#1}}
\thenumber{}
\def\theyear#1{\def\@theyear{#1}}
\def\subtitle#1{\def\@subtitle{#1}}

% Volunteers names
\def\prodedname#1{\def\@prodedname{#1}}
\prodedname{}
\def\handedname#1{\def\@handedname{#1}}
\handedname{}
\def\copyedname#1{\def\@copyedname{#1}}
\copyedname{}
\def\translatorname#1{\def\@translatorname{#1}}
\translatorname{}
\def\reviewername#1{\def\@reviewername{#1}}
\reviewername{}
\def\suppmat#1{\def\@suppmat{#1}}
\suppmat{}

\newcommand{\@insert@metadata}{%
	\begin{textblock*}{3cm}[1,0](\dimexpr\textwidth-\oddsidemargin\relax,\dimexpr\pageheight-\zposy{loc:beg_abstract}sp\relax)
		\footnotesize\raggedright%
		\setlength{\parskip}{\baselineskip}%
		\setlength{\parindent}{\z@}%
		\more@metadata\par
	\end{textblock*}
}

\newcommand{\printifnotempty}[4]{%
	\sbox0{#3}%
	\ifdim\wd0=0pt
	{}% if #3 is empty
	\else
	%	\begin{flushright}
		{\raggedleft\sflight \textcolor{gray}{#1: }{#2}\sff \textcolor{gray}{#3}#4}% if #2 is not empty
		%	\end{flushright}
	\fi
}

\newcommand{\more@metadata}{%
	\printifnotempty{Production Editor}{\\}{\@prodedname}{\\}
	\printifnotempty{Handling Editor}{\\}{\@handedname}{\\}
	\printifnotempty{Copy \& Layout Editor}{\\}{\@copyedname}{\par}
	\printifnotempty{Signed reviewer(s)}{\\}{\@reviewername}{\par}
	\printifnotempty{Translated by}{\\}{\@translatorname}{\par}
	\printifnotempty{Received}{\\}{\@receiveddate}{\\}
	\printifnotempty{Accepted}{\\}{\@accepteddate}{\\}
	\printifnotempty{Published}{\\}{\@publisheddate}{\par}
}

%-------------------------------------------------------------------------------
%                Configuration for heading
%-------------------------------------------------------------------------------

\title{Issue \@thevolume, Volume \@thenumber,  \@theyear}
\author[]{}

\pretitle{
	\begin{flushleft}
		\fontsize{19pt}{1em}\bfseries\sff
	}
	\posttitle{%
		\vskip .2cm
		\fontsize{16pt}{1em}\bfseries\sff\color{seismicacolor1} 
		
		\@subtitle
	\end{flushleft}%
%	\vskip .2cm
}
\preauthor{%
%	\lineskip 0.2cm%
	\begin{flushleft}
	}
	
	\postauthor{%
	\end{flushleft}%
	\vskip -1cm
	\par
		\zsavepos{loc:end_authors}
}
\predate{}
\postdate{
}
\date{}

\newcommand{\banner}{banner_imprint}

\renewcommand\maketitlehooka{%
	\vspace{-1.5cm}
	\includegraphics[width=\textwidth]{\banner}
	
	{\vspace*{-1.3cm} \hspace{0.2cm} }
	
	\vspace*{1.7cm}
}

%\renewcommand\maketitlehookd{%
%	\pagestyle{fancy}
%	\thispagestyle{plain}
%%	\@insert@metadata
%}

%-------------------------------------------------------------------------------
%                Configuration for asbtract
%-------------------------------------------------------------------------------

\newcommand*{\abstracttitlestyle}[1]{{\sff \large \bfseries #1}}

\let\oldthanks\thanks
\renewcommand{\thanks}[1]{\oldthanks{\small \sflight #1}}

\newenvironment{summary}[1]
{
	\par
	\noindent \abstracttitlestyle{#1} \hspace{0.2cm}\normalsize \sffamily\color{seismicacolor1}
}{
	\vspace{0.3cm}}%

\newenvironment{tocwidth}{\begin{adjustwidth}{}{0.25\paperwidth}}{\end{adjustwidth}}
\newenvironment{abswidth}{\begin{adjustwidth}{}{0\paperwidth}}{\end{adjustwidth}}

%% abstract.sty specs, needed for saythanks
\setlength{\absleftindent}{0pt}
\setlength{\absrightindent}{0pt}
\renewcommand{\abstractname}{}   
\renewcommand{\absnamepos}{empty} 
\addto\captionsenglish{\renewcommand{\abstractname}{}} % necessary to remove abstract title... don't know why

\if@onecolumn
\newcommand*{\makeseistitle}[1]{%
	\maketitle
	\begin{abswidth}
		#1
	\end{abswidth}
%	\vspace*{0.7cm}
}
\else
\newcommand*{\makeseistitle}[1]{%
	\twocolumn[
	\maketitle
	\begin{abswidth}
	\begin{onecolabstract}
	\zsavepos{loc:beg_abstract}		
		#1
	\end{onecolabstract}
	\end{abswidth}
	\vspace*{0.7cm}
	]
}
\fi

\newcommand*{\addsummaries}[1]{%
	\twocolumn[
	\begin{abswidth}
		#1
	\end{abswidth}

%	\vspace*{0.7cm}
	]
}


%-------------------------------------------------------------------------------
%                Configuration for sections
%-------------------------------------------------------------------------------

\titleformat{\section}{\fontsize{14pt}{1em}\bfseries\sff}{\thesection}{1em}{}
%\titlespacing\section{0pt}{8pt plus 4pt minus 2pt}{6pt plus 2pt minus 2pt}
\titleformat{\subsection}{\fontsize{12pt}{0.3em}\bfseries\sff}{\thesubsection}{1em}{}
%\titlespacing\subsection{0pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}
\titleformat{\subsubsection}{\fontsize{11pt}{0.1em}\bfseries\sff}{\thesubsubsection}{1em}{}
%\titlespacing\subsubsection{0pt}{8pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}

\setcounter{secnumdepth}{3}


%-------------------------------------------------------------------------------
%                Configuration for header and footer
%-------------------------------------------------------------------------------

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
%\fancyfoot[L]{\sff\bfseries\footnotesize \thepage}
\fancyfoot[R]{\sflight \footnotesize {\scshape \bfseries \color{seismicacolor1light} SEISMICA}~|~volume \@thevolume.\@thenumber~|~\@theyear}
\fancyhead[L]{\sflight \footnotesize {\scshape \bfseries \color{seismicacolor1light} SEISMICA} | {\scshape \bfseries } }
%\fancyhead[R]{\footnotesize \@author[1]}
\renewcommand{\headrule}{}

\fancypagestyle{plain}{%
	\fancyhead{}
	\renewcommand{\headrule}{}
	\fancyfoot{}
%	\fancyfoot[L]{\sff\bfseries\footnotesize \thepage}
	\fancyfoot[R]{\sflight \footnotesize {\scshape \bfseries \color{seismicacolor1light} SEISMICA}~|~ISSN 2816-9387~|~volume \@thevolume.\@thenumber~|~\@theyear}
}

%-------------------------------------------------------------------------------
%                Configuration for TOC
%-------------------------------------------------------------------------------

\newcommand{\insertarticle}[3]{%
	\noindent \href{#3}{\textcolor{black}{#1}}\\
	\hspace*{.5cm}{\color{seismicacolor1}\textbf{#2}}
	\vspace*{.2cm}
}

%-------------------------------------------------------------------------------
%                Hyphenation and stuff
%-------------------------------------------------------------------------------

\hyphenation{seis-mo-lo-gy}
\hyphenation{seis-mo-ge-nic}
\hyphenation{earth-quake}


% end of seismica.cls 
