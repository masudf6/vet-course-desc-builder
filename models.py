# course_gen/models.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Unit:
    code: str
    name: str
    type: str
    hours: str
    criteria: List[str] = field(default_factory=list)