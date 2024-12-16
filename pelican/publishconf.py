# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://andreynovikov.info'
RELATIVE_URLS = False

# FEED_ALL_ATOM = "feeds/all.atom.xml"
# CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = 'andreynovikov-info'
GOOGLE_SITE_VERIFICATION = 'Kpb-e90rCCQ-TI7guNhsEwANcizR07Hd2ddV7zvEn9Q'
ANALYTICS = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HVMCJLW9LT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-HVMCJLW9LT');
</script>
"""
