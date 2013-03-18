#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, re
import magic
import simplejson as json
import MySQLdb
from webob import Request, Response
from webob.exc import HTTPNoContent

import wsgiref.handlers

THUMBNAIL_HEIGHT = 120

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

def bool(value):
    if str(value).lower() in ("yes", "y", "true", "t", "1"): return True
    return False

def connectDB():
    return MySQLdb.connect(user='novikov', passwd='anNo', db='novikov', use_unicode=True, charset='utf8')

def loadSession(sessionId):
    path = '/www/com.novikov.andrey/tmp/sess'
    session = {'user': None}
    if sessionId == None:
        return session
    try:
        with open(''.join([path, '/', sessionId])) as f:
            for line in f:
                (key, val) = line.strip().split('=', 1)
                session[key] = val
    except IOError:
        print >> sys.stderr, "Now session with id %s" % sessionId
    return session

def image(request, imageId):
    response = Response(content_type='text/plain', charset='utf-8')

    db = connectDB()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('''SELECT id, name, bundle, description FROM gallery_image WHERE id = %s''', (imageId))

    image = cursor.fetchone()
    image['path'] = ''.join(['/galleries', image['bundle'], '/', image['name']])
    del image['bundle']

    # Get rating
    cursor.execute('''SELECT AVG(rating) AS average FROM gallery_image_rating WHERE image = %s GROUP BY image''', (imageId))
    rating = cursor.fetchone()
    if rating != None:
        image['rating'] = rating

    # Get labels
    cursor.execute('''SELECT id, name FROM gallery_label INNER JOIN gallery_label_image ON (label = id AND image = %s)''', (imageId))
    labels = cursor.fetchall()
    if labels != None:
        image['labels'] = labels

    session = loadSession(request.cookies.get('sess', None))
    userId = session['user']
    if userId != None:
        cursor.execute('''INSERT INTO gallery_image_log VALUES(%s, %s, 5, NOW())''', (imageId, userId))
        db.commit()

    cursor.close()
    response.text = json.dumps(image, indent=4, ensure_ascii=False)
    return response

def makeThumbnail(path, force = False):
    # Construct path to thumbnail and return it if file exists
    tpath = re.sub(r'\/([^\/]+)$', r'/thumbs/t-\1', path)
    if os.path.isfile(tpath) and force == False:
        return tpath
    # Create directory if it not exists
    tdir = os.path.dirname(tpath)
    if not os.path.isdir(tdir):
        os.makedirs(tdir, 0750)
    # Rescale and save image
    from wand.image import Image
    with Image(filename=path) as image:
        ox = image.width
        oy = image.height
        ny = THUMBNAIL_HEIGHT
        nx = ox * ny / oy
        image.resize(width=nx, height=ny)
        image.strip()
        if os.path.isfile(tpath):
            os.remove(tpath)
        image.save(filename=tpath)
    # Return path to thumbnail
    return tpath

def thumbnail(request, imageId):
    response = Response()
    # cache for one month
    response.cache_expires(2592000)

    db = connectDB()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('''SELECT name, bundle FROM gallery_image WHERE id = %s''', (imageId))
    image = cursor.fetchone()
    path = ''.join([request.environ['DOCUMENT_ROOT'], '/galleries', image['bundle'], '/', image['name']])
    tpath = makeThumbnail(path, bool(request.params.get('force', None)))
    thumb = open(tpath, 'rb')
    buffer = thumb.read()
    thumb.close()

    session = loadSession(request.cookies.get('sess', None))
    userId = session['user']
    if userId != None:
        cursor.execute('''INSERT INTO gallery_image_log VALUES(%s, %s, 4, NOW())''', (imageId, userId))
        db.commit()
    cursor.close()

    ms = magic.open(magic.MAGIC_MIME)
    ms.load()
    response.content_type = ms.buffer(buffer)
    response.charset = None
    response.body = buffer

    return response

def log(request, imageId):
    db = connectDB()
    cursor = db.cursor()
    session = loadSession(request.cookies.get('sess', None))
    userId = session['user']
    if userId != None:
        status = request.params.get('status', 1)
        cursor.execute('''INSERT INTO gallery_image_log VALUES(%s, %s, %s, NOW())''', (imageId, userId, status))
        db.commit()
    cursor.close()
    response = HTTPNoContent()
    response.cache_expires(0)
    return response

def application(environ, start_response):
    request = Request(environ)

    action = request.params.get('action', None)
    imageId = request.params.get('id', None)

    for case in switch(action):
        if case('image'):
            response = image(request, imageId)
            break
        if case('thumbnail'):
            response = thumbnail(request, imageId)
            break
        if case('log'):
            response = log(request, imageId)
            break
        if case('env'):
            response = Response(content_type='text/plain', charset='utf-8')
            parts = []
            for name, value in sorted(request.environ.items()):
                parts.append(u'%s: %r' % (name, value))
            response.text = u'\n'.join(parts)
            break
        if True:
            response = Response(content_type='text/plain', charset='utf-8')
            response.text = u'Unknown action'

    response.headers['Access-Control-Allow-Origin'] = 'http://andreynovikov.info'
    response.cache_control.private = True
    response.vary = ['Cookie']
    #print >> sys.stderr, response
    #for name, value in response.headerlist:
    #    print >> sys.stderr, '%s: %s' % (name, value)

    return response(environ, start_response)

if __name__ == '__main__':
    wsgiref.handlers.CGIHandler().run(application)
