"""Any miscellaneous utilities/functions to assist the model
training workflow are to be contained here."""

import os
import hydra
import tensorflow as tf

def export_model(model):
    """Serialises and exports the trained model.

    Parameters
    ----------
    model : tf.keras.Model
        Trained model.
    """

    model_file_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "models/text-classification-model")

    model.save(model_file_path)


def load_model(path_to_model):
    """Function to load the predictive model.

    A sample utility function to be used for loading a Keras model
    saved in 'SavedModel' format. This function can be customised
    for more complex loading steps.

    Parameters
    ----------
    path_to_model : str
        Path to a directory containing a Keras model in
        'SavedModel' format.

    Returns
    -------
    Keras model instance
        An object with the compiled model.
    """

    loaded_model = tf.keras.models.load_model(path_to_model)
    return loaded_model
