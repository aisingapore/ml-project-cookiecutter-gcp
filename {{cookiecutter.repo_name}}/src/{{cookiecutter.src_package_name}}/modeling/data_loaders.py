"""This module contains functions that assist in loading datasets
for the model training pipeline."""

import os
import tensorflow as tf


def load_datasets(current_working_dir, args):
    """Load datasets specified through YAML config.

    Paramaters
    ----------
    args : dict
        Dictionary containing the pipeline's configuration passed from
        Hydra.

    Returns
    -------
    dict
        Dictionary object for which its values are "tf.data.Dataset"
        objects.
    """

    data_path = os.path.join(
        current_working_dir, args["train"]["data_path"])

    train_ds = tf.keras.preprocessing.text_dataset_from_directory(
        os.path.join(data_path, "train"),
        batch_size=args["train"]["bs"],
        validation_split=args["train"]["val_split"],
        subset="training",
        seed=args["train"]["seed"])

    val_ds = tf.keras.preprocessing.text_dataset_from_directory(
        os.path.join(data_path, "train"),
        batch_size=args["train"]["bs"],
        validation_split=args["train"]["val_split"],
        subset="validation",
        seed=args["train"]["seed"])

    test_ds = tf.keras.preprocessing.text_dataset_from_directory(
        os.path.join(data_path, "test"),
        batch_size=args["train"]["bs"])

    datasets = {
        "train": train_ds,
        "val": val_ds,
        "test": test_ds
    }

    return datasets
