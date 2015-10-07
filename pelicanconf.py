#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Petr Kalmykov'
SITENAME = 'Astro blog'
SITEURL = ''

PLUGIN_PATHS = ['plugins',]
PLUGINS = [
	'sitemap', 
	'tag_cloud', 
#	'related_posts', 
	'tipue_search',
	'extract_toc',
]

SITEMAP = {
	'format' : 'xml',
	'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

THEME = 'themes/pelican-bootstrap3'
PATH = 'content'
STATIC_PATHS = ['images',]

TIMEZONE = 'Asia/Novosibirsk'

DEFAULT_LANG = 'ru'
DEFAULT_METADATA = {
    'status': 'draft',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         )

# Social widget
SOCIAL = (('github','https://github.com/StonedAstronaut'),
          ('google-plus', 'https://plus.google.com/u/0/113483139834962824849/posts'),
          ('rss','/feeds/all.atom.xml'),
          )

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True

DEFAULT_PAGINATION = 10

# AVATAR = 'images/profile.png'
# ABOUT_ME = '<b>I am Astro</b>'

DISPLAY_CATEGORIES_ON_MENU = False

DISPLAY_ARTICLE_INFO_ON_INDEX = True

FAVICON = 'images/favicon.png'

GOOGLE_ANALYTICS = 'UA-43336913-2'

# GITHUB_URL = 'https://github.com/StonedAstronaut'
# GITHUB_USER = 'StonedAstronaut'
# GITHUB_REPO_COUNT = True
# GITHUB_SHOW_USER_LINK = True

PDF_GENERATOR = False

DIRECT_TEMPLATES = (('index', 'categories', 'authors', 'archives', 'search'))

# DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
# RELATED_POSTS_MAX = 10
# PYGMENTS_STYLE = 'emacs'

MD_EXTENSIONS = (['toc', 'codehilite(css_class=highlight)', 'extra'])

# NAVBAR_ELEMENTS = ['search']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
