class ClientError(Exception):
  def __init__(self, error, status, message):
    self.error = error
    self.status = status
    self.message = message
    super().__init__(self.message)

  def to_dict(self):
    return {
      'error': self.error,
      'status': self.status,
      'message': self.message
    }
