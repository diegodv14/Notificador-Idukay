import polars as pl

class EvaluationService(): 
             
    @staticmethod
    def get_bad_notes(df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns([
            pl.col("Nota").cast(pl.Float64)
        ])
        return df.filter(pl.col("Nota") < 11)