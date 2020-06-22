class HandlerException(Exception):
  def __init__(self, status, message):
    super(HandlerException, self).__init__(status, message)

    self.status = status
    self.message = message

class BadRequestException(HandlerException):
  def __init__(self, message):
    super(BadRequestException, self).__init__(400, message)

class ResourceNotFoundException(HandlerException):
  def __init__(self, message):
    super(ResourceNotFoundException, self).__init__(404, message)

class ForbiddenException(HandlerException):
  def __init__(self, message):
    super(ForbiddenException, self).__init__(403, message)
