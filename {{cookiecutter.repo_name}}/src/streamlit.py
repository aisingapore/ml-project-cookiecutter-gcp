import os
import logging
import hydra
import streamlit as st

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}

@st.cache
def load_model(model_path):
    return {{cookiecutter.src_package_name_short}}.modeling.utils.load_model(model_path)

@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """This main function does the following:
    - load logging config
    - loads trained model on cache
    - gets string from user to be loaded for inferencing
    - conducts inferencing on string
    - outputs prediction results on the dashboard
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(logger_config_path)

    logger.info("Loading the model...")
    pred_model = load_model(args["inference"]["model_path"])

    logger.info("Loading dashboard...")
    title = st.title('{{cookiecutter.project_name}}')

    text_input = st.text_input("Review",
        placeholder="Insert your review here")

    logger.info("Conducting inferencing on text input...")
    curr_pred_result = float(pred_model.predict(text_input))
    sentiment = ("positive" if curr_pred_result > 0.5
                else "negative")

    logger.info("Inferencing has completed. \nText input: {} \nSentiment: {}",
                text_input, sentiment)
    st.write("The sentiment of the review is", sentiment, ".")

if __name__ == "__main__":
    main()
