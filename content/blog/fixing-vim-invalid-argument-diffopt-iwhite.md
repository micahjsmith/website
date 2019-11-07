Title: Fixing invalid argument iwhite on vimdiff
Date: 2019-11-07
Category: programming
Tags: vim, macos, catalina
Slug: fixing-vim-invalid-argument-diffopt-iwhite
Authors: Micah Smith

Vim's diff mode is a lightweight diffing tool that can be used at the command line, in particular with the `git diff` command. In a [previous post]({filename}/blog/vim-diff-with-plus.md), I wrote about configuring vimdiff as the git difftool for use with Matlab development (yes, way back when I was actually writing Matlab code).

Recently, I've been getting errors using vimdiff of the following (showing manual invocation rather than through `git diff`):

```
$ vimdiff
Error detected while processing /Users/micahsmith/.vimrc:
line   65:
E474: Invalid argument: diffopt+=iwhite
Press ENTER or type command to continue
```

The corresponding section of my .vimrc file is as follows:

```vimscript
"Ignore whitespace with vimdiff
if &diff
    set diffopt+=iwhite
endif
```

Had a new version of vim been released that deprecated this `diffopt` option? No, `iwhite` still appeared in the manual under `:help diffopt`. This error was driving me crazy, as when I ran `git diff` when there were many changed files, this error message would display for me to acknowledge between every file comparison.

After beating my head against the wall for a while, I finally figured out the issue. Most of my frustration is environment specific, but it does seem like MacOS Catalina bundled a different version of vim that removed support for the `iwhite` option. I'm not going to dive into it too thoroughly, but if you confirm that Catalina is to blame, let me know in the comments.

I don't use the system version of vim anyway, instead using [MacVim](https://macvim-dev.github.io/macvim/) installed using Homebrew Cask. So why was this causing me problems? I realized that I had been using an alias to invoke MacVim from the terminal but that my alias did not capture invocation of the form `vimdiff` which used the system `vim`. Uninstall MacVim and reinstalling it caused it to re-install symlinks including `/usr/local/bin/vim`, a command that did not exist as such when I originally installed MacVim.

### Before

- `vim` aliased to `/usr/bin/local/mvim` in `~/.bashrc`
- `git difftool` set to `vimdiff` which pointed to system `/usr/bin/vim` and was unaffected by `vim` alias
- upgrade to MacOS Catalina involved upgrade of system `vim` which dropped support for `iwhite`

### After

- re-install MacVim (`brew cask zap macvim && brew cask install macvim`) which created a symlink at `/usr/local/bin/vim`
- deleted `vim` alias in `~/.bashrc` as `/usr/local/bin` already higher on my `$PATH` than `/usr/bin`
- `git difftool` set to `vim -d` (equivalent to vimdiff but hopefully less likely to cause future path issues)
