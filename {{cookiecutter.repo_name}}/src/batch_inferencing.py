import os
import datetime
import logging
import hydra
import glob
import jsonlines


import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """This main function does the following:
    - load logging config
    - gets list of files to be loaded for inferencing
    - loads trained model
    - conducts inferencing on data
    - outputs prediction results to a jsonline file
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(logger_config_path)

    logger.info("Loading the model...")
    pred_model = {{cookiecutter.src_package_name_short}}.modeling.utils.load_model(
        args["inference"]["model_path"])

    glob_expr = "{}/*.txt".\
        format(args["inference"]["input_data_dir"])
    logger.info("Conducting inferencing on text files...")

    for movie_review_file in glob.glob(glob_expr):

        file = open(movie_review_file, "r")
        file_content = file.readlines()
        curr_pred_result = float(pred_model.predict(file_content))
        sentiment = ("positive" if curr_pred_result > 0.5
                    else "negative")

        curr_time = datetime.datetime.now(
            datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        curr_res_jsonl = {
            "time": curr_time,
            "filepath": movie_review_file,
            "logit_prob": curr_pred_result,
            "sentiment": sentiment}

        with jsonlines.open("batch-infer-res.jsonl", mode="a") as writer:
            writer.write(curr_res_jsonl)
            writer.close()

    logger.info("Batch inferencing has completed.")
    logger.info("Output result location: {}/batch-infer-res.jsonl".
                format(os.getcwd()))

if __name__ == "__main__":
    main()
