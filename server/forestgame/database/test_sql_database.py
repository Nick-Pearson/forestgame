import unittest
import re
import os
from os import path

from forestgame.database.sql_connections import InMemoryConnectionFactory, PostgresConnectionFactory
from forestgame.database.sql_database import SQLDatabase

class MigrateDatabaseTest(unittest.TestCase):
  def get_connection_factory(self):
    if "DATABASE_URL" in os.environ:
      factory = PostgresConnectionFactory(os.environ["DATABASE_URL"])
      conn = factory.get_conn()
      conn.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
      conn.close()
      return factory
    return InMemoryConnectionFactory()

  def test_inits_fresh_database_to_schema(self):
    connection_factory = self.get_connection_factory()
    conn = connection_factory.get_conn()

    SQLDatabase(connection_factory)

    self.assertTrue(conn.table_exists("db_patch"))

  def test_init_after_setup_does_not_init_again(self):
    connection_factory = self.get_connection_factory()
    conn = connection_factory.get_conn()
    SQLDatabase(connection_factory)

    SQLDatabase(connection_factory)

    self.assertTrue(conn.table_exists("db_patch"))

  def test_init_from_base_patches_up_to_latest(self):
    connection_factory = self.get_connection_factory()
    if not isinstance(connection_factory, PostgresConnectionFactory):
      self.skipTest("Postgres DB not available")
      return

    conn = connection_factory.get_conn()
    schema_path = path.join(path.dirname(__file__), "patch", "baseschema.sql")
    with open(schema_path, 'r') as file:
      conn.conn.execute(file.read())
    conn.execute("INSERT INTO db_patch (apply_datetime, patch_id) VALUES (0, 0)")

    SQLDatabase(connection_factory)
    dump = conn.query("SELECT sql FROM sqlite_master WHERE type = 'table'")
    conn.close()

    conn = connection_factory.get_conn()
    SQLDatabase(connection_factory)
    expected = conn.query("SELECT sql FROM sqlite_master WHERE type = 'table'")
    self.assertEqual(len(expected), len(dump))
    for i in range(0, len(dump)):
      self.assert_string_contents_equal(dump[i][0], expected[i][0])

  def assert_string_contents_equal(self, str1, str2):
    regex = '[\n| |\t]'
    str1 = re.sub(regex, '', str1)
    str1 = re.sub(',', ',\n', str1)
    str2 = re.sub(regex, '', str2)
    str2 = re.sub(',', ',\n', str2)
    self.assertEqual(str1, str2)
