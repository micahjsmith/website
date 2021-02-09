Title: Sharing a preprint using acmart
Date: 2021-02-08
Category: research
Tags: latex
Slug: sharing-a-preprint-using-acmart
Authors: Micah Smith

Congratulations! You just submitted a paper to an ACM conference. While you are waiting to receive peer reviews, you may want to share a preprint with your colleagues.

Here's what you should *not* do -- send the exact file that you created as part of your submission. This is still anonymized, contains distracting ACM metadata in the header/footer, and does not correctly indicate that this paper is unpublished and not for distribution.

### Approach 1 - authordraft option

Instead, here is how to edit your TeX files to create and distribute a preprint that looks great.

Thanks to careful design of the `acmart` class, you can mostly just set options in your `documentclass` declaration.

Let's supposed you've submitted a paper to a conference that uses the `acmsmall` template. You might have initially declared the document class as follows:
```latex
\documentclass[acmsmall,anonymous,review]{acmart}
```

How do you convert this into a shareable preprint?

1. Remove `anonymous`. No explanation needed.
1. Add `authordraft`. This option is appropriate for "author's drafts that are not intended for distribution". It adds a watermark that says "Unpublished working draft. Not for distribution" and also enables the `review` and `timestamp` options.
1. Add `review=false` and `timestamp=false`.  These options are otherwise enabled by `authordraft`. This is personal preference, but when sending a document to colleagues, I want the reading experience to be as close as possible to as if they were viewing a published work. Thus these options will disable the red line numbers that would appear in the left margin, and remove the timestamp that would appear in the footer.
1. Add `nonacm`. This removes all ACM conference and copyright information. For the purposes of sharing with colleagues, this is just noise as you don't know that your paper will be published at any specific venue.
1. Add `screen`. This isn't usually suggested in sample submissions for some reason, but is good to add now that you can, in that the PDF is compiled for the "screen" (aka, a computer...) and hyperlinks are colorized.

Here is the final result:
```latex
\documentclass[acmsmall,screen,authordraft,nonacm,review=false,timestamp=false]{acmart}
```

### Approach 2 - preprint footer

Note that `authordraft` adds a watermark in the center of the page. If you prefer a different approach, you could instead set `authorversion`, which configures acmart to produce a version "for the author's personal use" (by adding a notice on the first page accordingly) -- this is something that would be appropriate for posting on your personal website for example.

```latex
\documentclass[acmsmall,screen,authorversion,nonacm]{acmart}
```

But you now need to indicate in another location that this a preprint. One option is to add a custom footer.

Here is one way to achieve that. The `fancyhdr` package is what is used under the hood to create headers and footers in many documents including the acmart-derived layouts. After a dive through `acmart.sty`, it turns out that we need to set our custom footer in an `AtBeginDocument` block. Otherwise, since `acmart` sets its own `fancyfoot` in an `AtBeginDocument` block, if we defined it in our own preamble it would get redefined.

```latex
\usepackage{fancyhdr}
\AtBeginDocument{%
    \addtolength{\footskip}{2.0\baselineskip}%
    \fancyfoot[L]{\textit{\textbf{Preprint --- do not distribute.}}}%
}
```

### References

- [acmart documentation](https://www.acm.org/binaries/content/assets/publications/consolidated-tex-template/acmart.pdf). See in particular section 2.3 ("Top Matter").
- [fancyhdr documentation](http://mirror.las.iastate.edu/tex-archive/macros/latex/contrib/fancyhdr/fancyhdr.pdf)
