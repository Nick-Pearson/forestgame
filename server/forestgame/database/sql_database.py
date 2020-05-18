from os import path;
import time;

class SQLDatabase:
  def __init__(self, connection):
    self.c = connection;
    self.initialise_database();

  def initialise_database(self):
    result = self.c.table_exists("db_patch");

    if result == False:
      self.init_from_schema();
    else:
      self.migrate_database();
  
  def init_from_schema(self):
    schema_path = path.join(path.dirname(__file__), "patch", "schema.sql");
    print("Empty database detected, initialising from schema: " + schema_path);

    with open(schema_path, 'r') as f:
      self.run_script(f.read());

    latest_patch = self.get_latest_patch();
    for i in range(0, latest_patch + 1):
      self.record_db_patch(i);

  def migrate_database(self):
    print("Determining migration scripts to run");

  def run_script(self, script):
    c = self.c.conn.cursor();
    cmds = script.split(';')
    for cmd in cmds:
      try:
        c.execute(cmd);
      except Exception as e:
        print("exception while executing:\n" + cmd);
        raise e;
    c.close();
  
  def get_latest_patch(self):
    return 0;

  def record_db_patch(self, patch_id):
    timestamp = int(time.time());
    self.c.execute("INSERT INTO db_patch (apply_datetime, patch_id) VALUES (%s, %s)", (timestamp, patch_id));
