# ##################################################
# import


import lib.util
import lib.sql
import lib.db

import lib.plugin


# ##################################################
# json


def search(query=None):
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    query is not None or lib.util.throw('missing query!')
    return lib.plugin.source.search(query)


def search_by_oid(oid=None):
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    oid is not None or lib.util.throw('missing track oid!')
    return lib.plugin.source.track(oid)


def retrieve_all():
    return lib.sql.retrieve_all(lib.db.track)


def create(oid):
    return update(oid)


def retrieve(oid):
    oid is not None or lib.util.throw('missing oid!')
    return lib.sql.retrieve(lib.db.track, oid)


def update(oid):
    lib.plugin.source is not None or lib.util.throw('missing track source!')
    oid is not None or lib.util.throw('missing oid!')
    obj = lib.plugin.source.track(oid)
    obj is not None or lib.util.throw('track %s not found!' % oid)
    obj.loaded = True
    return lib.sql.upsert(lib.db.track, obj)


def delete(oid):
    return lib.sql.delete(lib.db.track, oid)



