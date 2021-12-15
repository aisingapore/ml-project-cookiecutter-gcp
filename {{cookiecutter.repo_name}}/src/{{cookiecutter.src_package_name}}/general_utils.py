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
    logger = logging.getLogger(__name__)

    try:
        with open(logging_config_path, "rt") as file:
            log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    except Exception as e:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=default_level)
        logger.info(e)
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
    bool
        This function returns a boolean value indicative of success
        of intialising connection with MLflow server.
    """
    init_success = False
    if setup_mlflow:
        try:
            mlflow.set_tracking_uri(args["train"]["mlflow_tracking_uri"])
            mlflow.set_experiment(args["train"]["mlflow_exp_name"])
            mlflow.set_registry_uri(args["train"]["mlflow_artifact_location"])
            if autolog:
                mlflow.autolog()
            init_success = True
            logger.info("MLflow initialisation has succeeded.")
        except:
            logger.error("MLflow initialisation has failed.")

    return init_success


def mlflow_log(mlflow_init_status,
            type="metric", track_dict={},
            artifact_path="", directory=False):
    """Custom function for logging to MLflow server.

    This function is only relevant when the function `mlflow_init`
    returns a "True" value, translating to a successful initialisation
    of a connection with an MLflow server.

    Parameters
    ----------
    mlflow_init_status : bool
        Boolean value indicative of success
        of intialising connection with MLflow server.
    type : {"metric", "param", "artifact"}
        Logging type, by default "metric"
    track_dict : dict, optional
        Dictionary containing keys and values of metrics or parameters
        to be tracked by MLflow, by default {}
    artifact_path : str, optional
        Path to a file or directory to be logged as artifact(s),
        by default ""
    directory : bool, optional
        Whether artifact being specified is a directory or not,
        by default False
    """
    if mlflow_init_status:
        if type == "metric" and bool(track_dict):
            mlflow.log_metrics(track_dict)
        if type == "param" and bool(track_dict):
            mlflow.log_params(track_dict)
        if type == "artifact" and artifact_path:
            if directory:
                mlflow.log_artifacts(artifact_path)
            else:
                mlflow.log_artifact(artifact_path)
