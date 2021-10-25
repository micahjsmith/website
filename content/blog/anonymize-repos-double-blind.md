Title: Anonymize GitHub repos for double-blind submission
Date: 2019-10-23
Category: research
Tags: latex
Slug: anonymize-github-repos-double-blind
Authors: Micah Smith

Many venues for submitting research in computer science and other academic fields follow a double-blind review process, in which the authors should be anonymous to the reviewers. This can cause conflicts with ideas from *open science* or with the evaluation of software contributions as any linked GitHub repositories can contain identifying information about the authors. In this post I'll describe how I set up my LaTeX projects to facilitate double blind submission.

### Example document

Imagine that we have written the following highly-complex research paper in LaTeX:

```latex
\documentclass[sigconf,anonymous]{acmart}
\begin{document}
\author{Micah Smith}
\title{Title}
\maketitle
Here is my code: \url{https://github.com/micahjsmith/code}.
\end{document}
```

We're using the popular `acmart` class file which is used in computer science conferences like CHI, SIGMOD, KDD, etc. This class has an `anonymous` option which serves to anonymize the author list anywhere it appears. But the repo I have linked still gives away identifying information: the organization name appears in the URL and if one clicks through, the name of the authors and institution appear prominently.

### Anonymizing the repo

One approach to providing anonymous access to our important code is to manually remove identifying information from files, create an archive (e.g. `code.tar.gz`) and upload it as supplementary material.

This has several drawbacks:

- not all submission sites allow this form of upload
- a tarball is not a friendly way to share code, as the reviewer attempts to browse code from their file system and may not have editors configured to display your file types with the correct syntax highlighting, etc.
- you may forget to update the archive if you have updating your code and submission.

A better approach is to use a service like [Anonymous GitHub](https://anonymous.4open.science), which proxies requests to your live GitHub repository and strips identifying information based on your custom configuration. To use Anonymous GitHub, paste the URL of a GitHub repository and list of terms to anonymize from every file; terms will be replaced with `XXX`.

In our case, we want to anonymize the terms `Micah Smith` and `MIT`. So we could start with the following term list:

```
Micah Smith
MIT
```

The problem with this is that the linked software has been released under the MIT License, so a reviewer viewing the README or LICENSE would see the license is called `XXX License` (because it has been anonymized) and conclude that the author is from MIT, breaking the anonymity. Other substring matches could cause issues in similar situations.

The solution is to take advantage of the (undocumented) full regex matching that Anonymous GitHub will perform. Each line can contain an [arbitrary Python regex](https://docs.python.org/3/library/re.html#regular-expression-syntax). Thus we can match `MIT` only when it is *not* followed by the characters ` License` using a *negative lookahead*:

```
Micah Smith
MIT(?! License)
```

The result is an anonymized repo that can be shared with reviewers: <https://anonymous.4open.science/r/code-7E01>

### Referencing the repo

We could just copy and paste the new link into our LaTeX document, but that's too easy, isn't it? A flexible approach is to store the original URL and the anonymized URL in variables and place the appropriate one into the text based on whether the version being compiled is anonymized or not.

```latex
\documentclass[sigconf,anonymous]{acmart}

\newcommand{\repourl}{https://github.com/micahjsmith/code}

% can be placed in 'anonymize.tex' and input to the main file
\makeatletter
  \if@ACM@anonymous
    \renewcommand{\repourl}{https://anonymous.4open.science/r/code-7E01}
  \fi
\makeatother

\begin{document}
\author{Micah Smith}
\title{Title}
\maketitle
Here is my code: \url{\repourl}.
\end{document}
```

In this case, I searched the `acmart.cls` class file for the `anonymous` flag finding the command `\if@ACM@anonymous`. You can freely use this command as a switch within your document if you [jump through the usual \makeatletter/\makeatother hoops](https://tex.stackexchange.com/a/8353). For a different document format, different logic would be needed. For example, `IEEEtran.cls` defines the `\ifCLASSOPTIONpeerreview` conditional, but fewer IEEE conferences use double-blind review.

When (when!) your paper is accepted, you can simply remove the `anonymous` flag from your document class declaration, and the original link will replace the anonymized link without needing to look through the document.

### Conclusion

Using Anonymous GitHub and some LaTeX tricks, our paper appears as normal when the `anonymous` flag is not set. But when the `anonymous` flag is set on the document class, our readers can click through to an anonymized rendering of our repository.

What approach have you used to anonymizing your submissions?
