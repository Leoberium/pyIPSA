# TODO
import argparse

import pandas as pd


def parse_cli_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(
        description="Filter splice junctions and sites by different criteria"
    )
    parser.add_argument(
        "-i", "--input", type=str, metavar="FILE", required=True,
        help="input junctions file (step >= 3)"
    )
    parser.add_argument(
        "-e", "--entropy", type=float, metavar="FLOAT", default=1.5,
        help="entropy threshold"
    )
    parser.add_argument(
        "-c", "--count", type=int, metavar="INT", default=1,
        help="total count threshold"
    )
    parser.add_argument(
        "-g", "--gtag", action="store_true",
        help="use only GTAG splice sites"
    )
    parser.add_argument(
        "-o", "--output", type=str, metavar="FILE", required=True,
        help="output file name (step 6)"
    )
    args = parser.parse_args()
    return vars(args)


def read_and_filter(filename: str, entropy: float,
                    count: int, gtag: bool) -> pd.DataFrame:
    """Reads junctions, filters them and outputs sorted DataFrame."""
    df = pd.read_table(filename, header=None)
    df.columns = ["sj_id", "total_count", "staggered_count", "entropy",
                  "status", "nucleotides"]
    # filters
    c = df["total_count"] >= count
    e = df["entropy"] >= entropy
    df = df[c & e]
    if gtag:
        df = df[df["nucleotides"] == "GTAG"]
    return df


def main():
    args = parse_cli_args()
    df = read_and_filter(filename=args["input"], entropy=args["entropy"],
                         count=args["count"], gtag=args["gtag"])
    df.to_csv(args["output"], sep="\t", index=False, header=False, compression="gzip")


if __name__ == '__main__':
    main()
