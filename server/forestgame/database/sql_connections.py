import re
import psycopg2

class InMemoryConnection:
  def __init__(self):
    import sqlite3
    print("Connecting to in-memory database");
    self.conn = sqlite3.connect(':memory:');
  
  def table_exists(self, table):
    result = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "'");
    return len(result.fetchall()) != 0;

  def execute(self, sql, params):
    sql = re.sub("%\S?", "?", sql)
    self.conn.execute(sql, params);

class PostgresConnection:
  def __init__(self, database_url):
    print("Connecting to " + database_url);
    self.conn = psycopg2.connect(database_url, sslmode='require')
  
  def table_exists(self, table):
    cur = self.conn.cursor();
    result = cur.execute("SELECT to_regclass('schema_name.table_name');");
    cur.close();
    return result != None;

  def execute(self, sql, params):
    cur = self.conn.cursor();
    cur.execute(sql, params);
    cur.close();