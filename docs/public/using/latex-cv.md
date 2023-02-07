---
title: LaTeX Curriculum Vitae
---
# LaTeX Curriculum Vitae

Use jinja2 in LaTeX mode to generate a CV.

The example CV here was cribbed from [ TODO : where? ].

Unlike traditional jinja2, latexmode jinja2 uses slightly different syntax to avoid
conflicting.

A block is : \BLOCK{ ... }
A variable is: \VAR{ ... }
A comment is: \#{ ... }
A line statement (e.g. for)
block_start_string="\BLOCK{",
block_end_string="}",
variable_start_string="\VAR{",
variable_end_string="}",
comment_start_string="\#{",
comment_end_string="}",
line_statement_prefix="%%",
line_comment_prefix="%#",





cv.org
```
* details

** name

John Doe

** github

https://github.com/therealjohndoe

** email

johndoe@gmail.com

** linkedin

therealjohndoe

** website

http://www.geocities.com/johndoe

** telephone

07777 777777


* summary

This is a summary about me with a [[http://www.google.com][link to a website I made]] & some more stuff.

* experience

** Microsoft
:PROPERTIES:
:dates: 1980-2000
:END:

Invented Microsoft word.

** Google
:PROPERTIES:
:dates: January 2000-August 2020
:END:

Increased search volume by 50%.

```


cv.jinja2
```
%-----------------------------------------------------------------------------------------------------------------------------------------------%
%	The MIT License (MIT)
%
%	Copyright (c) 2021 Jitin Nair
%
%	Permission is hereby granted, free of charge, to any person obtaining a copy
%	of this software and associated documentation files (the "Software"), to deal
%	in the Software without restriction, including without limitation the rights
%	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
%	copies of the Software, and to permit persons to whom the Software is
%	furnished to do so, subject to the following conditions:
%	
%	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
%	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
%	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
%	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
%	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
%	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
%	THE SOFTWARE.
%	
%
%-----------------------------------------------------------------------------------------------------------------------------------------------%

%----------------------------------------------------------------------------------------
%	DOCUMENT DEFINITION
%----------------------------------------------------------------------------------------

% article class because we want to fully customize the page and not use a cv template
\documentclass[a4paper,12pt]{article}

%----------------------------------------------------------------------------------------
%	FONT
%----------------------------------------------------------------------------------------

% % fontspec allows you to use TTF/OTF fonts directly
% \usepackage{fontspec}
% \defaultfontfeatures{Ligatures=TeX}

% % modified for ShareLaTeX use
% \setmainfont[
% SmallCapsFont = Fontin-SmallCaps.otf,
% BoldFont = Fontin-Bold.otf,
% ItalicFont = Fontin-Italic.otf
% ]
% {Fontin.otf}

%----------------------------------------------------------------------------------------
%	PACKAGES
%----------------------------------------------------------------------------------------
\usepackage{url}
\usepackage{parskip} 	

%other packages for formatting
\RequirePackage{color}
\RequirePackage{graphicx}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage[scale=0.9]{geometry}

%tabularx environment
\usepackage{tabularx}

%for lists within experience section
\usepackage{enumitem}

% centered version of 'X' col. type
\newcolumntype{C}{>{\centering\arraybackslash}X} 

%to prevent spillover of tabular into next pages
\usepackage{supertabular}
\usepackage{tabularx}
\newlength{\fullcollw}
\setlength{\fullcollw}{0.47\textwidth}

%custom \section
\usepackage{titlesec}				
\usepackage{multicol}
\usepackage{multirow}

%CV Sections inspired by: 
%http://stefano.italians.nl/archives/26
\titleformat{\section}{\Large\scshape\raggedright}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{10pt}{10pt}

%Setup hyperref package, and colours for links
\usepackage[unicode, draft=false]{hyperref}
\definecolor{linkcolour}{rgb}{0,0.2,0.6}
\hypersetup{colorlinks,breaklinks,urlcolor=linkcolour,linkcolor=linkcolour}

%for social icons
\usepackage{fontawesome5}

%debug page outer frames
%\usepackage{showframe}

%----------------------------------------------------------------------------------------
%	BEGIN DOCUMENT
%----------------------------------------------------------------------------------------
\begin{document}

% non-numbered pages
\pagestyle{empty} 

%----------------------------------------------------------------------------------------
%	TITLE
%----------------------------------------------------------------------------------------

%% set details = root.at("details")

\begin{tabularx}{\linewidth}{@{} C @{}}
\Huge{\VAR{ details.at("name").body.strip }} \\[7.5pt]
\href{\VAR{ details.at("github").body.strip }}{\raisebox{-0.05\height}\faGithub\ \VAR{ details.at("github").body.strip }} \ $|$ \ 
\href{https://linkedin.com/in/\VAR{ details.at("linkedin").body.strip }}{\raisebox{-0.05\height}\faLinkedin\ \VAR{ details.at("linkedin").body.strip }} \ $|$ \ 
\href{https://mysite.com}{\raisebox{-0.05\height}\faGlobe \ mysite.com} \ $|$ \ 
\href{mailto:\VAR{ details.at("email").body.strip }}{\raisebox{-0.05\height}\faEnvelope \ \VAR{ details.at("email").body.strip }} \ $|$ \ 
\href{tel:\VAR{ details.at("telephone").body.strip}{\raisebox{-0.05\height}\faMobile \ \VAR{ details.at("telephone").body.strip} \\
\end{tabularx}

%----------------------------------------------------------------------------------------
% EXPERIENCE SECTIONS
%----------------------------------------------------------------------------------------

%Interests/ Keywords/ Summary
\section{Summary}
\VAR{ root.at("summary").body.latexed }

%Experience
\section{Work Experience}

%% for role in root.at("experience")
\begin{tabularx}{\linewidth}{ @{}l r@{} }
\textbf{role.name} & \hfill \VAR{ role.prop["dates"] } \\[3.75pt]
\multicolumn{2}{@{}X@{}}{\VAR{role.body}}  \\
\end{tabularx}
%% endfor

% \begin{tabularx}{\linewidth}{ @{}l r@{} }
% \textbf{Designation} & \hfill Mar 2019 - Jan 2021 \\[3.75pt]
% \multicolumn{2}{@{}X@{}}{
% \begin{minipage}[t]{\linewidth}
%    \begin{itemize}[nosep,after=\strut, leftmargin=1em, itemsep=3pt]
%        \item[--] long long line of blah blah that will wrap when the table fills the column width
%        \item[--] again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah. again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah
%    \end{itemize}
%    \end{minipage}
%}
% \end{tabularx}

%Projects
\section{Projects}

\begin{tabularx}{\linewidth}{ @{}l r@{} }
\textbf{Some Project} & \hfill \href{https://some-link.com}{Link to Demo} \\[3.75pt]
\multicolumn{2}{@{}X@{}}{long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width}  \\
\end{tabularx}

%----------------------------------------------------------------------------------------
%	EDUCATION
%----------------------------------------------------------------------------------------
\section{Education}
\begin{tabularx}{\linewidth}{@{}l X@{}}	
2030 - present & PhD (Subject) at \textbf{University} \hfill \normalsize (GPA: 4.0/4.0) \\

2023 - 2027 & Bachelor's Degree at \textbf{College} \hfill (GPA: 4.0/4.0) \\ 

2022 & Class 12th Some Board \hfill  (Grades) \\

2021 & Class 10th Some Board \hfill  (Grades) \\
\end{tabularx}

%----------------------------------------------------------------------------------------
%	SKILLS
%----------------------------------------------------------------------------------------
\section{Skills}
\begin{tabularx}{\linewidth}{@{}l X@{}}
Some Skills &  \normalsize{This, That, Some of this and that etc.}\\
Some More Skills  &  \normalsize{Also some more of this, Some more that, And some of this and that etc.}\\  
\end{tabularx}

\vfill
\center{\footnotesize Last updated: \today}

\end{document}

```




orji --latexmode cv.org cv.jinja2


```
%-----------------------------------------------------------------------------------------------------------------------------------------------%
%	The MIT License (MIT)
%
%	Copyright (c) 2021 Jitin Nair
%
%	Permission is hereby granted, free of charge, to any person obtaining a copy
%	of this software and associated documentation files (the "Software"), to deal
%	in the Software without restriction, including without limitation the rights
%	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
%	copies of the Software, and to permit persons to whom the Software is
%	furnished to do so, subject to the following conditions:
%	
%	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
%	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
%	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
%	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
%	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
%	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
%	THE SOFTWARE.
%	
%
%-----------------------------------------------------------------------------------------------------------------------------------------------%

%----------------------------------------------------------------------------------------
%	DOCUMENT DEFINITION
%----------------------------------------------------------------------------------------

% article class because we want to fully customize the page and not use a cv template
\documentclass[a4paper,12pt]{article}

%----------------------------------------------------------------------------------------
%	FONT
%----------------------------------------------------------------------------------------

% % fontspec allows you to use TTF/OTF fonts directly
% \usepackage{fontspec}
% \defaultfontfeatures{Ligatures=TeX}

% % modified for ShareLaTeX use
% \setmainfont[
% SmallCapsFont = Fontin-SmallCaps.otf,
% BoldFont = Fontin-Bold.otf,
% ItalicFont = Fontin-Italic.otf
% ]
% {Fontin.otf}

%----------------------------------------------------------------------------------------
%	PACKAGES
%----------------------------------------------------------------------------------------
\usepackage{url}
\usepackage{parskip} 	

%other packages for formatting
\RequirePackage{color}
\RequirePackage{graphicx}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage[scale=0.9]{geometry}

%tabularx environment
\usepackage{tabularx}

%for lists within experience section
\usepackage{enumitem}

% centered version of 'X' col. type
\newcolumntype{C}{>{\centering\arraybackslash}X} 

%to prevent spillover of tabular into next pages
\usepackage{supertabular}
\usepackage{tabularx}
\newlength{\fullcollw}
\setlength{\fullcollw}{0.47\textwidth}

%custom \section
\usepackage{titlesec}				
\usepackage{multicol}
\usepackage{multirow}

%CV Sections inspired by: 
%http://stefano.italians.nl/archives/26
\titleformat{\section}{\Large\scshape\raggedright}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{10pt}{10pt}

%Setup hyperref package, and colours for links
\usepackage[unicode, draft=false]{hyperref}
\definecolor{linkcolour}{rgb}{0,0.2,0.6}
\hypersetup{colorlinks,breaklinks,urlcolor=linkcolour,linkcolor=linkcolour}

%for social icons
\usepackage{fontawesome5}

%debug page outer frames
%\usepackage{showframe}

%----------------------------------------------------------------------------------------
%	BEGIN DOCUMENT
%----------------------------------------------------------------------------------------
\begin{document}

% non-numbered pages
\pagestyle{empty} 

%----------------------------------------------------------------------------------------
%	TITLE
%----------------------------------------------------------------------------------------

\begin{tabularx}{\linewidth}{@{} C @{}}
\Huge{John Doe} \\[7.5pt]
\href{https://github.com/therealjohndoe}{\raisebox{-0.05\height}\faGithub\ https://github.com/therealjohndoe} \ $|$ \ 
\href{https://linkedin.com/in/therealjohndoe}{\raisebox{-0.05\height}\faLinkedin\ therealjohndoe} \ $|$ \ 
\href{https://mysite.com}{\raisebox{-0.05\height}\faGlobe \ mysite.com} \ $|$ \ 
\href{mailto:johndoe@gmail.com}{\raisebox{-0.05\height}\faEnvelope \ johndoe@gmail.com} \ $|$ \ 
\href{tel:07777 777777{\raisebox{-0.05\height}\faMobile \ 07777 777777 \\
\end{tabularx}

%----------------------------------------------------------------------------------------
% EXPERIENCE SECTIONS
%----------------------------------------------------------------------------------------

%Interests/ Keywords/ Summary
\section{Summary}

This is a summary about me with a \href{http://www.google.com}{link to a website I made} \& some more stuff.


%Experience
\section{Work Experience}

\begin{tabularx}{\linewidth}{ @{}l r@{} }
\textbf{role.name} & \hfill 1980-2000 \\[3.75pt]
\multicolumn{2}{@{}X@{}}{
Invented Microsoft word.
}  \\
\end{tabularx}
\begin{tabularx}{\linewidth}{ @{}l r@{} }
\textbf{role.name} & \hfill January 2000-August 2020 \\[3.75pt]
\multicolumn{2}{@{}X@{}}{
Increased search volume by 50%.}  \\
\end{tabularx}
% \begin{tabularx}{\linewidth}{ @{}l r@{} }
% \textbf{Designation} & \hfill Mar 2019 - Jan 2021 \\[3.75pt]
% \multicolumn{2}{@{}X@{}}{
% \begin{minipage}[t]{\linewidth}
%    \begin{itemize}[nosep,after=\strut, leftmargin=1em, itemsep=3pt]
%        \item[--] long long line of blah blah that will wrap when the table fills the column width
%        \item[--] again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah. again, long long line of blah blah that will wrap when the table fills the column width but this time even more long long line of blah blah
%    \end{itemize}
%    \end{minipage}
%}
% \end{tabularx}

%Projects
\section{Projects}

\begin{tabularx}{\linewidth}{ @{}l r@{} }
\textbf{Some Project} & \hfill \href{https://some-link.com}{Link to Demo} \\[3.75pt]
\multicolumn{2}{@{}X@{}}{long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width long long line of blah blah that will wrap when the table fills the column width}  \\
\end{tabularx}

%----------------------------------------------------------------------------------------
%	EDUCATION
%----------------------------------------------------------------------------------------
\section{Education}
\begin{tabularx}{\linewidth}{@{}l X@{}}	
2030 - present & PhD (Subject) at \textbf{University} \hfill \normalsize (GPA: 4.0/4.0) \\

2023 - 2027 & Bachelor's Degree at \textbf{College} \hfill (GPA: 4.0/4.0) \\ 

2022 & Class 12th Some Board \hfill  (Grades) \\

2021 & Class 10th Some Board \hfill  (Grades) \\
\end{tabularx}

%----------------------------------------------------------------------------------------
%	SKILLS
%----------------------------------------------------------------------------------------
\section{Skills}
\begin{tabularx}{\linewidth}{@{}l X@{}}
Some Skills &  \normalsize{This, That, Some of this and that etc.}\\
Some More Skills  &  \normalsize{Also some more of this, Some more that, And some of this and that etc.}\\  
\end{tabularx}

\vfill
\center{\footnotesize Last updated: \today}

\end{document}

```
