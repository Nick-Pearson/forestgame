import os
import json
import sys

def populate_from_env(settings):
  if "PORT" in os.environ:
    settings["port"] = os.environ["PORT"];

def populate_from_args(settings):
  for arg in sys.argv:
    if arg == "--debug":
      settings["debug"] = True;

def load_settings():
  settings = {
    "name": "forestgame",
    "port": 5000,
    "debug": False,
  };
  populate_from_env(settings);
  populate_from_args(settings);
  return settings;