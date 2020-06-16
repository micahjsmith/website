Title: Hidden Icon? files on macOS
Date: 2020-06-15
Category: programming
Tags: macos
Slug: hidden-icon-files-macos-gdrive
Authors: Micah Smith

For a while I've tolerated files named `Icon?` that appear in my console `ls` and `git status` output on macOS as well as in some IDE file trees like in Atom:

```text
$ \ls -Al
total 696
-rw-------  1 micahsmith  staff  179 Nov 12  2019 Experiment Datasets.gsheet
-rw-r--r--@ 1 micahsmith  staff    0 Nov  2  2018 Icon?
-rw-------  1 micahsmith  staff  179 Aug 19  2018 test_20180818193120513976.gsheet
-rw-------  1 micahsmith  staff  179 Nov 12  2019 test_20180818193120513976_v1.gsheet
```

Why does the file `Icon?` appear and what is responsible for creating it? There is a nice discussion I found [on superuser](https://superuser.com/q/298785). The short answer is that in my case, the Google Drive desktop client ("Backup and Sync") for MacOS takes advantage of built-in Finder functionality to use a special icon for folders that are shared in Drive. The file that appears as `Icon?` [is actually](https://superuser.com/a/298798) a "hidden file" with the icon image itself stored in a non-empty "resource fork".

Though the Superuser answer does not expand on this, the reason the literal carriage return character appears as a `?` is because the default behavior of `ls` is equivalent to `ls -q` which sets:

> Force printing of non-graphic characters in file names as the character '?'

I don't care about these details and I appreciate the integration with Drive, Dropbox, etc. with Finder. But I don't want these to show up in my console output.

### Ignoring `Icon?` files in `git status`

Add to your global gitignore in `~/.gitignore`:

```text
Icon[^M]
```

Gitignore uses [fnmatch](https://docs.python.org/3/library/fnmatch.html) syntax[^1], so to match a literal carriage return character it can be enclosed within square brackets. To enter the literal carriage return character into Vim, for example, I use <kbd>Ctrl</kbd> <kbd>k</kbd> <kbd>C</kbd> <kbd>R</kbd> (see `:help digraphs` and  `:help digraph-table`) which then appears as `^M`.[^2]

If you entered the literal `Icon?` into a `.gitignore` file, it would also hide this file, but only by accident, because the `?` pattern matches any character, so the pattern would also match `Iconz` for example.

### Ignoring `Icon?` files in `ls -A`

I couldn't figure out how to do this easily from `man ls` by modifying any `ls` aliases I have. But I decided that I can tolerate this as long as it does not show up in in `git status` output. Let me know if you figure out a good way to do this!

[^1]: this is not the relevant fnmatch library but is a helpful reference
[^2]: In this code snippet we instead have literal characters <kbd>^</kbd> <kbd>M</kbd>, so copy and pasting will not work.
