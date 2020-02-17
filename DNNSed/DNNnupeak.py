from DNNBase import BaseCalculator, nu_bins
import os
import numpy as np


median_variances = [0.41651105, 0.50375067, 0.57480851, 0.6980996, 0.70062902, 0.74059361, 0.82359898, 0.70334238, 0.71769972, 0.69597561, 0.68775045, 0.69268567,
 0.74959257, 0.72729694, 0.73702109, 0.73718045, 0.73307117, 0., 0., 0.72000293, 0.73052439, 0.73981948, 0.76234908, 0.70161494,
 0.77692847, 0.7165665, 0.73114247, 0.80015174,0., 0.77041505, 0.73071954, 0.72916387, 0.74378204]
class NuPeakCalculator(BaseCalculator):
    def __init__(self, model_path='None', dec=None):
        if model_path == 'None':
            dirname = os.path.dirname(__file__)
            model_path = os.path.join(dirname, 'models/nu_peak')
        self.quantity = 'Nu-Peak'
        BaseCalculator.__init__(self, model_path, dec=dec)
        return

    def prepare_data(self, sed, exclude_nu_band=[], mask_catalog=['DEBL']):
        if len(sed['f4']) == 0:
            return None
        cat_nu_mask = np.array([True] * len(sed['f4']))
        for i in range(len(sed['f4'])):
            cat_bool = np.any([sed['f4'][i]==np.bytes_(j) for j in mask_catalog])
            nu_bool = np.any([((sed['f0'][i]>j[0]) & (sed['f0'][i]<j[1])) for j in exclude_nu_band])
            if np.any([cat_bool, nu_bool]):
                cat_nu_mask[i] = False
        sed = sed[(sed['f2'] != sed['f3']) & (sed['f3']>0) & (sed['f4'] != mask_catalog)]
        frequency = sed['f0']
        inds=np.sum(nu_bins<=frequency[:,np.newaxis], axis=1) - 1
        array=np.full((2, len(nu_bins)-1), 0.)
        for i in range(len(nu_bins)-1):
            tarray= sed['f1'][inds==i]
            tarray=tarray[tarray>0]
            if (len(tarray)==0):
                continue
            ret = np.log10(np.median(tarray))
            array[0,i] = ret / 10. + 2
            if len(tarray) < 2:
                array[1,i] = median_variances[i]
            else:
                if np.std(tarray) == 0:
                    array[1,i] =  median_variances[i]
                else:
                    array[1,i] =  np.log10(np.std(tarray)) /10. + 2
            array[np.isnan(array)] = 0
        return np.atleast_2d(array)[np.newaxis,:,:,np.newaxis]

