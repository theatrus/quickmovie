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

import cherrypy
from quickmovie.template import template
from quickmovie.model import meta

from quickmovie.model import Movie

class Main(object):

    @cherrypy.expose
    def plot(self, movie):
        m = meta.Session.query(Movie).filter_by(id = movie)[0]
        return m.plots[0].plot

    @cherrypy.expose
    def index(self, images = True, plot = False, genre = "All", filter="Filter"):
        t = {}
        t['movies'] = meta.Session.query(Movie).order_by(Movie.name)
	t['genres'] = meta.Session.query(Movie.genres).distinct();
        t['images'] = images
        t['plot'] = plot
	t['genre'] = genre
        meta.Session.commit()
        return template('index.html', t)
