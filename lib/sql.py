# ##################################################
# import

import sqlite3
import tempfile
import lib.util as util


# ##################################################
# database

class Database:
    _singleton = None

    @classmethod
    def singleton(cls):
        return cls._singleton or Database()

    # ##################################################
    # contructor

    def __init__(self, db_file=None):
        Database._singleton is None or util.throw('database already created! ( %s )' % Database._singleton.db_file)
        Database._singleton = self
        if db_file is not None:
            self.db_fd = None
            self.db_file = db_file
        else:
            self.db_fd, self.db_file = tempfile.mkstemp()
        print 'db [%s]' % self.db_file
        self.connection = None
        self.cursor = None

    # ##################################################
    # connect

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_file)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            # if self.db_fd is not None:
            #    os.close( self.db_fd )
            #    os.unlink( self.db_file )

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    # ##################################################
    # execute

    def execute_file(self, sql_file):
        with open(sql_file, 'r') as f:
            self.connection.cursor().executescript(f.read())
        self.connection.commit()

    def execute(self, sql):
        print sql.query
        if len(sql.args) > 0:
            self.cursor = self.connection.execute(sql.query, tuple(sql.args))
        else:
            self.cursor = self.connection.execute(sql.query)
        return self

    # ##################################################
    # commit

    def commit(self):
        self.connection.commit()
        return self

    # ##################################################
    # fetch

    def fetch_all(self, *args):
        rows = []
        for obj in self.cursor.fetchall():
            row = dict()
            for (index, arg) in enumerate(args):
                row[arg] = obj[index]
            rows.append(row)
        return rows

    def fetch_one(self, *args):
        rows = self.fetch_all(*args)
        return rows[0] if len(rows) > 0 else None


# ##################################################
# sql

class Sql:
    def __init__(self, query=None, args=None):
        self.query = query or ''
        self.args = args or []

    def execute(self):
        Database.singleton() is not None or util.throw('database not created!')
        return Database.singleton().execute(self)


class Select(Sql):
    def __init__(self, table, *args):
        Sql.__init__(self)
        self.table = table
        self.columns = args if len(args) > 0 else self.table.columns
        self.query = 'select %s from %s' % (', '.join(self.columns), self.table.name)

    def fetch_all(self):
        return self.execute().fetch_all(*self.columns)

    def fetch_one(self):
        Database.singleton() is not None or util.throw('database not created!')
        return Database.singleton().execute(self).fetch_one(*self.columns)

    def where(self, **kwargs):
        self.query = '%s where %s' % (self.query, ' and '.join('%s=?' % key for key in kwargs.iterkeys()))
        self.args = self.args + kwargs.values()
        return self

    def order_by(self, *args):
        self.query = '%s order by %s' % (self.query, ', '.join(args))
        return self


class Insert(Sql):
    def __init__(self, table, **kwargs):
        Sql.__init__(self)
        self.table = table
        self.columns = kwargs.keys()
        self.args = kwargs.values()
        keys = ', '.join(self.columns)
        values = ', '.join(['?'] * len(self.args))
        self.query = 'insert into %s ( %s ) values ( %s )' % (self.table.name, keys, values)

    def execute(self):
        Database.singleton() is not None or util.throw('database not created!')
        return Database.singleton().execute(self)


class Update(Sql):
    def __init__(self, table, **kwargs):
        Sql.__init__(self)
        self.table = table
        self.query = 'update %s set %s' % (self.table.name, ', '.join(['%s=?' % key for key in kwargs.iterkeys()]))
        self.args = kwargs.values()

    def execute(self):
        Database.singleton() is not None or util.throw('database not created!')
        return Database.singleton().execute(self)

    def where(self, **kwargs):
        self.query = '%s where %s' % (self.query, ' and '.join('%s=?' % key for key in kwargs.iterkeys()))
        self.args = self.args + kwargs.values()
        return self


class Delete(Sql):
    def __init__(self, table):
        Sql.__init__(self)
        self.table = table
        self.query = 'delete from %s' % (self.table.name)
        self.args = []

    def execute(self):
        Database.singleton() is not None or util.throw('database not created!')
        return Database.singleton().execute(self)

    def where(self, **kwargs):
        self.query = '%s where %s' % (self.query, ' and '.join('%s=?' % key for key in kwargs.iterkeys()))
        self.args = self.args + kwargs.values()
        return self


# ##################################################
# table

class Table(object):
    def __init__(self, name, *columns):
        self.name = name
        self.columns = columns

    # ##################################################
    # sql query

    def select(self, *args):
        return Select(self, *args)

    def insert(self, **kwargs):
        return Insert(self, **kwargs)

    def update(self, **kwargs):
        return Update(self, **kwargs)

    def delete(self):
        return Delete(self)


# ##################################################
# helper

def retrieve_all(table):
    return [util.Object(row['json']) for row in table.select('json').order_by('oid desc').fetch_all() if row is not None]


def search(table, oid):
    row = table.select('json').where(oid=oid).fetch_one()
    if row is None:
        return None
    return util.Object(row['json'])


def retrieve(table, oid):
    row = table.select('json').where(oid=oid).fetch_one()
    row is not None or util.throw('unknown oid ( %s )!' % oid)
    return util.Object(row['json'])


def insert(table, obj):
    table.insert(oid=obj.oid, json=obj.json).execute()
    return retrieve(table, obj.oid)


def update(table, obj):
    table.update(json=obj.json).where(oid=obj.oid).execute()
    return retrieve(table, obj.oid)


def upsert(table, obj):
    old_obj = search(table, oid=obj.oid)
    if old_obj is None:
        return insert(table, obj)
    return update(table, obj)


def delete(table, oid):
    obj = search(table, oid)
    if obj is not None:
        table.delete().where(oid=obj.oid).execute()
    return obj
