import logging
import time
import json

from Model import Model

class SeldonWrapper:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.name)

        self._model = Model(*args, **kwargs)

    def metrics(self):
        return [{
            "type": "GAUGE", "key": key, "value": value
        } for key, value in self.model.metrics.items()]

    def predict(self, X, features_name=None):
        """
        Return a prediction.

        Parameters
        ----------
        X : string, byte, ndarray or list of primitive types
            input to model
        feature_names : None
            leave as None

        Returns
        -------
        y: string, byte, ndarray or list of primitive types
            output of model
        """

        model_start_time = time.process_time()
        self.verify_dtype(X)
        X = self.preprocess(X)
        self.logger.info("Predicting...")
        y = self.model.predict(X)
        y = self.postprocess(y)
        self.verify_dtype(y)
        self.model.metrics_update(
            "model_latency_seconds",
            time.process_time() - model_start_time
        )
        
        return y

    def preprocess(self, X):
        return X

    def postprocess(self, y):
        return y

    def send_feedback(
        self, request=None, response=None, 
        reward=None, truth=None, routing=None
    ):
        """
        Provide feedback to indicate the performance of the model.
        Note: This is copied directly from Kapitan Scout and haven't 
              been vetted yet

        Parameters
        ----------
        request: string, byte, ndarray or list of primitive types
            Input to model
        response: raw protobuf message
            The raw REST API response from the prediction request.
            inputted within feedback REST API request, where it is
            used by router function to route the send_feedback to the 
            correct model. (The response from a prediction will contain 
            info on which model made the prediction.)            
            this variable does not appear within send_feedback function
        reward: int(1) or int(0)
            reward for the model
            1: model made a 'good' prediction
            0: model made a 'bad' prediction
            inputted within feedback REST API request, where it is
            used by router function to route the send_feedback to the 
            correct model. (The response from a prediction will contain 
            info on which model made the prediction.)
            this variable does not appear within send_feedback function
        reward: int(1) or int(0)
            reward for the model
            1: model made a 'good' prediction
            0: model made a 'bad' prediction
            inputted within feedback REST API request, where it is
            used by router function to route predictions to models with 
            higher reward scores.
            this variable does not appear within send_feedback function
        truth: string, byte, ndarray or list of primitive types
            output of the model
        """
        if not self.loaded_feedback:
            self.correct_feedback = 0
            self.wrong_feedback = 0
            self.loaded_feedback = True
            self.logger.info("Loading feedback for the first time...")

        self.logger.info("Sending Feedback...")

        X_test = request
        y_test = truth
        X_test = self.preprocess(X_test)
        y_pred = self.model.predict(X_test)
        y_pred = self.postprocess(y_pred)

        # Uncomment if using numpy
        # if type(y_pred) == np.ndarray:
        #     y_pred = y_pred.tolist()
        # if type(y_test) == np.ndarray:
        #     y_test = y_test.tolist()
        # self.logger.info(
        #     f"y_pred:{type(y_pred)} {y_pred}, y_test:{type(y_test)} " +\
        #     f"{y_test}, y_pred==y_test:{y_pred==y_test}"
        # )

        if y_pred == y_test:
            self.correct_feedback += 1
            self.logger.info(
                f"updated correct feedback:{self.correct_feedback}"
            )
        else:
            self.wrong_feedback += 1

        acc = self.correct_feedback/(self.correct_feedback+self.wrong_feedback)
        self.logger.info(f"updated correct feedback:{acc}")
        self.model.metrics_update("model_accuracy_rate", acc)
        return acc

    def verify_dtype(self, X):
        """
        Verifies that data can be transferred using REST API
        """

        # You can add np.ndarray if you have imported numpy
        valid_dtypes  = (str, bytes, list, dict)
        dtype_err_msg = "Invalid datatype for REST API request. " +\
            "Accepted datatypes are str, bytes, list, dict, np.ndarray"
        cont_err_msg  = "Invalid datatpye for REST API request. " +\
            "list or dict can only contain primitive datatypes"
        
        if type(X) not in valid_dtypes:
            raise TypeError(dtype_error_msg)
        elif type(X)==list or type(X)==dict:
            try:
                json.dumps(X)
            except:
                raise TypeError(cont_err_msg)
        else:
            return True

    @property
    def model(self):
        return self._model

    @property
    def name(self):
        """
        Returns the name of this class.
        """
        return type(self).__name__
