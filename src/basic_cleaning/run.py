#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging

import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    logger.info("cleaning data")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetim
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging artifact clean_sample.csv")
    run.log_artifact(artifact)

    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The input artifact to process",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description for the output",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price",
        required=True
    )

    args = parser.parse_args()

    go(args)
