from typing import Any, List, TypedDict


class Material(TypedDict):
    topic: str
    note: str

class NoteEntry(TypedDict):
    student: str        
    notes: List[Material] = []
