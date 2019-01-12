"""Perform SQL on namedtuple objects.
"""
from collections import namedtuple
import sqlite3


class SqlNt():
    def __init__(self, nt, nt_name, return_as_nt=True):
        self.nt = self._validate_object(nt)
        self._nt_name = nt_name
        self._db = self._init_db()
        self._curs = self._db.cursor()
        self._create_tables()
        self.table = self._nt_name
        self.fields = self._get_schema()
        self.return_as_nt = return_as_nt

    def _validate_object(self, obj):
        if isinstance(obj, list) and len(obj) > 0:
            first_inst = obj[0]
            if self._is_namedtuple(first_inst):
                return obj 
        elif self._is_namedtuple(obj):
            return obj
        raise TypeError("The object does not appear to be a namedtuple.")

    def __del__(self):
        self._teardown_db()

    def _init_db(self):
        db = sqlite3.connect(":memory:")
        db.row_factory = sqlite3.Row
        return db

    def _create_tables(self):
        if isinstance(self.nt, list):
            fields = self.nt[0]._fields
        else:
            fields = self.nt._fields
        create_sql = "create table {} (".format(self._nt_name)
        insert_sql = "insert into {} values (".format(self._nt_name)
        for column in fields:
            create_sql += "{},".format(column)
            insert_sql += "?,"
        create_sql = "{});".format(create_sql[:-1])
        insert_sql = "{});".format(insert_sql[:-1])
        self._curs.execute(create_sql)
        self._insert_tables(insert_sql)
        self._db.commit()

    def _insert_tables(self, sql):
        if isinstance(self.nt, list):
            for row in self.nt:
                values = tuple(row)
                self._curs.execute(sql, values)
        else:
            values = tuple(self.nt)
            self._curs.execute(sql, values)

    def _get_schema(self):
        sql = "select * from pragma_table_info(?);"
        results = self._curs.execute(sql, (self._nt_name,)).fetchall()
        fields = []
        for row in results:
            fields.append(row['name'])
        return fields

    def _teardown_db(self):
        self._curs.close()
        self._db.close()

    def _is_namedtuple(self, obj):
        obj_type = type(obj)
        bases = obj_type.__bases__
        if len(bases) != 1 or bases[0] != tuple:
            return False
        fields = getattr(obj_type, '_fields', None)
        if not isinstance(fields, tuple):
            return False
        return all(type(n) == str for n in fields)

    def _to_nt(self, row_obj):
        fields = row_obj.keys()
        nt = namedtuple('nt', ",".join(fields))
        return nt(*tuple(row_obj))

    def sqlnt(self, sql):
        try:
            results = []
            row_results = self._curs.execute(sql).fetchall()
            if not self.return_as_nt:
                for row in row_results:
                    results.append(tuple(row))
            else:
                for row in row_results:
                    results.append(self._to_nt(row))
        except sqlite3.OperationalError as ex:
            raise RuntimeError(ex)
        return results
