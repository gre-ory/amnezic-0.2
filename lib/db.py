# ##################################################
# import

import lib.sql as sql

# ##################################################
# configure

FILE = 'db/amnezic.sqlite'
SCHEMA = 'sql/schema.sql'

# ##################################################
# table

theme = sql.Table('theme', 'oid', 'json')
track = sql.Table('track', 'oid', 'json')
game = sql.Table('game', 'oid', 'json')
player = sql.Table('player', 'oid', 'json')
