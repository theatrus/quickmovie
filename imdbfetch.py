#!/usr/bin/env python
# Copyright (c) 2008 Yann Ramin
# This file is part of quickmovie.
#
# quickmovie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quickmovie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with quickmovie.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append('.')

import os

import cherrypy

from quickmovie.model import meta
from quickmovie.model import Movie, Plot
import quickmovie.model

import sqlalchemy as sa

import quickmovie.controller.main
import imdb
import re

import urllib2

def fetch_cover(inurl, outfile):
    print "    Trying to fetch",inurl
    filein = urllib2.urlopen(inurl)
    fileout = open(outfile, 'w')
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
    return outfile



def store_plot(rawplot, movie):

    plot = u"".join(rawplot)
    rplot = re.search('(.*)::(.*)', plot)
    plot = rplot.group(1)

    found = False

    for existing_plot in movie.plots:
        if plot == existing_plot.plot:
            found = True

    if found == False:
        print "   Fetched a plot"
        po = Plot()

        po.plot = plot
        po.pick = False
        movie.plots.append(po)
        meta.Session.add(po)



def store_plots(iamovie, movie):
    if iamovie.has_key('plot'):
        for rawplot in iamovie['plot']:
            store_plot(rawplot, movie)
    else:
        store_plot(u"No plots found.", movie)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))


    engine = sa.create_engine('sqlite:///quickmovie.sqlite')
    quickmovie.model.init(engine)
    print "Running quickmovie scanner"

    for dirpath, dirnames, filenames in os.walk(sys.argv[1]):

        for file in filenames:
            file = file.lower()
            if file[-3:] != 'iso' and file[-3:] != 'avi':
                continue

            rawfile = unicode(file)
            print rawfile
            m = None

            r = meta.Session.query(Movie).filter_by(filename = rawfile).all()
            if len(r) > 0:
                print "Already in DB, going to update",rawfile
                m = r[0]

            print rawfile

            file = file[:-4] # Crude extension strip
            file = file.replace("_", " ")

            ia = imdb.IMDb()
            iares = ia.search_movie(file)
            if len(iares) == 0:
                continue
            iamovie = iares[0]
            ia.update(iamovie)
            ia.update(iamovie, 'plot')
            # Try to fix broken consoles without unicode - force to ascii

            print file, u'->', iamovie['title'].encode('ascii', 'replace')

            try:
                if m == None:
                    m = Movie() # Make a new movie
                m.name = iamovie['title']
                m.filename = rawfile
                m.imdb_id = unicode(iamovie.getID())
                m.year = int(iamovie['year'])

                # Fetch cover
                cover_url = os.path.sep + 'covers' + os.path.sep + m.imdb_id + '.jpg'

                if not iamovie.has_key('cover url'):
                    print "   Couldn't fetch cover art"
                    m.imageurl = u'nocover.jpg'
                else:
                    fetch_cover(iamovie['cover url'], 'htdocs' + os.path.sep + cover_url)
                    m.imageurl = cover_url

                m.genres = iamovie['genres'][0]
                m.length = iamovie['runtimes'][0]
                if iamovie.has_key('taglines'):
                    ia.update(iamovie, 'taglines')
                    m.taglines = u"".join(iamovie['taglines'])
                m.rating = float(iamovie['rating'])



                # Look for existing plots
                store_plots(iamovie, m)

                try:
                    meta.Session.add(m)
                except:
                    pass
                finally:
                    meta.Session.commit()

            except Exception,e:
                print "Exception while processing IMDB request",e


if __name__ == '__main__':
    main()
