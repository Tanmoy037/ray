import click
import os
import subprocess
from typing import List

import numpy as np

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument("targets", required=True, type=str)
@click.argument("team", required=True, type=str)
@click.option(
    "--concurrency",
    default=3,
    type=int,
    help=("Number of concurrent test jobs to run."),
)
@click.option(
    "--shard",
    default=0,
    type=int,
    help=("Index of the concurrent shard to run."),
)
def main(targets: str, team: str, concurrency: int, shard: int) -> None:
    test_targets = get_test_targets(targets, team)
    run_tests(np.array_split(test_targets, concurrency)[shard].tolist())


def run_tests(test_targets: List[str]) -> None:
    """
    Run tests
    """
    bazel_options = (
        subprocess.check_output([f"{CURRENT_DIR}/../../run/bazel_export_options"])
        .decode("utf-8")
        .split()
    )
    subprocess.check_call(
        [
            "bazel",
            "test",
            "--test_size_filters=small,medium",
            "--config=ci",
        ]
        + bazel_options
        + test_targets
    )


def get_test_targets(targets: str, team: str) -> List[str]:
    """
    Get all test targets that are not flaky
    """
    test_targets = (
        subprocess.check_output(
            [
                "bazel",
                "query",
                f"attr(tags, team:{team}, tests({targets})) intersect " "("
                # TODO(can): Remove this once we have a better way
                # to filter out test size
                f"attr(size, small, tests({targets})) union "
                f"attr(size, medium, tests({targets}))"
                ")",
            ]
        )
        .decode("utf-8")
        .split("\n")
    )
    with open(f"{CURRENT_DIR}/{team}.flaky", "rb") as f:
        flaky_tests = f.read().decode("utf-8").split("\n")

    return [test for test in test_targets if test not in flaky_tests]


if __name__ == "__main__":
    main()
