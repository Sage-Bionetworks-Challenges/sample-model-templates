"""Python Model Example"""
import os

import typer
import pandas as pd


def predict(df):
    """
    Run a prediction: full name will only contains two names.
    """
    df[['first_name', 'last_name']] = df['name'].str.split(" ", n=1, expand=True)
    return df


def main(input_dir: str = '/input',
         output_dir: str = '/output'):
    """
    Create a CLI with two args: `input_dir`, `output_dir`
    """
    data = pd.read_csv(os.path.join(input_dir, "names.csv"))
    predictions = predict(data)
    predictions.to_csv(os.path.join(output_dir, "predictions.csv"), index=False)


if __name__ == "__main__":
    typer.run(main)
