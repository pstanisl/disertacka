\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{puthesis}
         [2008/05/02 v1.4 Princeton University Thesis class]
\RequirePackage{setspace}
\newcounter{subyear}
\setcounter{subyear}{\number\year}
\def\papertype#1{\gdef\@papertype{#1}}
\def\papertypeEN#1{\gdef\@papertypeEN{#1}}
\def\submitted#1{\gdef\@submitted{#1}}
\def\@submittedyear{\ifnum\month>10 \stepcounter{subyear}\thesubyear
  \else\thesubyear\fi}
\def\@submittedmonth{\ifnum\month>10 January\else\ifnum\month>5 November
  \else June\fi\fi}
\def\copyrightyear#1{\gdef\@copyrightyear{#1}}
\def\@copyrightyear{\number\year}
\def\authorcaption#1{\gdef\@authorcaption{#1}}
\def\authorcaptionEN#1{\gdef\@authorcaptionEN{#1}}
\def\advisercaption#1{\gdef\@advisercaption{#1}}
\def\advisercaptionEN#1{\gdef\@advisercaptionEN{#1}}
\def\titleEN#1{\gdef\@titleEN{#1}}
\def\adviser#1{\gdef\@adviser{#1}}
\def\departmentfieldcaption#1{\gdef\@departmentfieldcaption{#1}}
\def\departmentfieldcaptionEN#1{\gdef\@departmentfieldcaptionEN{#1}}
\def\departmentfield#1{\gdef\@departmentfield{#1}}
\def\departmentfieldEN#1{\gdef\@departmentfieldEN{#1}}
\long\def\@abstract{\@latex@error{No \noexpand\abstract given}\@ehc}
\long\def\@statement{\@latex@error{No \noexpand\statement given}\@ehc}
\newcommand*{\frontmatter}{
  \pagenumbering{arabic}
}
\newcommand*{\mainmatter}{}
\newcommand*{\makelot}{}
\newcommand*{\makelof}{}
\newcommand*{\makelos}{}
\newcommand*{\maketoc}{
  % Add ToC to the pdfbookmarks as a section, but not to the ToC itself.
  % only if we have the hyperref command that is necessary
  \ifdefined\pdfbookmark
     \phantomsection
     \pdfbookmark[1]{\contentsname}{Contents}
  \else
  \fi
  \setcounter{page}{1}
  \tableofcontents
  \clearpage
}
%% Setup a command to add extra space only if in singlespacing mode
\newcommand*{\extravspace}[1]{\vspace{0in}}
%% Setup a command to set spacing for body text; also used to restore spacing after long tables in document
\newcommand*{\bodyspacing}{
  \doublespacing
}
%% Setup a command to set spacing for long tables, to be used manually in document
\newcommand*{\tablespacing}{
  \singlespacing
}
%% Command inserted into the document immediately after \begin{document} to place all frontmatter
%%   This was formerly named 'begincmd' and called below in \AtBeginDocument{}
%%   However, that is not compatible with package 'hyperref'. \tableofcontents needs
%%   to be declared from within the document itself.
\newcommand*{\makefrontmatter}{
  \bodyspacing
  \frontmatter
  \maketitlepage
  \maketitlepageEN
  \makestatement
  \makeacknowledgements
  \makeabstract
  \maketoc
  \makelos
  \clearpage\mainmatter
}
\def\@submitted{\@submittedmonth~\@submittedyear}
\def\@dept{Cybernetics}
\def\@universitypref{}
\def\@deptpref{Katedra}
\def\departmentprefix#1{\gdef\@deptpref{#1}}
\def\university#1{\gdef\@univ{#1}}
\def\universityEN#1{\gdef\@univEN{#1}}
\def\faculty#1{\gdef\@faculty{#1}}
\def\facultyEN#1{\gdef\@facultyEN{#1}}
\def\department#1{\gdef\@dept{#1}}
\def\departmentEN#1{\gdef\@deptEN{#1}}
\long\def\acknowledgements#1{\gdef\@acknowledgements{#1}}
\long\def\listofshorcuts#1{\gdef\@listofshorcuts{#1}}
\def\dedication#1{\gdef\@dedication{#1}}

\def\@deptEN{Cybernetics}
\def\@universityprefEN{}
\def\@deptprefEN{Department}
\def\departmentprefix#1{\gdef\@deptprefEN{#1}}
\def\universityEN#1{\gdef\@univEN{#1}}
\def\facultyEN#1{\gdef\@facultyEN{#1}}
\def\departmentEN#1{\gdef\@deptEN{#1}}

\newcommand{\maketitlepage}{{
  \thispagestyle{empty}
  \sc
  \vspace*{0cm}
  \begin{center}
    \@univ \\
    \@faculty \\
    \@dept \\
  \end{center}
  \vspace*{4cm}
  % \extravspace{5cm}
  \begin{center}
    \LARGE \@title
  \end{center}
  \vspace*{3cm}
  % \extravspace{3cm}
  \begin{center}
    %A Dissertation \\
    %Presented to the Faculty \\
    %of Princeton University \\
    %in Candidacy for the Degree \\
    %of Doctor of Philosophy
    \LARGE \@papertype
    % \@papertype \\
    % \@submitted
  \end{center}
  \vspace{2cm}
  \extravspace{2cm}
  \begin{flushleft}
    %Recommended for Acceptance \\
    %by the
    \@authorcaption \  \@author \\
    \@advisercaption \  \@adviser \\
    \@departmentfieldcaption \  \@departmentfield
  \end{flushleft}
  % \vspace{.3in}
  % \extravspace{.3in}
  % \begin{center}
  %   \@submitted
  % \end{center}
  \clearpage
}}
\newcommand{\maketitlepageEN}{{
  \thispagestyle{empty}
  \sc
  \vspace*{0cm}
  \begin{center}
    \@univEN \\
    \@facultyEN \\
    \@deptEN \\
  \end{center}
  \vspace*{4cm}
  % \extravspace{5cm}
  \begin{center}
    \LARGE \@titleEN
  \end{center}
  \vspace*{3cm}
  % \extravspace{3cm}
  \begin{center}
    %A Dissertation \\
    %Presented to the Faculty \\
    %of Princeton University \\
    %in Candidacy for the Degree \\
    %of Doctor of Philosophy
    \LARGE \@papertypeEN
    % \@papertype \\
    % \@submitted
  \end{center}
  \vspace{2cm}
  \extravspace{2cm}
  \begin{flushleft}
    %Recommended for Acceptance \\
    %by the
    \@authorcaptionEN \  \@author \\
    \@advisercaptionEN \  \@adviser \\
    \@departmentfieldcaptionEN \  \@departmentfieldEN
  \end{flushleft}
  % \vspace{.3in}
  % \extravspace{.3in}
  % \begin{center}
  %   \@submitted
  % \end{center}
  \clearpage
}}
\newcommand*{\makecopyrightpage}{
  \thispagestyle{empty}
  \vspace*{0in}
  \begin{center}
    \copyright\ Copyright by \@author, \@copyrightyear. \\
    All rights reserved.
  \end{center}
  \clearpage
}
\newcommand*{\makeabstract}{
  \newpage
  %\addcontentsline{toc}{section}{Abstract}
  %\begin{center}
  %\Large \textbf{Abstrakt}
  %\end{center}
  \@abstract
  \thispagestyle{empty}
  \clearpage
}
\newcommand*{\makestatement}{
  \newpage
  %\addcontentsline{toc}{section}{Abstract}
  %\begin{center}
  %\Large \textbf{Abstrakt}
  %\end{center}
  \@statement
  \thispagestyle{empty}
  \clearpage
}
\def\makeacknowledgements{
  \ifx\@acknowledgements\undefined
  \else
    \ifdefined\phantomsection
     % makes hyperref recognize this section properly for pdf links
     \phantomsection
    \else
    \fi

    %\addcontentsline{toc}{section}{Acknowledgements}
    %\begin{center}
    %  \Large \textbf{Poděkování}
    %\end{center}
    \@acknowledgements
  \thispagestyle{empty}
    \clearpage
  \fi
  }
\def\makededication{
  \ifx\@dedication\undefined
  \else
    \vspace*{1.5in}
    \begin{flushright}
      \@dedication
    \end{flushright}
    \clearpage
  \fi
  }
\DeclareOption{lot}{\renewcommand*{\makelot}{
  \ifdefined\phantomsection
    % makes hyperref recognize this section properly for pdf links
    \phantomsection
  \else
  \fi
  \addcontentsline{toc}{chapter}{Seznam tabulek}\listoftables}}
\DeclareOption{lof}{\renewcommand*{\makelof}{
  \ifdefined\phantomsection
    % makes hyperref recognize this section properly for pdf links
    \phantomsection
  \else
  \fi
  \addcontentsline{toc}{chapter}{Seznam obrázků}\listoffigures}}
% \DeclareOption{los}{
%   \renewcommand*{\makelos}{
%     \RequirePackage{losymbol}
%     \section*{List of Symbols\@mkboth {LIST OF SYMBOLS}{LIST OF SYMBOLS}}
%     \@starttoc{los}
%   \ifdefined\phantomsection
%     % makes hyperref recognize this section properly for pdf links
%     \phantomsection
%   \else
%   \fi
%     \addcontentsline{toc}{section}{Seznam symbolů}
%   }
% }
\DeclareOption{los}{
  \renewcommand*{\makelos}{
    %\RequirePackage{losymbol}
    \section*{Seznam pou\v{z}it\'{y}ch zkratek\@mkboth {Seznam pou\v{z}it\'{y}ch zkratek}{Seznam pou\v{z}it\'{y}ch zkratek}}
    % \section*{{eznam}{Seznam}}
    %\@starttoc{los}
  \ifdefined\phantomsection
    % makes hyperref recognize this section properly for pdf links
    \phantomsection
  \else
  \fi
    \addcontentsline{toc}{chapter}{Seznam pou\v{z}it\'{y}ch zkratek}
	%\setcounter{page}{1}
    % TODO: Command does not work -> hardcoded filename (PS 20200127)
    % \@listofshorcuts
    \input{listofshorcuts}
  }
}
\DeclareOption{singlespace}{
  \renewcommand*{\bodyspacing}{
  \singlespacing
  }
  %% Add extra space only if in singlespacing mode
  \renewcommand*{\extravspace}[1]{\vspace{#1}}
}
%% Doublespacing is the default for the thesis -- need not be declared.
\DeclareOption{doublespacing}{
  \renewcommand*{\bodyspacing}{
  \doublespacing
  }
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions
%% Not necessary to specify the point size - we inherit it from above
%% \LoadClass[12pt]{report}
\LoadClass{report}
\setlength{\oddsidemargin}{.5in}   %{.4375in}
\setlength{\evensidemargin}{.5in} %{.4375in}
\setlength{\topmargin}{-.5in}  %{-.5625in}
\setlength{\footskip}{.25in} % to put page number 3/4" from the bottom of the page (1/4" from bottom of body text)
\setlength{\textheight}{9in}
\setlength{\textwidth}{6in}

%%% Alter LaTeX defaults to try to eliminate all widows and orphans
\clubpenalty=10000
\widowpenalty=10000

%%% try to avoid overfull lines by limiting how far it is okay to exceed the margins
%%% http://www.tex.ac.uk/cgi-bin/texfaq2html?label=overfull
\setlength{\emergencystretch}{2em}

\long\def\abstract#1{\gdef\@abstract{#1}}
\long\def\statement#1{\gdef\@statement{#1}}
%% 'begincmd' no longer used -- insert \makefrontmatter in the document instead. See above.
%\AtBeginDocument{\begincmd}
\endinput
%%
%% End of file `puthesis.cls'.
