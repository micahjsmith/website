#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import datetime

AUTHOR = 'Micah Smith'
SITENAME = 'Micah Smith'
SITEURL = 'http://localhost:8000'
SITELOGO = '/images/micah.jpg'
SITETITLE = 'Micah J. Smith'
COPYRIGHT_NAME = 'Micah Smith'
COPYRIGHT_YEAR = datetime.date.today().year
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

PATH = 'content'

# Theme
THEME = 'themes/Flex/'
CUSTOM_CSS = 'static/custom.css'
DISABLE_URL_HASH = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Main page
MAIN_MENU = False
DISPLAY_PAGES_ON_MENU = True
PAGES_SORT_ATTRIBUTE = 'order'

INDEX_URL = 'blog'
INDEX_SAVE_AS = 'blog/index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'

# drafts
DRAFT_URL = 'blog/drafts/{slug}'
DRAFT_SAVE_AS = 'blog/drafts/{slug}/index.html'
DRAFT_PAGE_URL = 'drafts/{slug}'
DRAFT_PAGE_SAVE_AS = 'drafts/{slug}/index.html'

# Blogroll
# LINKS = (('blog', '/blog.html'),)

# Social widget
GITHUB_URL = 'https://github.com/micahjsmith'
TWITTER_USERNAME = 'micahjsmith'
SOCIAL = (
    ('twitter', 'https://twitter.com/micahjsmith'),
    ('github', 'https://github.com/micahjsmith'),
    ('stack-overflow', 'https://stackoverflow.com/users/2514228/micah-smith'),
    ('linkedin', 'https://www.linkedin.com/in/micahjsmith'),
    ('key', 'https://keybase.io/micahjsmith'), # use fa-key for keybase.io
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Plugins
PLUGIN_PATHS = ['plugins', 'plugins/pelican-embed-tweet']
PLUGINS = ['render_math', 'embed_tweet']
JINJA_ENVIRONMENT = {}

# Static content
STATIC_PATHS = ['extra', 'images', 'files', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/CNAME': { 'path' : 'CNAME' },
    'extra/custom.css': {'path': 'static/custom.css'},
}

# Flex

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
