"""Perform SQL on namedtuple objects.
"""
from collections import namedtuple
import sqlite3


class SqlNt():
    def __init__(self, globals_dict):
        self._global_objects = globals_dict
        self._nt_objects = self._get_global_nts()
        self._db = self._init_db()
        self._curs = self._db.cursor()
        self._create_tables()

    # def __repr__(self):
    #     print(self.results)

    def __del__(self):
        self._teardown_db()

    def _init_db(self):
        db = sqlite3.connect(":memory:")
        return db

    def _create_tables(self):
        for nt_name, nt in self._nt_objects.items():
            if isinstance(nt, list):
                fields = nt[0]._fields
            else:
                fields = nt._fields
            create_sql = "create table {} (".format(nt_name)
            insert_sql = "insert into {} values (".format(nt_name)
            for column in fields:
                create_sql += "{},".format(column)
                insert_sql += "?,"
            create_sql = "{});".format(create_sql[:-1])
            insert_sql = "{});".format(insert_sql[:-1])
            self._curs.execute(create_sql)
            self._insert_tables(insert_sql, nt)
            self._db.commit()

    def _insert_tables(self, sql, nt):
        if isinstance(nt, list):
            for row in nt:
                values = tuple(row)
                self._curs.execute(sql, values)
        else:
            values = tuple(nt)
            self_curs.execute(sql, values)

    def _teardown_db(self):
        self._curs.close()
        self._db.close()

    def _get_global_nts(self):
        global_objects = dict(self._global_objects)
        nt_dict = dict()
        for obj_name, obj_type in global_objects.items():
            obj = eval(obj_name)
            if isinstance(obj, list) and len(obj) > 0:
                first_inst = obj[0]
                if self._is_namedtuple(first_inst):
                    nt_dict[obj_name] = obj 
            elif self._is_namedtuple(obj):
                nt_dict[obj_name] = obj 
        return nt_dict

    def _is_namedtuple(self, obj):
        obj_type = type(obj)
        bases = obj_type.__bases__
        if len(bases) != 1 or bases[0] != tuple:
            return False
        fields = getattr(obj_type, '_fields', None)
        if not isinstance(fields, tuple):
            return False
        return all(type(n) == str for n in fields)

    def sqlnt(self, sql):
        results = self._curs.execute(self.sql).fetchall()
        return results
