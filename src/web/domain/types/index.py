from typing import Any, List, TypedDict


class Parcial(TypedDict):
    type: str
    note: str

class Material(TypedDict):
    topic: str
    note: List[Parcial] = []

class NoteEntry(TypedDict):
    student: str        
    notes: List[Material] = []
