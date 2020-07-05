from flask_socketio import emit

class Event:
  def __init__(self, event_type, data, display_msg):
    self.event_type = event_type
    self.data = data
    self.display_msg = display_msg

class EventSystem:
  def emit_event(self, event, game_id):
    print("sending event type " + event.event_type + " for " + game_id)
    event_map = {
      "type": event.event_type,
      "display_msg": event.display_msg
    }
    emit('game_event', event_map, room=game_id, namespace='/')
    emit(event.event_type, event.data, room=game_id, namespace='/')