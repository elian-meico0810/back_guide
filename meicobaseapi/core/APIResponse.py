from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, status_code=None, data=None, message=None, **kwargs):
        success = True
        if status_code > 202:
            success = False
        response_data = {
            "statusCode": status_code,
            "data": data,
            "message": message,
            "success": success
        }
        super().__init__(data=response_data, status=status_code, **kwargs)
 