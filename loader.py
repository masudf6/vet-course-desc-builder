import pandas as pd
from typing import List

from models import Unit


def load_units(excel_file: str) -> List[Unit]:
    df = pd.read_excel(excel_file, dtype=str)
    return [
        Unit(
            code=row['Subject Code'].strip(),
            name=row['Subject Name'].strip(),
            type=row['Subject Type'].strip(),
            hours=row['Contact Hours'].strip(),
        )
        for _, row in df.iterrows() if row['Subject Code']
    ]