import numpy as np
import keras
import keras.layers
import keras.backend as K
from keras.models import load_model
import keras.losses
import os

def gaussian_nll(ytrue, ypreds):
    n_dims = int(int(ypreds.shape[1])/2)
    mu = ypreds[:, 0:n_dims]
    logsigma = ypreds[:, n_dims:]

    mse = -0.5*K.sum(K.square((ytrue-mu)/K.exp(logsigma)),axis=1)
    sigma_trace = -K.sum(logsigma, axis=1)
    log2pi = -0.5*n_dims*np.log(2*np.pi)

    log_likelihood = mse+sigma_trace+log2pi

    return K.mean(-log_likelihood)


nu_bins = [0,1e9,5*1e9,1*1e10,7.5*1e10, 1*1e11, 2.5*1e11, 5*1e11, 1*1e12, 1*1e13, 5*1e13, 1.58*1e14 ,3*1e14,
           3.97*1e14, 5*1e14, 6.3*1e14, 7.94*1e14, 1*1e15, 1.25*1e15, 1.58*1e15, 5*1e15, 5*1e16, 1*1e17,
           1.58*1e17, 2.5*1e17, 3.16*1e17, 3.98*1e17, 6.3*1e17, 8*1e17,
           1.26*1e18, 2.5*1e18, 1*1e19, 1*1e23, 1e24, 1e25, 1e26]

sin_dec_bins = np.array([-1,-0.67, -0.42, -0.20, 0.02, 0.23, 0.45, 0.66,0.83, 1.])

class NuPeakCalculator(object):
    def __init__(self, model_path='None'):
        if model_path == 'None':
            dirname = os.path.dirname(__file__)
            model_path = os.path.join(dirname, 'models/')
        self.__model_path = model_path
        self.__models = []
        for i in range(len(sin_dec_bins)-1):
            self.__models.append(load_model(os.path.join(model_path, 'dec_'+str(i)+'.h5'),
                                           custom_objects={'gaussian_nll': gaussian_nll}))
        return



    def prepare_data(self, sed, mask_catalog='DEBL'):
        sed = sed[(sed['f2'] != sed['f3']) & (sed['f3']>0) & (sed['f4'] != mask_catalog)]
        frequency = sed['f0']
        inds=np.sum(nu_bins<=frequency[:,np.newaxis], axis=1) - 1
        array=np.full(len(nu_bins)*2, 0.)
        for i in range(len(array)):
            tarray= sed['f1'][inds==i]
            if len(tarray)==0:
                continue
            ret = np.log10(np.median(tarray))
            if not np.isfinite(ret):
                continue
            array[i] = ret / 10.
            array[len(nu_bins)+i] =  np.var(np.log10(tarray)) /10.
            array[np.isnan(array)] = 0
        return np.atleast_2d(array) #np.concatenate([array, np.log10(nu_bins[1:])])


    def do_classification(self, sed_path, dec):
        ''' dec in degrees '''
        idata = np.genfromtxt(sed_path, skip_header=4, usecols = [0,1,2,3,6],
                          dtype=[np.float, np.float, np.float, np.float, object])
        in_data = self.prepare_data(idata)
        model_ind = np.where(np.sin(np.radians(dec))<sin_dec_bins)[0][0]
        out = self.__models[model_ind - 1].predict(in_data)[0]
        out[1] = np.exp(out[1])
        print('Predict Nu-Peak of {} +- {}'.format(out[0], out[1]))
        return out 
 

