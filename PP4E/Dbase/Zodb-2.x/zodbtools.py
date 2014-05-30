class FileDB:
    "automate zodb connect and close protocols"
    def __init__(self, filename):
        from ZODB import FileStorage, DB
        self.storage = FileStorage.FileStorage(filename)
        db = DB(self.storage)
        connection = db.open()
        self.root = connection.root()
    def commit(self):
        import transaction
        transaction.commit()               # get_tansaction() deprecated
    def close(self):
        self.commit()
        self.storage.close()
    def __getitem__(self, key):
        return self.root[key]              # map indexing to db root
    def __setitem__(self, key, val):
        self.root[key] = val               # map key assignment to root
    def __getattr__(self, attr):
        return getattr(self.root, attr)    # keys, items, values
