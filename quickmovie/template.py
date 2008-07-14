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
