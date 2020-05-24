from os import path
import time

class SQLDatabase:
  def __init__(self, connectionfactory):
    self.connectionfactory = connectionfactory
    self.initialise_database()

  def initialise_database(self):
    conn = self.connectionfactory.get_conn()
    result = conn.table_exists("db_patch")
    conn.close()

    if not result:
      self.init_from_schema()
    else:
      self.migrate_database()

  def init_from_schema(self):
    schema_path = path.join(path.dirname(__file__), "patch", "schema.sql")
    print("Empty database detected, initialising from schema: " + schema_path)

    with open(schema_path, 'r') as file:
      self.run_script(file.read())

    latest_patch = self.get_latest_patch()
    for i in range(0, latest_patch + 1):
      self.record_db_patch(i)

  def migrate_database(self):
    conn = self.connectionfactory.get_conn()
    last_patch = conn.query("SELECT patch_id FROM db_patch ORDER BY patch_id DESC LIMIT 1")[0][0]
    conn.close()
    latest_patch = self.get_latest_patch()

    for i in range(last_patch + 1, latest_patch + 1):
      print("Running migration script patch" + str(i) + ".sql")

      patch_path = path.join(path.dirname(__file__), "patch", "patch" + str(i) + ".sql")
      with open(patch_path, 'r') as file:
        self.run_script(file.read())

      self.record_db_patch(i)

  def run_script(self, script):
    conn = self.connectionfactory.get_conn()
    cmds = script.split(';')
    for cmd in cmds:
      cmd = cmd.strip()
      if len(cmd) == 0:
        continue

      try:
        conn.execute(cmd)
      except Exception as exception:
        print("Exception while executing: \"" + cmd + "\"")
        raise exception
    conn.close()

  def get_latest_patch(self):
    return 1

  def record_db_patch(self, patch_id):
    timestamp = int(time.time())
    conn = self.connectionfactory.get_conn()
    conn.execute("INSERT INTO db_patch (apply_datetime, patch_id) VALUES (%s, %s)", (timestamp, patch_id))
    conn.close()

  def execute(self, sql, params=()):
    conn = self.connectionfactory.get_conn()
    conn.execute(sql, params)
    conn.close()
  
  def query(self, sql, params=()):
    conn = self.connectionfactory.get_conn()
    result = conn.query(sql, params)
    conn.close()
    return result

