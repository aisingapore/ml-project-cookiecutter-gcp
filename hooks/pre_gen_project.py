import re
import sys


COOKIE_INPUTS = {
    "project_name": {
        "user_input": "{{cookiecutter.project_name}}",
        "regex": r"^[a-zA-Z0-9_]+(?:_? [a-zA-Z0-9]+)*$"},
    "description": {
        "user_input": "{{cookiecutter.description}}"},
    "repo_name": {
        "user_input": "{{cookiecutter.repo_name}}",
        "regex": r"^[a-z](?:-?[a-z0-9]+)*$"},
    "src_package_name": {
        "user_input": "{{cookiecutter.src_package_name}}",
        "regex": r"^[a-z](?:_?[a-z0-9]+)*$"},
    "src_package_name_short": {
        "user_input": "{{cookiecutter.src_package_name_short}}",
        "regex": r"^[a-z](?:_?[a-z0-9]+)*$"},
    "gcp_project_id": {
        "user_input": "{{cookiecutter.gcp_project_id}}",
        "regex": r"^[a-z0-9](?:-?[a-z0-9]+)*$"},
    "author_name": {
        "user_input": "{{cookiecutter.author_name}}"},
    "open_source_license": {
        "user_input": "{{cookiecutter.open_source_license}}"}
}

ERROR_MSG_LIST = []


def check_input_length(cookie_input_key, cookie_input_val):

    input_val = cookie_input_val["user_input"].strip()
    if len(input_val) not in range(1, 73):
        ERROR_MSG_LIST.append("ERROR: %s - '%s' is not of valid length (1 to 72)."
            % (cookie_input_key, cookie_input_val["user_input"]))


def check_input_regex(cookie_input_key, cookie_input_val):

    if not re.match(cookie_input_val["regex"], cookie_input_val["user_input"]):

        if cookie_input_key == "project_name":
            ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid project name. Please use only alphanumeric characters."
                % (cookie_input_key, cookie_input_val["user_input"]))

        if cookie_input_key == "repo_name":
            ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid repository name. Only alphanumeric characters and hyphens are permitted."
                % (cookie_input_key, cookie_input_val["user_input"]))

        if cookie_input_key in ["src_package_name", "src_package_name_short"]:
            ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid Python package name."
                % (cookie_input_key, cookie_input_val["user_input"]))

        if cookie_input_key == "gcp_project_id":
            ERROR_MSG_LIST.append("ERROR: %s - '%s' is not a valid GCP project ID."
                % (cookie_input_key, cookie_input_val["user_input"]))


def check_cookiecutter_inputs():

    for cookie_input_key, cookie_input_val in COOKIE_INPUTS.items():

        check_input_length(cookie_input_key, cookie_input_val)
        if "regex" in cookie_input_val:
            check_input_regex(cookie_input_key, cookie_input_val)

    if len(ERROR_MSG_LIST) > 0:

        for error_msg in ERROR_MSG_LIST:
            print(error_msg)
        sys.exit(1)

check_cookiecutter_inputs()
