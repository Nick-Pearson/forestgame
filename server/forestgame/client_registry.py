import uuid
import time
import httpagentparser

class Client:
  def __init__(self, client_id, user_agent):
    self.client_id = client_id
    self.create_datetime = int(time.time())
    self.last_datetime = self.create_datetime
    self.user_agent = user_agent

    agent_data = httpagentparser.detect(user_agent)
    os_data = agent_data.get("os") or {}
    self.user_os_name = os_data.get("name")
    self.user_os_version = os_data.get("version")
    browser_data = agent_data.get("browser") or {}
    self.user_browser_name = browser_data.get("name")
    self.user_browser_version = browser_data.get("version")
    self.bot = agent_data.get("bot")

  def insert_to_db(self, db):
    db.execute("""
        INSERT INTO client (uuid,
                            create_datetime,
                            last_datetime,
                            user_agent,
                            user_os_name,
                            user_os_version,
                            user_browser_name,
                            user_browser_version,
                            bot)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
               (self.client_id,
                self.create_datetime,
                self.last_datetime,
                self.user_agent,
                self.user_os_name,
                self.user_os_version,
                self.user_browser_name,
                self.user_browser_version,
                self.bot))

class ClientRegistry:
  def __init__(self, db):
    self.db = db

  def refresh_client(self, client_id):
    timestamp = int(time.time())
    self.db.execute("UPDATE client SET last_datetime = %s WHERE uuid=%s", (timestamp, str(client_id)))

  def add_client(self, user_agent):
    client = Client(str(uuid.uuid4()), user_agent)
    client.insert_to_db(self.db)
    return client
