class InvalidUrl(Error):
    """Raised for an invalid server URL"""
    pass

class IncompleteParams(Error):
    """Raised for an incomplete inputs"""
    pass

class ResponseError(Error):
    """Raised for an unsuccessful response from the server"""
    pass