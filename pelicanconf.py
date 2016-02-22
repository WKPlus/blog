#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'WKPlus'
SITENAME = u'\u4e03\u96f6\u516b\u843d'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

THEME_PATH = '/var/www/pelican/pelican-themes/'
THEME = THEME_PATH + 'pelican-bootstrap3'
#THEME = THEME_PATH + 'nmnlist'

DEFAULT_PAGINATION = 10
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

