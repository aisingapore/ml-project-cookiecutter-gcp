if [ -e env.sh ]; then
    source env.sh
fi
if [ -e secret ]; then
    source secret/secret.sh
fi
seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE