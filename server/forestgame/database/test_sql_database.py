import unittest;
import re
from os import path;

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

  def test_init_from_base_patches_up_to_latest(self):
    c = InMemoryConnectionFactory();
    conn = c.get_conn();
    schema_path = path.join(path.dirname(__file__), "patch", "baseschema.sql");
    with open(schema_path, 'r') as f:
      conn.conn.executescript(f.read());
    conn.execute("INSERT INTO db_patch (apply_datetime, patch_id) VALUES (0, 0)");

    SQLDatabase(c);
    dump = conn.query("SELECT sql FROM sqlite_master WHERE type = 'table';");
    conn.close();

    conn = c.get_conn();
    SQLDatabase(c);
    expected = conn.query("SELECT sql FROM sqlite_master WHERE type = 'table';");
    self.assertEqual(len(expected), len(dump));
    for i in range(0, len(dump)):
      self.assertStringContentsEqual(dump[i][0], expected[i][0]);
  
  def assertStringContentsEqual(self, str1, str2):
    regex = '[\n| |\t]';
    str1 = re.sub(regex, '', str1)
    str1 = re.sub(',', ',\n', str1)
    str2 = re.sub(regex, '', str2)
    str2 = re.sub(',', ',\n', str2)
    self.assertEqual(str1, str2);