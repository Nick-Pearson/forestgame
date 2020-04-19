# Internal representatiob of rest request
# Abstracts away specifics of whatever web library
class Request:
  def __init__(self, client_id, path, body=None):
    self.client_id = client_id;
    self.path = path;

    if body == None:
      self.body = {};
    else:
      self.body = body;