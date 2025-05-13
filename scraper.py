import re
import requests
import xml.etree.ElementTree as ET
from typing import List


def scrape_unit(unit_code: str) -> List[str]:
    """
    Downloads the XML for unit_code, strips any BOM, parses it,
    and extracts only the numbered performance criteria.
    """
    # 1. download raw bytes
    pkg     = unit_code[:3]
    url     = f"https://training.gov.au/assets/{pkg}/{unit_code}_R1.xml"
    resp    = requests.get(url)
    resp.raise_for_status()

    # 2. decode and remove BOM if present
    xml_text = resp.content.decode('utf-8-sig')

    # 3. parse with AuthorIT namespace
    ns   = {'a': 'http://www.authorit.com/xml/authorit'}
    root = ET.fromstring(xml_text)

    criteria = []
    # 4. find the right <Topic>
    for topic in root.findall('.//a:Topic', ns):
        heading = topic.find('.//a:PrintHeading', ns)
        if heading is not None and heading.text and heading.text.strip() == 'Elements and Performance Criteria':
            # iterate rows, skip header, pull <p> from second <td>
            for tr in topic.findall('.//a:tr', ns):
                if tr.get('header') == 'true':
                    continue
                tds = tr.findall('a:td', ns)
                if len(tds) < 2:
                    continue
                for p in tds[1].findall('a:p', ns):
                    text = ''.join(p.itertext()).strip()
                    # only keeping text that start with a digit ("1.1", "2.3", etc.)
                    if re.match(r'^\d+\.\d+', text):
                        criteria.append(text)
            break

    if not criteria:
        raise ValueError(f"No performance criteria found for unit {unit_code!r}")

    return criteria