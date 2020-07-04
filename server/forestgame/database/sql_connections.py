import re
import sqlite3
import psycopg2

class InMemoryConnection:
  def __init__(self):
    self.conn = sqlite3.connect("file::memory:?cache=shared", uri=True)

  def table_exists(self, table):
    result = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "'")
    return len(result.fetchall()) != 0

  def execute(self, sql, params=()):
    sql = re.sub(r"%\S?", "?", sql)
    self.conn.execute(sql, params)
    self.conn.commit()

  def query(self, sql, params=()):
    sql = re.sub(r"%\S?", "?", sql)
    cur = self.conn.cursor()
    cur.execute(sql, params)
    result = cur.fetchall()
    cur.close()
    return result

  def close(self):
    self.conn.close()

class InMemoryConnectionFactory:
  def __init__(self):
    # keep a persistent connection open
    print("Setting up in-memory database")
    self.__conn = InMemoryConnection()

  def get_conn(self):
    return InMemoryConnection()

class PostgresConnection:
  def __init__(self, database_url):
    self.conn = psycopg2.connect(database_url, sslmode='require')

  def table_exists(self, table):
    cur = self.conn.cursor()
    cur.execute("SELECT to_regclass('public." + table + "')")
    result = cur.fetchall()
    cur.close()
    return result[0][0] is not None

  def execute(self, sql, params=()):
    cur = self.conn.cursor()
    cur.execute(sql, params)
    self.conn.commit()
    cur.close()

  def query(self, sql, params=()):
    cur = self.conn.cursor()
    cur.execute(sql, params)
    result = cur.fetchall()
    cur.close()
    return result

  def close(self):
    self.conn.close()

class PostgresConnectionFactory:
  def __init__(self, database_url):
    print("Setting up postgres with " + database_url)
    self.database_url = database_url

  def get_conn(self):
    return PostgresConnection(self.database_url)
