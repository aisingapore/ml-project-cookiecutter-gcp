import logging
import fastapi
from fastapi.middleware.cors import CORSMiddleware

import {{cookiecutter.src_package_name}} as {{cookiecutter.src_package_name_short}}
import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi


LOGGER = logging.getLogger(__name__)
LOGGER.info("Setting up logging configuration.")
{{cookiecutter.src_package_name_short}}.general_utils.setup_logging(
    logging_config_path={{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.LOGGER_CONFIG_PATH)

API_V1_STR = {{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.API_V1_STR
APP = fastapi.FastAPI(
    title={{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.API_NAME,
    openapi_url=f"{API_V1_STR}/openapi.json")
API_ROUTER = fastapi.APIRouter()
API_ROUTER.include_router(
    {{cookiecutter.src_package_name_short}}_fapi.v1.routers.model.ROUTER, prefix="/model", tags=["model"])
APP.include_router(
    API_ROUTER, prefix={{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.API_V1_STR)

ORIGINS = ["*"]

APP.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
