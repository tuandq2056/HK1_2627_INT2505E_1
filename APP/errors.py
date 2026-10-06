class ProblemError(Exception):
    def __init__(self, status=500, title="Internal Server Error", detail=None, error_type="about:blank", instance=None):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = error_type
        self.instance = instance

    def to_dict(self, req_path=None):
        return {
            "type": self.type,
            "title": self.title,
            "detail": self.detail,
            "status": self.status,
            "instance": self.instance or req_path,
            "error": self.detail,
        }

class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass