Title: Fixing invalid argument iwhite on vimdiff
Date: 2019-11-07
Modified: 2020-03-27
Category: programming
Tags: vim, macos, catalina
Slug: fixing-vim-invalid-argument-diffopt-iwhite
Authors: Micah Smith

[Update from 2020-03-27 below]

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

```vim
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

---

### Update

I dove deeper into the source of the problem on the version of vim provided by MacOS
Catalina and I was able to identify the problem more clearly and find a solution. First, the
Catalina vim version did not drop support for iwhite. Rather, the problem is that somehow 
the default setting which includes `internal` is invalid for the version of vim installed.
Here is a log demonstrating the issue.

```
$ /usr/bin/vim -u NONE
:set diffopt?
  diffopt=internal,filler
:set diffopt+=iwhite
E474: Invalid argument: diffopt+=iwhite
:set diffopt=internal
E474: Invalid argument: diffopt=internal
:set diffopt=filler
:set diffopt+=iwhite
:set diffopt?
  diffopt=filler,iwhite
```

Summary

- stock vim with no config defaults to `diffopt=internal,filler`
- stock vim does not actually support the option `internal` (`:help diffopt` is actually
    accurate in this regard in that it is not shown as an option, though it is listed as the
    default)
- running `:set diffopt+=iwhite` semantically does `:set diffopt=internal,filler,iwhite`
    which contains an invalid option
- the error message is highly misleading suggesting that the invalid argument is `iwhite`
    when it is actually `internal`

A quick fix

- first remove `internal` from the list of options
- then add your desired options

```vim
if &diff
    set diffopt-=internal
    set diffopt+=iwhite
endif
```

My version of vim FWIW:
```
$ /usr/bin/vim --version
VIM - Vi IMproved 8.1 (2018 May 18, compiled Dec 13 2019 14:45:40)
Included patches: 1-503, 505-680, 682-1312
Compiled by root@apple.com
```
