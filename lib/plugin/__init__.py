
# ##################################################
# source


source = None


# ##################################################
# interface


class Source(object):

    def __init__(self):
        pass

    def search(self, query):
        return []

    def track(self, oid):
        return None

    def artist(self, oid):
        return None

    def genre(self, oid):
        return None
