"""This module provides definitions of predictive models to be
trained."""

import tensorflow as tf
import tensorflow_hub as hub


def seq_model(args):
    """Initialise a sequential model.

    Paramaters
    ----------
    args : dict
        Dictionary containing the pipeline's configuration passed from
        Hydra.

    Returns
    -------
    tf.keras.Model
        Compiled sequential model.
    """

    hub_layer = hub.KerasLayer(
        args["train"]["pretrained_embedding"], input_shape=[],
        dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation="relu"))
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer=args["train"]["optimiser"],
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=[args["train"]["metric"]])

    return model
