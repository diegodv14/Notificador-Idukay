import polars as pl

class EvaluationService(): 
             
    @staticmethod
    def get_bad_notes(df: pl.DataFrame) -> pl.DataFrame:
        return df.filter(int(pl.col("Nota")) < 10)