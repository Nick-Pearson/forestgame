BUILDINGS = [
  {
    "name": "Town Hall",
    "id": 0,
    "buildable": False,
  },
  {
    "name": "Farm",
    "id": 1,
    "buildable": True,
    "cost": {
      "wood": 20
    }
  },
  {
    "name": "Sawmill",
    "id": 3,
    "buildable": True,
    "cost": {
      "wood": 40,
      "gold": 10
    }
  },
  {
    "name": "Windmill",
    "id": 4,
    "buildable": True,
    "cost": {
      "wood": 20,
      "gold": 15
    }
  },
]

def get_building_for_id(building_id):
  for building in BUILDINGS:
    if building["id"] == building_id:
      return building
  return None
