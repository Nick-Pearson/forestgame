import unittest

from forestgame.database.sql_connections import InMemoryConnectionFactory;
from forestgame.database.sql_database import SQLDatabase;

class MigrateDatabaseTest(unittest.TestCase):
  def test_inits_fresh_database_to_schema(self):
    c = InMemoryConnectionFactory();
    conn = c.get_conn().conn;

    db = SQLDatabase(c);

    all_tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall();
    self.assertEqual("db_patch", all_tables[0][0]);

  def test_init_after_setup_does_not_init_again(self):
    c = InMemoryConnectionFactory();
    conn = c.get_conn().conn;
    SQLDatabase(c);

    db = SQLDatabase(c);

    all_tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall();
    self.assertEqual("db_patch", all_tables[0][0]);

  # TODO: Database patch test