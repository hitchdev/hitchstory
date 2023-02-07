---
title: LaTeX Letter
---
# LaTeX Letter

Use jinja2 in LaTeX mode to generate a letter.

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





letter.org
```
* from details
** name

John Doe

** address

1234 NW Bobcat Lane,
Bobcat City,
MO
65584-5678.

** telephone

+1-541-754-3010

** email

johndoe@gmail.com

** signature image


* body

Could I get world peace? Failing that maybe an Xbox.

Many thanks!

* to address

123 Elf Road,
North Pole,
88888

* postscript

P.S. An iPhone would also be acceptable.

```


letter.jinja2
```
% Thin Formal Letter
% LaTeX Template
% Version 2.0 (7/2/17)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@LaTeXTemplates.com)
%
% Originally based on an example on WikiBooks 
% (http://en.wikibooks.org/wiki/LaTeX/Letters) but rewritten as of v2.0
%
% License:
% CC BY-NC-SA 3.0 (http://creativecommons.org/licenses/by-nc-sa/3.0/)
%

%----------------------------------------------------------------------------------------
%	DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\documentclass[10pt]{letter} % 10pt font size default, 11pt and 12pt are also possible

\usepackage{geometry} % Required for adjusting page dimensions

\usepackage{graphicx}

%\longindentation=0pt % Un-commenting this line will push the closing "Sincerely," to the left of the page

\geometry{
    paper=a4paper, % Change to letterpaper for US letter
    top=3cm, % Top margin
    bottom=1.5cm, % Bottom margin
    left=4.5cm, % Left margin
    right=4.5cm, % Right margin
    %showframe, % Uncomment to show how the type block is set on the page
}

\usepackage[T1]{fontenc} % Output font encoding for international characters
\usepackage[utf8]{inputenc} % Required for inputting international characters

\usepackage{stix} % Use the Stix font by default

\usepackage{microtype} % Improve justification

%----------------------------------------------------------------------------------------
%	YOUR NAME & ADDRESS SECTION
%----------------------------------------------------------------------------------------
%
%% set fromdetails = root.at("from details")

\signature{
    \VAR{fromdetails.at("name").body.strip}
} % Your name for the signature at the bottom

\address{
\VAR{ fromdetails.at("address").body.strip.replace("\n", "\\\\ \n") } \\
\VAR{ fromdetails.at("telephone").body.strip } \\
\VAR{ fromdetails.at("email").body.strip }
} % Your address and phone number

%----------------------------------------------------------------------------------------

\begin{document}

%----------------------------------------------------------------------------------------
%	ADDRESSEE SECTION
%----------------------------------------------------------------------------------------

\begin{letter}{
\VAR{ root.at("to address").body.strip.replace("\n", "\\\\ \n") }
} % Name/title of the addressee

%----------------------------------------------------------------------------------------
%	LETTER CONTENT SECTION
%----------------------------------------------------------------------------------------

\opening{\textbf{Dear Sir or Madam,}}


\VAR{ root.at("body").body.latexed }


\vspace{2\parskip} % Extra whitespace for aesthetics

\closing{
Yours faithfully,
}

\ps{
%% if root.has("postscript")
\VAR{ root.at("postscript").body.latexed }
%% endif
} % Postscript text, comment this line to remove it

% \encl{Copyright permission form} % Enclosures with the letter, comment this line to remove it

%----------------------------------------------------------------------------------------

\end{letter}

\end{document}

```




orji --latexmode letter.org letter.jinja2


```
% Thin Formal Letter
% LaTeX Template
% Version 2.0 (7/2/17)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@LaTeXTemplates.com)
%
% Originally based on an example on WikiBooks 
% (http://en.wikibooks.org/wiki/LaTeX/Letters) but rewritten as of v2.0
%
% License:
% CC BY-NC-SA 3.0 (http://creativecommons.org/licenses/by-nc-sa/3.0/)
%

%----------------------------------------------------------------------------------------
%	DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\documentclass[10pt]{letter} % 10pt font size default, 11pt and 12pt are also possible

\usepackage{geometry} % Required for adjusting page dimensions

\usepackage{graphicx}

%\longindentation=0pt % Un-commenting this line will push the closing "Sincerely," to the left of the page

\geometry{
    paper=a4paper, % Change to letterpaper for US letter
    top=3cm, % Top margin
    bottom=1.5cm, % Bottom margin
    left=4.5cm, % Left margin
    right=4.5cm, % Right margin
    %showframe, % Uncomment to show how the type block is set on the page
}

\usepackage[T1]{fontenc} % Output font encoding for international characters
\usepackage[utf8]{inputenc} % Required for inputting international characters

\usepackage{stix} % Use the Stix font by default

\usepackage{microtype} % Improve justification

%----------------------------------------------------------------------------------------
%	YOUR NAME & ADDRESS SECTION
%----------------------------------------------------------------------------------------
%
\signature{
    John Doe
} % Your name for the signature at the bottom

\address{
1234 NW Bobcat Lane,\\ 
Bobcat City,\\ 
MO\\ 
65584-5678. \\
+1-541-754-3010 \\
johndoe@gmail.com
} % Your address and phone number

%----------------------------------------------------------------------------------------

\begin{document}

%----------------------------------------------------------------------------------------
%	ADDRESSEE SECTION
%----------------------------------------------------------------------------------------

\begin{letter}{
123 Elf Road,\\ 
North Pole,\\ 
88888
} % Name/title of the addressee

%----------------------------------------------------------------------------------------
%	LETTER CONTENT SECTION
%----------------------------------------------------------------------------------------

\opening{\textbf{Dear Sir or Madam,}}



Could I get world peace? Failing that maybe an Xbox.

Many thanks!



\vspace{2\parskip} % Extra whitespace for aesthetics

\closing{
Yours faithfully,
}

\ps{

P.S. An iPhone would also be acceptable.
} % Postscript text, comment this line to remove it

% \encl{Copyright permission form} % Enclosures with the letter, comment this line to remove it

%----------------------------------------------------------------------------------------

\end{letter}

\end{document}

```
