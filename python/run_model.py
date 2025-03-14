"""Python Model Example"""
import os

import pandas as pd
import typer
from typing_extensions import Annotated


def predict(df):
    """
    Run a prediction: full name will only contains two names.
    """
    df[["first_name", "last_name"]] = df["name"].str.split(" ", n=1, expand=True)
    return df


def main(
    input_dir: Annotated[str, typer.Option()] = "/input",
    output_dir: Annotated[str, typer.Option()] = "/output",
):
    """
    Run inference using data in input_dir and output predictions to output_dir
    """
    data = pd.read_csv(os.path.join(input_dir, "names.csv"))
    predictions = predict(data)
    predictions.to_csv(os.path.join(output_dir, "predictions.csv"), index=False)


if __name__ == "__main__":
    typer.run(main)
