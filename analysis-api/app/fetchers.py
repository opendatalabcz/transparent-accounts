from typing import Optional
from xml.etree import ElementTree

import requests


def fetch_identifier(identifier: str) -> Optional[str]:
    """
    Fetches the name of the company with the given identifier from the ARES database.
    :param identifier: identifier of the company (IČO)
    :return: name of the company or None if not found
    """
    response = requests.get(f"https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico={identifier}")
    tree = ElementTree.fromstring(response.content)
    # Namespace of the ARES XML schema
    ns = {'are': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1'}
    # Use XML path's './/' to search for the element in the whole tree
    element = tree.find('.//are:Obchodni_firma', ns)
    return element.text if element is not None else None
