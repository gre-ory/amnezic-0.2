# ##################################################
# import


import lib.util
import lib.sql
import lib.db

import lib.plugin


# ##################################################
# category


CATEGORY_GENRE = 'genre'
CATEGORY_ARTIST = 'artist'
CATEGORY_YEAR = 'year'


# ##################################################
# json


def retrieve_all():
    return lib.sql.retrieve_all(lib.db.theme)


def retrieve(oid):
    oid is not None or lib.util.throw('missing theme oid!')
    return lib.sql.retrieve(lib.db.theme, oid)


def create_genre(oid):
    oid is not None or lib.util.throw('missing genre oid!')
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    obj = lib.plugin.source.genre(oid)
    obj is not None or lib.util.throw('unknown genre!')
    obj.category = CATEGORY_GENRE
    return lib.sql.insert(lib.db.theme, obj)


def create_artist(oid):
    oid is not None or lib.util.throw('missing artist oid!')
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    obj = lib.plugin.source.artist(oid)
    obj is not None or lib.util.throw('unknown artist!')
    obj.category = CATEGORY_ARTIST
    return lib.sql.insert(lib.db.theme, obj)


def create_year(oid):
    oid is not None or lib.util.throw('missing year oid!')
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    obj = lib.plugin.source.artist(oid)
    obj is not None or lib.util.throw('unknown year!')
    obj.category = CATEGORY_YEAR
    return lib.sql.insert(lib.db.theme, obj)

def update(obj):
    obj is not None or lib.util.throw('missing theme!')
    obj.oid is not None or lib.util.throw('missing theme oid!')
    old = retrieve(obj.oid)
    obj.name = obj.name or old.name or lib.util.throw('missing theme name!')
    obj.tracks = old.tracks or []
    return lib.sql.update(lib.db.theme, obj)


def add_track(oid, track_oid):
    oid is not None or lib.util.throw('missing oid!')
    track_oid is not None or lib.util.throw('missing track oid!')
    obj = retrieve(oid)
    if track_oid not in obj.tracks:
        obj.tracks.append(track_oid)
    return lib.sql.update(lib.db.track, obj)


def remove_track(oid, track_oid):
    oid is not None or lib.util.throw('missing oid!')
    track_oid is not None or lib.util.throw('missing track oid!')
    obj = retrieve(oid)
    if track_oid not in obj.tracks:
        obj.tracks.append(track_oid)
    return lib.sql.update(lib.db.track, obj)


def delete(oid):
    oid is not None or lib.util.throw('missing theme oid!')
    return lib.sql.delete(lib.db.theme, oid)
