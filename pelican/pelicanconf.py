#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

#AUTHOR = 'Andrey Novikov'
SITENAME = 'Andrey Novikov'
SITEURL = 'http://andreynovikov.info'

PATH = 'content'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['tag_cloud','summary']

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'ru'

STATIC_PATHS = ['cars']

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

#DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'html5up-striped'

PROFILE_IMG_URL = 'https://secure.gravatar.com/avatar/b829de587134a496f79b4152f5561b61?s=100'
COPYRIGHT = 'Andrey Novikov'
DISQUS_SITENAME = 'andreynovikov-info'