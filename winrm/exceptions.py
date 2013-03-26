class WinRMError(Exception):
    pass

class WinRMWebServiceError(WinRMError):
    """Generic WinRM SOAP Error"""
    pass

class WinRMAuthorizationError(WinRMError):
    """Authorization Error"""
    pass

class WinRMWSManFault(WinRMError):
    """A Fault returned in the SOAP response. The XML node is a WSManFault"""
    def __init__(self, code, reason, detail):
        super(WinRMWSManFault, self).__init__(code, reason, detail)
        self.code = code
        self.reason = reason
        self.detail = detail

    def __str__(self):
        return self.reason

class WinRMTimeout(WinRMWSManFault):
    """Exception raised if the winrm request timed out (at the winrm level)."""
    pass

class WinRMTransportError(WinRMError):
    """"Transport-level error"""
    pass
