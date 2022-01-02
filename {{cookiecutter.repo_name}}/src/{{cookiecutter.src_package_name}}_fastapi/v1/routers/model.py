import logging
import fastapi

import {{cookiecutter.src_package_name}}_fastapi as {{cookiecutter.src_package_name_short}}_fapi


logger = logging.getLogger(__name__)


ROUTER = fastapi.APIRouter()
PRED_MODEL = {{cookiecutter.src_package_name_short}}_fapi.deps.PRED_MODEL


@ROUTER.post("/predict", status_code=fastapi.status.HTTP_200_OK)
def predict_sentiment(movie_reviews_json: {{cookiecutter.src_package_name_short}}_fapi.schemas.MovieReviews):
    """Endpoint that returns sentiment classification of movie review
    texts.

    Parameters
    ----------
    movie_reviews_json : {{cookiecutter.src_package_name_short}}_fapi.schemas.MovieReviews
        'pydantic.BaseModel' object detailing the schema of the request
        body

    Returns
    -------
    dict
        Dictionary containing the sentiments for each movie review in
        the body of the request.

    Raises
    ------
    fastapi.HTTPException
        A 500 status error is returned if the prediction steps
        encounters any errors.
    """
    result_dict = {"data": []}

    try:
        logger.info("Generating sentiments for movie reviews.")
        movie_reviews_dict = movie_reviews_json.dict()
        review_texts_array = movie_reviews_dict["reviews"]
        for review_val in review_texts_array:
            curr_pred_result = PRED_MODEL.predict([review_val["text"]])
            sentiment = ("positive" if curr_pred_result > 0.5
                        else "negative")
            result_dict["data"].append(
                {"review_id": review_val["id"], "sentiment": sentiment})
            logger.info(
                "Sentiment generated for Review ID: {}".
                format(review_val["id"]))

    except Exception as error:
        print(error)
        raise fastapi.HTTPException(
            status_code=500, detail="Internal server error.")

    return result_dict


@ROUTER.get("/version", status_code=fastapi.status.HTTP_200_OK)
def get_model_version():
    """Get version (UUID) of predictive model used for the API.

    Returns
    -------
    dict
        Dictionary containing the UUID of the predictive model being
        served.
    """
    return {"data": {"model_uuid": {{cookiecutter.src_package_name_short}}_fapi.config.SETTINGS.PRED_MODEL_UUID}}
