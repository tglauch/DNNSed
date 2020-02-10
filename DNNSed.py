import numpy as np
import keras
import keras.layers
import keras.backend as K
from keras.models import load_model
import keras.losses
import os
import warnings
def gaussian_nll(ytrue, ypreds):
    n_dims = int(int(ypreds.shape[1])/2)
    mu = ypreds[:, 0:n_dims]
    logsigma = ypreds[:, n_dims:]

    mse = -0.5*K.sum(K.square((ytrue-mu)/K.exp(logsigma)),axis=1)
    sigma_trace = -K.sum(logsigma, axis=1)
    log2pi = -0.5*n_dims*np.log(2*np.pi)

    log_likelihood = mse+sigma_trace+log2pi

    return K.mean(-log_likelihood)


nu_bins = [0,1e9,5*1e9,1*1e10,7.5*1e10, 1.8*1e11, 5*1e11, 1e13, 5*1e13, 1.58*1e14 ,3*1e14,
           3.97*1e14, 5*1e14, 6.3*1e14, 7.94*1e14, 1*1e15, 1.25*1e15, 1.58*1e15, 5*1e15, 5*1e16, 1*1e17,
           1.58*1e17, 2.5*1e17, 3.16*1e17, 3.98*1e17, 6.3*1e17, 8*1e17,
           1.26*1e18, 2.5*1e18, 1*1e19, 1*1e23, 1e24, 1e25, 1e26]
nu_bins = np.array(nu_bins)

sin_dec_bins = np.array([-1,-0.67, -0.42, -0.20, 0.02, 0.23, 0.45, 0.66,0.83, 1.])

class NuPeakCalculator(object):
    def __init__(self, model_path='None', dec=None):
        if model_path == 'None':
            dirname = os.path.dirname(__file__)
            model_path = os.path.join(dirname, 'models/')
        self.__model_path = model_path
        self.__models = [ [] for i in range(len(sin_dec_bins)-1)]
        if dec is None:
            for i in range(len(sin_dec_bins)-1):
                path = os.path.join(model_path, 'dec_'+str(i)+'.h5')
                print('Load Model {}'.format(path))
                self.__models[i] = load_model(path, custom_objects={'gaussian_nll': gaussian_nll})
        else:
            self.add_model(dec)
        return

    def add_model(self, dec):
        ind = self.get_model_pos_ind(dec)
        path = os.path.join(self.__model_path, 'dec_'+str(ind)+'.h5')
        print('Load Model {}'.format(path))
        self.__models[ind] = load_model(path, custom_objects={'gaussian_nll': gaussian_nll})
        return

    def prepare_data(self, sed, exclude_nu_band=[], mask_catalog=['DEBL']):
        cat_nu_mask = np.array([True] * len(sed['f4']))
        for i in range(len(sed['f4'])):
            cat_bool = np.any([sed['f4'][i]==np.bytes_(j) for j in mask_catalog])
            nu_bool = np.any([((sed['f0'][i]>j[0]) & (sed['f0'][i]<j[1])) for j in exclude_nu_band])
            if np.any([cat_bool, nu_bool]):
                cat_nu_mask[i] = False
        sed = sed[(sed['f2'] != sed['f3']) & (sed['f3']>0) & cat_nu_mask]
        frequency = sed['f0']
        inds=np.sum(nu_bins<=frequency[:,np.newaxis], axis=1) - 1
        array=np.full((len(nu_bins)-1)*2, 0.)
        for i in range(len(nu_bins)-1):
            tarray= sed['f1'][inds==i]
            if len(tarray)==0:
                continue
            ret = np.log10(np.median(tarray))
            if not np.isfinite(ret):
                continue
            array[i] = ret / 10.
            array[len(nu_bins)-1+i] =  np.var(np.log10(tarray)) /10.
            array[np.isnan(array)] = 0
        return np.atleast_2d(array)

    def get_model_pos_ind(self, dec):
        return (np.where(sin_dec_bins < np.sin(np.radians(dec)))[0][-1])

    def do_classification(self, sed_path, dec, exclude_nu_band=[], mask_catalog=['DEBL'],
                          return_sed=False, verbose=True):
        ''' dec in degrees '''
        idata = np.genfromtxt(sed_path, skip_header=4, usecols = [0,1,2,3,6],
                          dtype=[np.float, np.float, np.float, np.float, object])
        in_data = self.prepare_data(idata, mask_catalog=mask_catalog,
                                    exclude_nu_band=exclude_nu_band)
        model_ind = self.get_model_pos_ind(dec)
        if self.__models[model_ind] == []:
            warnings.warn("Model not yet loaded")
            print('Trying to load model..')
            self.add_model(dec)
        out = self.__models[model_ind].predict(in_data)[0]
        out[1] = np.exp(out[1])
        if verbose:
            print('Predict Nu-Peak of {} +- {}'.format(out[0], out[1]))
        if return_sed:
            return np.array([in_data[0][:len(nu_bins)-1], in_data[0][len(nu_bins)-1:]]), out
        else:
            return out


