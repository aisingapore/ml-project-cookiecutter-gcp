"""This module contains functions for cleaning text data."""

import logging
import re
import string
import tensorflow as tf


logger = logging.getLogger(__name__)


def tag_punct_remover(input_text):
    """Does the following to a string:
    - lower case
    - remove punctuations
    - remove HTML tags

    Parameters
    ----------
    input_text : str
        String of characters.

    Returns
    -------
    tf.tensor
        Processed string converted into a tensor.
    """
    lowercase_text = tf.strings.lower(input_text)
    strip_html_text = tf.\
        strings.regex_replace(lowercase_text,
                            "<[^>]+>", " ")
    no_punct_text = tf.\
        strings.regex_replace(strip_html_text,
                            "[%s]" % re.escape(string.punctuation), " ")

    no_sing_charac_text = tf.\
        strings.regex_replace(no_punct_text,
                            "\s+[a-zA-Z]\s+", " ")

    sing_wspaced_text = tf.\
        strings.regex_replace(no_sing_charac_text,
                            "\s+", " ")

    return sing_wspaced_text


def process_file(file_path):
    """Reads in a text file and processes the text within it.

    Parameters
    ----------
    file_path : str
        String of characters.

    Returns
    -------
    tf.tensor
        Processed string converted into a tensor.
    """
    logger.debug("Reading text file: {}".format(file_path))
    with open(file_path, "r") as file:
        curr_txt = file.read()
    edit_text = tag_punct_remover(curr_txt)

    return edit_text
