import re
import requests
import xml.etree.ElementTree as ET
from typing import List


def scrape_unit(unit_code: str) -> List[str]:
    """
    Download the XML for unit_code, strip any BOM, parse it,
    and extract only the numbered performance criteria.
    """
    # 1. Download raw bytes
    pkg     = unit_code[:3]
    url     = f"https://training.gov.au/assets/{pkg}/{unit_code}_R1.xml"
    resp    = requests.get(url)
    resp.raise_for_status()

    # 2. Decode and remove BOM if present
    xml_text = resp.content.decode('utf-8-sig')

    # 3. Parse with AuthorIT namespace
    ns   = {'a': 'http://www.authorit.com/xml/authorit'}
    root = ET.fromstring(xml_text)

    criteria = []
    # 4. Find the right <Topic>
    for topic in root.findall('.//a:Topic', ns):
        heading = topic.find('.//a:PrintHeading', ns)
        if heading is not None and heading.text and heading.text.strip() == 'Elements and Performance Criteria':
            # 5. Iterate rows, skip header, pull <p> from second <td>
            for tr in topic.findall('.//a:tr', ns):
                if tr.get('header') == 'true':
                    continue
                tds = tr.findall('a:td', ns)
                if len(tds) < 2:
                    continue
                for p in tds[1].findall('a:p', ns):
                    text = ''.join(p.itertext()).strip()
                    # 6. Only keep bullets that start with a digit (e.g. "1.1", "2.3", etc.)
                    if re.match(r'^\d+\.\d+', text):
                        criteria.append(text)
            break

    if not criteria:
        raise ValueError(f"No numbered performance criteria found for unit {unit_code!r}")

    return criteria  # Return type is List[str]