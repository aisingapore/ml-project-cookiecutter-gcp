import os
import hydra

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
