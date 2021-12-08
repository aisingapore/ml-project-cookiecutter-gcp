import logging

import metrics

class Model(object):
    """
    Model template.
    Ensure that the name of the model class is the same as the name of 
    the file.
    Also ensure that the name of the model called in the Dockerfile is
    the same as the name of the file.

    You can do whatever modifications in this class, so long as it is 
    compatible with the deployment wrappers (Seldon Core, BentoML, 
    etc). The methods written in this class is just a guideline on what
    you may need during deployment.
    """

    def __init__(self):
        """
        Add any extra initialisation parameters.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        self._metrics = {}

        # Update your custom metric updates in metrics.py
        self.metric_funcs = {
            i:j for i, j in metrics.__dict__.items()
            if callable(j)
        }

        # Load your model here
        class DummyModel:
            def predict(self, var):
                return var
        self._model = DummyModel()

    def predict(self, var, meta=None):
        """
        Returns a prediction.

        Parameters
        ----------
        var:    Any
                Values to be sent to the model.
        meta:   Any
                Metadata of the values sent, might be used to modify
                the output.
        
        Returns
        -------
        output: Any
                Output of the model
        """
        output = self._model.predict(var)

        return output

    """
    Methods below are deemed to be static and not expected to be 
    modified by the template user.
    """

    def metrics_update(self, metric, value=0):
        """
        Updates your metrics.

        Parameters
        ----------
        metric: string
                Name of the metric to be updated
        value:  int, float
                Number to modify the metric
        
        Returns
        -------
        None.
        """
        if metric in self.metric_funcs.keys():
            self.metrics[metric] = self.metric_funcs[metric](
                value, self.metrics.get(metrics, 0)
            )
            self.logger.info(
                f"Updating {metric}, new value: {self.metrics[value]}"
            )
        else:
            self.metric_funcs[metric] = lambda value: value
            self.metrics[metric] = self.metric_funcs[metric](value)
            self.logger.warn(
                f"Unknown metric: {metric}. " +\
                f"Setting {metric} with {value}."
            )

    @property
    def metrics(self):
        """
        Metrics to track the model.
        """
        return self._metrics

    @property
    def name(self):
        """
        Returns the name of this class.
        """
        return type(self).__name__


