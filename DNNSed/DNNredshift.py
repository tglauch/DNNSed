from DNNBase import BaseCalculator
import os

class RedshiftCalculator(BaseCalculator):
    def __init__(self, model_path='None', dec=None):
        if model_path == 'None':
            dirname = os.path.dirname(__file__)
            model_path = os.path.join(dirname, 'models/redshift')
        self.quantity = 'Redshift'
        BaseCalculator.__init__(self, model_path, dec=dec)
        return



