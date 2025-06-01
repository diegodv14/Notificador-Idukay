from abc import ABC, abstractmethod
import polars as pl
class IEvaluationService(ABC):
    @staticmethod
    @abstractmethod
    def get_bad_notes(df: pl.DataFrame) -> pl.DataFrame:
        """
        
        """
        pass