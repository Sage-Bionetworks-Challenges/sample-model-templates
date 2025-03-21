"""Python Model Example"""

import os

import numpy as np
import pandas as pd
import typer
from typing_extensions import Annotated


def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Sample prediction function.

    TODO: Replace this with your actual model prediction logic. In this
    example, random floats are assigned.
    """
    pred = df.loc[:, ["id"]]
    pred["probability"] = np.random.random_sample(size=len(pred.index))
    return pred


def main(
    input_dir: Annotated[str, typer.Option()] = "/input",
    output_dir: Annotated[str, typer.Option()] = "/output",
):
    """
    Run inference using data in input_dir and output predictions to output_dir.
    """
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))
    predictions = predict(data)
    predictions.to_csv(
        os.path.join(output_dir, "predictions.csv"),
        index=False,
    )


if __name__ == "__main__":
    typer.run(main)
