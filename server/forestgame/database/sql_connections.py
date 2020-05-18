import re
import psycopg2

class InMemoryConnection:
  def __init__(self):
    import sqlite3
    print("Connecting to in-memory database");
    self.conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
  
  def table_exists(self, table):
    result = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "'");
    return len(result.fetchall()) != 0;

  def execute(self, sql, params=()):
    sql = re.sub("%\S?", "?", sql)
    self.conn.execute(sql, params);

  def close(self):
    self.conn.close();

class InMemoryConnectionFactory:
  def get_conn(self):
    return InMemoryConnection();

class PostgresConnection:
  def __init__(self, database_url):
    self.conn = psycopg2.connect(database_url, sslmode='require')
  
  def table_exists(self, table):
    cur = self.conn.cursor();
    cur.execute("SELECT to_regclass('public." + table + "')")
    result = cur.fetchall()
    cur.close();
    return len(result) != 0;

  def execute(self, sql, params=()):
    cur = self.conn.cursor();
    cur.execute(sql, params);
    self.conn.commit();
    cur.close();

  def close(self):
    self.conn.close();

class PostgresConnectionFactory:
  def __init__(self, database_url):
    print("Setting up postgres with " + database_url);
    self.database_url = database_url;
  
  def get_conn(self):
    return PostgresConnection(self.database_url);