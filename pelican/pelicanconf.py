#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

#AUTHOR = 'Andrey Novikov'
SITENAME = 'Andrey Novikov'
SITEURL = ''

PATH = 'content'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['tag_cloud','summary','sitemap']

MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra','del_ins']

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

STATIC_PATHS = ['cars','travel']

SUMMARY_MAX_LENGTH = 120

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Androzic', 'http://androzic.com/'),
         ('Xpoint', 'http://xpoint.ru/user/1'),
         ('ФРИ', 'http://ezhe.ru/fri/527/'),)

# Social widget
SOCIAL = (('google-plus', 'https://plus.google.com/100618994892995632809'),
          ('facebook', 'http://www.facebook.com/andrey.g.novikov'),
          ('twitter', 'http://twitter.com/andreynovikov'),
          ('youtube', 'http://www.youtube.com/profile?user=novikovandrey'),
          ('flickr', 'http://www.flickr.com/photos/andreynovikov/'),
          #('panoramio', 'http://www.panoramio.com/user/725010'),
          ('github', 'http://github.com/andreynovikov'),
          ('stack-overflow', 'http://stackoverflow.com/users/488489/andrey-novikov'),)

DEFAULT_PAGINATION = 5

SITEMAP = {'format': 'xml',
           'priorities': {
               'articles': 0.3,
               'indexes': 0.5,
               'pages': 1.0
           },
           'changefreqs': {
               'articles': 'monthly',
               'indexes': 'weekly',
               'pages': 'yearly'
           }
}

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'html5up-striped'

PROFILE_IMG_URL = 'https://secure.gravatar.com/avatar/b829de587134a496f79b4152f5561b61?s=100'
COPYRIGHT = '<a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a><br/>by Andrey Novikov unless otherwise marked'
