import os
import logging
import hydra
import mlflow


import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


@hydra.main(config_path="../conf/base", config_name="train-model-hptuning.yml")
def main(args):
    """This main function does the following:
    - load logging config
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
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(logger_config_path)

    mlflow_init_status, mlflow_run = {{cookiecutter.src_package_name_short}}.general_utils.\
        mlflow_init(
            args, setup_mlflow=args["train"]["setup_mlflow"],
            autolog=args["train"]["mlflow_autolog"])
    {{cookiecutter.src_package_name_short}}.general_utils.\
        mlflow_log(
            mlflow_init_status, "log_params",
            params=args["train"])

    datasets = {{cookiecutter.src_package_name_short}}.modeling.data_loaders.\
        load_datasets(hydra.utils.get_original_cwd(), args)

    model = {{cookiecutter.src_package_name_short}}.modeling.models.seq_model(args)

    logger.info("Training the model...")
    model.fit(
        datasets["train"],
        epochs=args["train"]["epochs"],
        validation_data=datasets["val"])

    logger.info("Evaluating the model...")
    test_loss, test_acc = model.evaluate(datasets["test"])

    logger.info("Test Loss: {}, Test Accuracy: {}".\
        format(test_loss, test_acc))

    logger.info("Exporting the model...")
    {{cookiecutter.src_package_name_short}}.modeling.utils.export_model(model)

    if mlflow_init_status:
        artifact_uri = mlflow.get_artifact_uri()
        logger.info("Artifact URI: {}".format(artifact_uri))
        {{cookiecutter.src_package_name_short}}.general_utils.\
            mlflow_log(
                mlflow_init_status, "log_params",
                params={"artifact_uri": artifact_uri})
        logger.info("Model training with MLflow run ID {} has completed.".
            format(mlflow_run.info.run_id))
        mlflow.end_run()
    else:
        logger.info("Model training has completed.")

    return test_loss,test_acc


if __name__ == "__main__":
    main()
