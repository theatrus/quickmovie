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

    cherrypy.server.quickstart()
    cherrypy.engine.start()



if __name__ == '__main__':
    main()
