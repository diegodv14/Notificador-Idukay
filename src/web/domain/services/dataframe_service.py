from abc import ABC, abstractmethod
from typing import List

from src.web.domain.types.index import NoteEntry

class IDataFrameService(ABC):
    @staticmethod
    @abstractmethod
    def create_dataframe(data:List[NoteEntry]=None):
        """
        Create a DataFrame from the provided data.
        
        :param data: The data to create the DataFrame from.
        :return: A DataFrame object.
        """
        pass
