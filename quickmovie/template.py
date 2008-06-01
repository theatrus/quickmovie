import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup

import gettext

def template(name, args):
    look = TemplateLookup(directories=['template'], output_encoding = 'utf-8')

    temp = look.get_template(name)
    args['session'] = cherrypy.session # Give cherrypy session

    t = gettext.translation('quickmovie', fallback = True)

    args['_'] = t.ugettext
    args['url'] = cherrypy.url

    return temp.render_unicode(**args)
