import os
import logging
import pathlib
import re
import hydra
import tensorflow as tf

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}


@hydra.main(config_path="../conf/base", config_name="pipelines.yml")
def main(args):
    """Main programme to read in raw data files and process them.
    """

    logger = logging.getLogger(__name__)
    logger.info("Setting up logging configuration.")
    logger_config_path = os.path.\
        join(hydra.utils.get_original_cwd(),
            "conf/base/logging.yml")
    {{cookiecutter.src_package_name_short}}.general_utils.setup_logging(logger_config_path)

    raw_data_dirs_list = args["data_prep"]["raw_dirs_paths"]
    processed_data_path = args["data_prep"]["processed_data_path"]

    for raw_data_dir in raw_data_dirs_list:

        raw_data_dir = os.path.join(
            hydra.utils.get_original_cwd(), raw_data_dir)
        processed_data_path = os.path.join(
            hydra.utils.get_original_cwd(), processed_data_path)

        logger.info("Processing raw text files from: \'{}\'.".
                    format(raw_data_dir))
        txt_files_list = pathlib.Path(raw_data_dir).rglob("*.txt")

        for filename in txt_files_list:
            try:
                logger.debug("Processing text file: {}".
                            format(filename))
                curr_edit_text = {{cookiecutter.src_package_name_short}}.\
                    data_prep.process_text.process_file(filename)

                out_filename = re.sub(
                    raw_data_dir, processed_data_path, str(filename))

                os.makedirs(os.path.dirname(out_filename), exist_ok=True)
                tf.io.write_file(
                    out_filename, curr_edit_text)
                logger.debug("Processed text file exported: {}".
                            format(out_filename))
            except:
                logger.error("Error encountered while processing file: {}".
                            format(filename))

    logging.info("Data preparation pipeline has completed.")


if __name__ == "__main__":
    main()
