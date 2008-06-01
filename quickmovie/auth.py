import cherrypy

# Cheap auth layer

def user_valid():
    if 'user' in cherrypy.session:
        if cherrypy.session['user'] is not None:
            return True
    return False
