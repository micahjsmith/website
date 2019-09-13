Title: Trim graphics in LaTeX
Date: 2019-09-13
Category: programming
Tags: latex
Slug: trim-figure-in-latex
Authors: Micah Smith

How to trim a figure in LaTeX.

You've already inserted the figure into a `figure` environment and now want to trim excess whitespace.

Start adjusting from here:
```
\fbox{\includegraphics[clip=true, trim={0 0 0 0}, width=\linewidth]{myfigure}}
```

`fbox` is a black box around the float content so you can see where your figure ends and where the rest of the page begins. Now, adjust the numbers in the `trim` option and recompile. The four numbers represent pixels to trim off from the left, bottom, right and top of the figure. After you have trimmed your figure as close as you can to the actual content, remove the `fbox` and you are set.

Source: http://mirror.las.iastate.edu/tex-archive/macros/latex/required/graphics/grfguide.pdf
