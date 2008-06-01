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
    orm.mapper(Movie, movies_table)





movies_table = sa.Table('movies', meta.metadata,
                        sa.Column('id', sa.Integer, primary_key=True),
                        sa.Column('name', sa.Unicode(200)),
                        sa.Column('filename', sa.Unicode(300)),
                        sa.Column('length', sa.Unicode(100)),
                        sa.Column('imdb_id', sa.Unicode(100)),
                        sa.Column('rating', sa.Float),
                        sa.Column('plot', sa.Unicode(500)),
                        sa.Column('taglines', sa.Unicode(500)),
                        sa.Column('year', sa.Integer),
                        sa.Column('genres', sa.Unicode(500)),
                        sa.Column('imageurl', sa.Unicode(200)))

class Movie(object):
    pass

