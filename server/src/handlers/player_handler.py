from flask import Blueprint, request

class PlayerHandler():  
  def change_name(self, game_id):
    requestData = request.get_json();
    return {"name": requestData["name"]};

  def get_name(self, game_id):
    return {"name": "The player's name"};
    
  def get_player_stats(self, game_id):
    stats = {
        "population": 150,
        "wood": 25,
        "coin": 110,
        "food": 10
    };
    return {"stats": stats};