Title: Inline markup within words in reStructuredText
Date: 2020-08-12
Category: programming
Tags: rst, docs
Slug: inline-markup-within-words-rst
Authors: Micah Smith

I often write documentation with reStructuredText and Sphinx. Sometimes I want to refer to
the plural of some programming concept, where the concept is monospace font but the plural
form is in the normal font, e.g. `list`s.

While this is easy to do in markdown:

```markdown
`list`s
```

It is less apparent in rst.

| rST markup | output | comment |
|------------|--------|---------|
|``` ``list``s ``` | \`\`list\`\`s | first attempt |
|``` ``list`` s ``` | `list` s | note the space after list, even though it's barely noticeable on my own site |
|``` ``list``\ s``` | `list`s | need to escape the space! |

**💡 The key is to escape the space after the end-string of the inline markup.**

This applies to italic font, bold font, etc. in addition to the inline literal (monospace)
blocks.

The operative part of the spec:

> Inline markup start-strings and end-strings are only recognized if the following conditions are met:

> ...

> 7\. Inline markup end-strings must end a text block or be immediately followed by

>    - whitespace,
>    - one of the ASCII characters - . , : ; ! ? \ / ' " ) ] } >
>    - or a similar non-ASCII punctuation character. [14]

Have you found another way to do this? Let me know in the comments.

Source: <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#inline-markup>
