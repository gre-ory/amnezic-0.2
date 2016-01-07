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


def retrieve():
    return lib.sql.retrieve_all(lib.db.track)

