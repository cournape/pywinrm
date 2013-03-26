import xml.etree.cElementTree as ET

from winrm.exceptions import WinRMTimeout, WinRMWSManFault

#NS_SOAP_ENV ='s' # http://www.w3.org/2003/05/soap-envelope
#NS_ADDRESSING ='a' # http://schemas.xmlsoap.org/ws/2004/08/addressing
#NS_CIMBINDING ='b' # http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd
#NS_ENUM ='n' # http://schemas.xmlsoap.org/ws/2004/09/enumeration
#NS_TRANSFER ='x' # http://schemas.xmlsoap.org/ws/2004/09/transfer
#NS_WSMAN_DMTF ='w' # http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd
#NS_WSMAN_MSFT ='p' # http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd
#NS_SCHEMA_INST ='xsi' # http://www.w3.org/2001/XMLSchema-instance
#NS_WIN_SHELL ='rsp' # http://schemas.microsoft.com/wbem/wsman/1/windows/shell
#NS_WSMAN_FAULT = 'f' # http://schemas.microsoft.com/wbem/wsman/1/wsmanfault
#NS_WSMAN_CONF = 'cfg'# http://schemas.microsoft.com/wbem/wsman/1/config

NS_SOAP_ENV = "{http://www.w3.org/2003/05/soap-envelope}"
NS_WSMAN_FAULT = "{http://schemas.microsoft.com/wbem/wsman/1/wsmanfault}"
NS_ADDRESSING ="{http://schemas.xmlsoap.org/ws/2004/08/addressing}"
NS_CIMBINDING ="{http://schemas.dmtf.org/wbem/wsman/1/cimbinding.xsd}"

ENVELOPE = ET.Element(NS_SOAP_ENV + "Envelope")

HEADER = ET.SubElement(ENVELOPE, NS_SOAP_ENV + "Header")
BODY = ET.SubElement(ENVELOPE, NS_SOAP_ENV + "Body")

FAULT = ET.SubElement(BODY, NS_SOAP_ENV + "Fault")

CODE = ET.SubElement(FAULT, NS_SOAP_ENV + "Code")
REASON = ET.SubElement(FAULT, NS_SOAP_ENV + "Reason")
DETAIL = ET.SubElement(FAULT, NS_SOAP_ENV + "Detail")

REASON_TEXT = ET.SubElement(REASON, NS_SOAP_ENV  + "Text")

# FIXME: there HAS to be a better way to handle that namespace-related crap
def parse_fault(message):
    root = ET.fromstring(message)
    body = root.find(BODY.tag)
    fault = body.find(FAULT.tag)
    if fault:
        code = fault.find(CODE.tag). \
            find(NS_SOAP_ENV + "Subcode" + "/" + NS_SOAP_ENV + "Value").text
        reason = fault.find(REASON.tag).find(NS_SOAP_ENV + "Text").text
        detail = fault.find(DETAIL.tag). \
            find(NS_WSMAN_FAULT + "WSManFault/" + NS_WSMAN_FAULT + "Message").text
        if code == "w:TimedOut":
            return WinRMTimeout(code, reason, detail)
        else:
            return WinRMWSManFault(code, reason, detail)
    else:
        raise ValueError("Could not parse message as fault")
