import unittest

from forestgame.database.sql_connections import InMemoryConnection, PostgresConnection;
from forestgame.database.sql_database import SQLDatabase;

class MigrateDatabaseTest(unittest.TestCase):
  def test_inits_fresh_database_to_schema(self):
    c = InMemoryConnection();

    db = SQLDatabase(c);

    all_tables = c.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall();
    self.assertEqual("db_patch", all_tables[0][0]);

  def test_init_after_setup_does_not_init_again(self):
    c = InMemoryConnection();
    SQLDatabase(c);

    db = SQLDatabase(c);

    all_tables = c.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall();
    self.assertEqual("db_patch", all_tables[0][0]);