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
    "name": "Swamill",
    "id": 2,
    "buildable": True,
    "cost": {
      "wood": 40,
      "gold": 10
    }
  },
  {
    "name": "Windmill",
    "id": 3,
    "buildable": True,
    "cost": {
      "wood": 20,
      "gold": 15
    }
  },
];

def get_building_for_id(id):
  for building in BUILDINGS:
    if building["id"] == id:
      return building;
  return None;