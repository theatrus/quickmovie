import sys
sys.path.append('.')

import os

import cherrypy

from quickmovie.model import meta
from quickmovie.model import Movie
import quickmovie.model

import sqlalchemy as sa

import quickmovie.controller.main
import imdb
import re

import urllib2

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))


    engine = sa.create_engine('sqlite:///quickmovie.sqlite')
    quickmovie.model.init(engine)

    for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
        for file in filenames:
            file = file.lower()
            if file[-3:] != 'iso':
                continue

            rawfile = unicode(file)
            
            r = meta.Session.query(Movie).filter_by(filename = rawfile).all()
            if len(r) > 0:
                print "Already in DB",rawfile
                continue

            print rawfile

            file = file[:-4]
            file = file.replace("_", " ")

            ia = imdb.IMDb()
            iares = ia.search_movie(file)
            iamovie = iares[0]
            ia.update(iamovie)
            
            # Try to fix broken consoles without unicode - force to ascii

            print file, u'->', iamovie['title'].encode('ascii', 'replace')
            try:
                m = Movie()
                m.name = iamovie['title']
                m.filename = rawfile
                m.imdb_id = unicode(iamovie.getID())
                m.year = int(iamovie['year'])

                # Fetch cover
                cover_url = '/covers/'+m.imdb_id+'.jpg'

                filein = urllib2.urlopen(iamovie['cover url'])
                fileout = open('htdocs/covers/'+m.imdb_id+'.jpg', 'w')
                while True:
                    try:
                        bytes = filein.read(1024)
                        fileout.write(bytes)
                    except IOError, (errno, strerror):
                        print "IOERROR!"
                    if bytes == "":
                        break
                filein.close()
                fileout.close()
                        
                

                m.imageurl = cover_url
                m.genres = iamovie['genres'][0]
                m.length = iamovie['runtimes'][0]
                if iamovie.has_key('taglines'):
                    ia.update(iamovie, 'taglines')
                    m.taglines = u"".join(iamovie['taglines'])
                m.rating = float(iamovie['rating'])
                plot = u"".join(iamovie['plot'][0])
                rplot = re.search('(.*)::(.*)', plot)
                m.plot = rplot.group(2)
                
                meta.Session.save(m)
                meta.Session.commit()
            except Exception,e:
                print "Exception",e


if __name__ == '__main__':
    main()
