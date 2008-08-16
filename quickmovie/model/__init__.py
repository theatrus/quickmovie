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

import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types

from quickmovie.model import meta


def init(bind):
    meta.engine = bind
    meta.Session = orm.scoped_session(
        orm.sessionmaker(transactional = True, autoflush = True, bind = bind))
    meta.metadata.create_all(bind=meta.engine)

    load_orm()

def load_orm():
    orm.mapper(Plot, plots_table)
    orm.mapper(Movie, movies_table, properties={
        'plots': orm.relation(Plot)
        })


plots_table = sa.Table('plots', meta.metadata,
                       sa.Column('id', sa.Integer, primary_key = True),
                       sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.id')),
                       sa.Column('pick', sa.Boolean),
                       sa.Column('plot', sa.Unicode(600)))


movies_table = sa.Table('movies', meta.metadata,
                        sa.Column('id', sa.Integer, primary_key = True),
                        sa.Column('name', sa.Unicode(200)),
                        sa.Column('filename', sa.Unicode(300)),
                        sa.Column('length', sa.Unicode(100)),
                        sa.Column('imdb_id', sa.Unicode(100)),
                        sa.Column('rating', sa.Float),
                        sa.Column('taglines', sa.Unicode(500)),
                        sa.Column('year', sa.Integer),
                        sa.Column('genres', sa.Unicode(500)),
                        sa.Column('imageurl', sa.Unicode(200)))

class Movie(object):
    pass

class Plot(object):
    pass
