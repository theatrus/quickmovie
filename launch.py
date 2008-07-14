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

import quickmovie.model
import sqlalchemy as sa

import quickmovie.controller.main
import imdb



def create_data():
   pass
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))


    engine = sa.create_engine('sqlite:///quickmovie.sqlite')
    quickmovie.model.init(engine)

    create_data()

    cherrypy.config.update({'server.socket_host' : '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': int(sys.argv[1])})

    # Routes is broken with decodefilter :(
    #d = cherrypy.dispatch.RoutesDispatcher()
    #d.connect('', route = '', controller = quickmovie.controller.main.Main())

    #d.connect('user/login', route = 'user/login', controller = quickmovie.controller.main.Main(), action = 'login')
    #d.connect('user/logout', route = 'user/logout', controller = quickmovie.controller.main.Main(), action = 'logout')
    #d.connect('patch', route = 'patch/:action', controller = quickmovie.controller.patch.PatchController() )
    #d.connect('project', route = 'project/:id', controller = quickmovie.controller.project.ProjectController())

    gconf = {
        '/' : {
            'tools.sessions.on' : True,
            'tools.staticdir.on' : True,
            'tools.staticdir.root' : os.path.join ( current_dir, 'htdocs'),
            'tools.staticdir.dir' : '.',
            'tools.encode.on' : True,
            'tools.encode.encoding' : 'UTF-8',
            'tools.decode.on' : True,
            'tools.proxy.on' : True,
            'tools.decode.encoding' : 'UTF-8' }}
            #'request.dispatch' : d } }

    root = quickmovie.controller.main.Main()

    cherrypy.tree.mount(root, '/', config = gconf)
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
