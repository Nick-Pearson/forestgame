import os
import json
import sys

def populate_from_env(settings):
  if "PORT" in os.environ:
    settings["port"] = os.environ["PORT"];
  if "DATABASE_URL" in os.environ:
    settings["databaseUrl"] = os.environ["DATABASE_URL"];

def populate_from_args(settings):
  for arg in sys.argv:
    if arg == "--debug":
      settings["debug"] = True;
    if arg == "--in-memory":
      settings["runMemoryDatabase"] = True;

def load_settings():
  settings = {
    "name": "forestgame",
    "port": 5000,
    "debug": False,
    "runMemoryDatabase": False,
    "databaseUrl": "dbname=test user=postgres"
  };
  populate_from_env(settings);
  populate_from_args(settings);
  return settings;