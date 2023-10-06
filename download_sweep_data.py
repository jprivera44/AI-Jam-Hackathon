"""Download artifacts from runs in a sweep for later analysis."""

import os

from tqdm import tqdm
import wandb

import constants

OUTPUT_FOLDER_ACTIONS = "results/actions_v2"
OUTPUT_FOLDER_VARIABLES = "results/variables_v2"


def main():
    """Main function."""

    api = wandb.Api()

    # Get user input for the sweep ID
    sweep_id = input("Enter the sweep ID: ")
    # sweep_id = "kckc8ckq"

    # Get the sweep
    sweep = api.sweep(f"{constants.WANDB_PROJECT}/{sweep_id}")

    # Get the runs in the sweep
    runs = list(sweep.runs)

    # Get user input for the prefix they want to use for the downloaded files
    prefix = input("Enter the prefix for the downloaded files: ").strip()
    # prefix = "DEBUG"

    # Download the artifacts from each run
    for run in tqdm(runs):
        # Download the actions artifact
        artifact_actions = api.artifact(
            f"{constants.WANDB_PROJECT}/run-{run.id}-whole_runactions:latest"
        )
        artifact_actions.download(root=OUTPUT_FOLDER_ACTIONS)

        # Rename the "actions.table.json" in the output folder to be prefix + 'A' + run.name[-1].json
        os.rename(
            f"{OUTPUT_FOLDER_ACTIONS}/whole_run/actions.table.json",
            f"{OUTPUT_FOLDER_ACTIONS}/{prefix} A{run.name[-1]}.json",
        )

        # Download the variables artifact
        artifact_variables = api.artifact(
            f"{constants.WANDB_PROJECT}/run-{run.id}-whole_rundynamic_vars:latest"
        )
        artifact_variables.download(root=OUTPUT_FOLDER_VARIABLES)

        # Rename the "dynamic_vars.table.json" in the output folder to be prefix + 'V' + run.name[-1].json
        os.rename(
            f"{OUTPUT_FOLDER_VARIABLES}/whole_run/dynamic_vars.table.json",
            f"{OUTPUT_FOLDER_VARIABLES}/{prefix} V{run.name[-1]}.json",
        )

    # Remove the whole_run folders
    if os.path.exists(f"{OUTPUT_FOLDER_ACTIONS}/whole_run"):
        os.rmdir(f"{OUTPUT_FOLDER_ACTIONS}/whole_run")
    if os.path.exists(f"{OUTPUT_FOLDER_VARIABLES}/whole_run"):
        os.rmdir(f"{OUTPUT_FOLDER_VARIABLES}/whole_run")


if __name__ == "__main__":
    main()
