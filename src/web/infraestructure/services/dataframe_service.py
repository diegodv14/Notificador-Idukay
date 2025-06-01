from typing import List
import polars as pl

from web.domain.services.dataframe_service import IDataFrameService
from web.domain.types.index import NoteEntry


class DataFrameService(IDataFrameService):
    @staticmethod
    def create_dataframe(data: List[NoteEntry] = None) -> pl.DataFrame:
        
        if(data is None or not isinstance(data, list) or not all(isinstance(entry, dict) for entry in data)):
            raise ValueError("Invalid data format. Expected a list of student entries with notes.")
        
        map_data = []
        for student_entry in data:
            student_name = student_entry["student"]
            for topic_entry in student_entry["notes"]:
                topic_name = topic_entry["topic"]
                for note_entry in topic_entry["note"]:
                    map_data.append({
                        "Estudiante": student_name,
                        "Materia": topic_name,
                        "Tipo de Nota": note_entry["type"],
                        "Nota": note_entry["note"]
                    })
                    
        
                    
        return pl.DataFrame(map_data)

        
