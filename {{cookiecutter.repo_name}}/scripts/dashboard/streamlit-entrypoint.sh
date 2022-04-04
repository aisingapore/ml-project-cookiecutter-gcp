#!/bin/bash

set -x

source ~/.bashrc >/dev/null
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

if [ ! -d "$PRED_MODEL_PATH" ]; then
    gsutil cp -r $PRED_MODEL_GCS_URI $HOME/from-gcs
fi

streamlit run src/streamlit.py -- inference.model_path=$PRED_MODEL_PATH
