#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Micah Smith"
SITENAME = "Micah Smith"
SITEURL = "http://localhost:8000"
SITELOGO = SITEURL + "/images/micah.jpg"
SITETITLE = "Micah J. Smith"
COPYRIGHT_YEAR = 2016

PATH = "content"

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

# Theme
THEME = "flex"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Main page
MAIN_MENU = True
DISPLAY_PAGES_ON_MENU = True

MENUITEMS = (("Blog", "/blog.html"),
             ("Archives", "/archives.html"),
             ("Categories", "/categories.html"),
             ("Tags", "/tags.html"),)

INDEX_SAVE_AS = "blog.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
ARTICLE_URL = "blog/{date:%Y}/{date:%m}/{slug}/"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%m}/{slug}/index.html"

# Blogroll
# LINKS = (("blog", "/blog.html"),)

# Social widget
GITHUB_URL = "https://github.com/micahjsmith"
TWITTER_USERNAME = "micahjsmith"
SOCIAL = (("twitter", "https://twitter.com/micahjsmith"),
          ("github", "https://github.com/micahjsmith"),
          ("stack-overflow", "https://stackoverflow.com/users/2514228/micah-smith"),
          ("linkedin", "https://www.linkedin.com/in/micahjsmith"))

DEFAULT_PAGINATION = False
PLUGIN_PATHS = ["./pelican-plugins"]


# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
