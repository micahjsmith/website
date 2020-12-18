Title: Using vimdiff with dumb paths
Date: 2016-02-02
Category: programming
Tags: vim, git, matlab
Slug: vim-diff-dumb-paths

I've been loving vimdiff as my git difftool for a while.

## Vimdiff and Matlab packages

Vimdiff runs into some problems when working with Matlab code. Matlab considers
directories with names beginning with `+` as "packages", a natural way to organize
projects. However, this means that many paths relative to the git top-level directory begin
with `+`. Of course, this applies to any path beginning with a `+`, though this is otherwise an
uncommon naming convention.

Suppose that your project looks like this:
```
+code/
  foo.m
  bar.m
```

You might want to use vim to diff your two files:
```bash
vimdiff +code/foo.m +code/bar.m
```

But vim will tell you:
```
Error detected while processing command line:
E492: Not an editor comamnd: code/foo.m
E492: Not an editor comamnd: code/bar.m
```

What's going on? Vim interprets `+` as the start of a command-line argument (beyond
the typical `-`) and fails to find options/commands called `code/foo.m` and `code/bar.m`.

## The vimdiff solution

Simply tell vimdiff somehow that the paths you are specifying are not options. (By the way,
note that vimdiff is pretty much just an alias for `vim -d`.)

We could prefix them with the current directory:
```
vimdiff ./+code/foo.m ./+code/bar.m
```

Better yet, note that the `--` option
>Denotes the end of the options.  Arguments after this will be handled as
>a file  name. This can be used to edit a filename that starts with a '-'.

Or, in our case, to edit a filename that starts with a `+`:
```
vimdiff -- +code/foo.m +code/bar.m
```

## Bringing git into the picture

We now update `+code/foo.m` and want to compare to the previous commit. Using git's
`difftool` command, we diff all modified git-tracked files using a tool of our choice:
```
git difftool --tool=vimdiff
```

Unfortunately, we run into the same problem as before.
```
"/private/var/folders/7v/cjvpqzt57c5fsb7qvsjmm5sw0000gn/T/7i6IKG_foo.m" [readonly] 1L, 6C
Error detected while processing command line:
E492: Not an editor comamnd: code/foo.m
```

Since you haven't specified the file names yourself, you can't use either of the solutions
from the previous section!

## The git solution

Git is basically writing the "before" state of the file to a temporary location and invoking
a typical vimdiff command. If we can modify this command, we can use one of our solutions
above.

One possibility is to set git's `difftool.<tool>.cmd` config option:
>Specify the command to invoke the specified diff tool. The specified command is evaluated in
>shell with the following variables available: LOCAL is set to the name of the temporary file
>containing the contents of the diff pre-image and REMOTE is set to the name of the temporary
>file containing the contents of the diff post-image.

We can do
```
git config --global difftool.vimdiff.cmd 'vimdiff -- $LOCAL $REMOTE'
```

That'll do it. While you're at it, why not update your `~/.gitconfig` with the following handy
diff-related settings:
```
[alias]
	d   = difftool
[diff]
	tool = vimdiff
[difftool]
	prompt = false
[difftool "vimdiff"]
	cmd = vimdiff -- $LOCAL $REMOTE
```

Most people will likely never come across this problem: none of their paths are this crazy,
they use a different (read: graphical) difftool, they even use an external diff wrapper.
But this simple solution is all I need.
