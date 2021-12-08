import os
import logging
import hydra
import mlflow

import {{ cookiecutter.src_package_name }} as {{ cookiecutter.src_package_name_short }}


@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """This main function does the following:
    - load config parameters
    - initialise experiment tracking (MLflow)
    - loads training, validation and test data
    - initialises model layers and compile
    - trains, evaluates, and then exports the model
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    {{ cookiecutter.src_package_name_short }}.general_utils.setup_logging(logger_config_path)

    logger.info("Loading config file.")

    mlflow.set_tracking_uri(args["train"]["mlflow_tracking_uri"])
    mlflow.set_experiment(args["train"]["mlflow_exp_name"])
    mlflow.set_registry_uri(args["train"]["mlflow_artifact_location"])
    mlflow.tensorflow.autolog()

    datasets = {{ cookiecutter.src_package_name_short }}.modeling.data_loaders.\
        load_datasets(hydra.utils.get_original_cwd(), args)

    model = {{ cookiecutter.src_package_name_short }}.modeling.models.seq_model(args)

    print('Training the model...')
    model.fit(
        datasets['train'],
        epochs=args['train']['epochs'],
        validation_data=datasets['val'])

    print('Evaluating the model...')

    # eval_metrics = model.evaluate(datasets['test'])
    model.evaluate(datasets['test'])

    {{ cookiecutter.src_package_name_short }}.modeling.utils.export_model(model)


if __name__ == '__main__':
    main()
