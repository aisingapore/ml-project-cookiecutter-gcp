"""Utilities or functions that are useful across all the different
modules in this package can be defined here."""

import os
import logging
import logging.config
import yaml
import mlflow


logger = logging.getLogger(__name__)


def setup_logging(logging_config_path="./conf/base/logging.yml",
                default_level=logging.INFO):
    """Set up configuration for logging utilities.

    Parameters
    ----------
    logging_config_path : str, optional
        Path to YAML file containing configuration for Python logger,
        by default "./config/logging_config.yaml"
    default_level : logging object, optional, by default logging.INFO
    """

    try:
        with open(logging_config_path, "rt") as file:
            log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    except Exception as error:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=default_level)
        logger.info(error)
        logger.info(
            "Logging config file is not found. Basic config is being used.")


def mlflow_init(args, setup_mlflow=False, autolog=False):
    """Initialise MLflow connection.

    Parameters
    ----------
    args : dict
        Dictionary containing the pipeline's configuration passed from
        Hydra.
    setup_mlflow : bool, optional
        Choice to set up MLflow connection, by default False
    autolog : bool, optional
        Choice to set up MLflow's autolog, by default False

    Returns
    -------
    init_success : bool
        Boolean value indicative of success
        of intialising connection with MLflow server.

    mlflow_run : Union[None, `mlflow.entities.Run` object]
        On successful initialisation, the function returns an object
        containing the data and properties for the MLflow run.
        On failure, the function returns a null value.
    """
    init_success = False
    mlflow_run = None
    if setup_mlflow:
        try:
            mlflow.set_tracking_uri(args["train"]["mlflow_tracking_uri"])
            mlflow.set_experiment(args["train"]["mlflow_exp_name"])

            if autolog:
                mlflow.autolog()

            mlflow.start_run()

            if "MLFLOW_HPTUNING_TAG" in os.environ:
                mlflow.set_tag(
                    "hptuning_tag",
                    os.environ.get("MLFLOW_HPTUNING_TAG"))

            mlflow_run = mlflow.active_run()
            init_success = True
            logger.info("MLflow initialisation has succeeded.")
            logger.info("UUID for MLflow run: {}".format(
                mlflow_run.info.run_id))
        except:
            logger.error("MLflow initialisation has failed.")

    return init_success, mlflow_run


def mlflow_log(mlflow_init_status,
            log_function, **kwargs):
    """Custom function for utilising MLflow's logging functions.

    This function is only relevant when the function `mlflow_init`
    returns a "True" value, translating to a successful initialisation
    of a connection with an MLflow server.

    Parameters
    ----------
    mlflow_init_status : bool
        Boolean value indicative of success of intialising connection
        with MLflow server.
    log_function : str
        Name of MLflow logging function to be used.
        See https://www.mlflow.org/docs/latest/python_api/mlflow.html
    **kwargs
        Keyword arguments passed to `log_function`.
    """
    if mlflow_init_status:
        try:
            method = getattr(mlflow, log_function)
            method(**{key: value for key, value in kwargs.items()
                    if key in method.__code__.co_varnames})
        except Exception as error:
            logger.error(error)
