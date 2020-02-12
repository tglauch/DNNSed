# DNNSed

The spectral energy distribution (SED) of blazars consinsts in an ideal case of two bumps where the first bump is due to synchroton emission of accelerated particles in the jet. Hence the position of the first bump, the nu-peak, provides important information about the nature and the energetics of the object. In most real world examples fitting the nu-peak is somewhat challenging due to sparse data and the background emission of the galaxy and the accretion of the disk. This project provides an easy to use deep-learning based nu-peak estimator that has several advantages

- *Automatized* prediction of the nu-peak in less than 100ms per source (even on a CPU)
- *Stability* against sparse data and background emission
- *Reliable* error estimation


# How to install

The package can be easily installed using the pip package manager 

```pip install git+https://github.com/tglauch/DNNSed```

Alternatively download the package and run python install

``` 
git clone https://github.com/tglauch/DNNSed
cd DNNSed
python setup.py install
```

# How to use

DNNSed is optimized for the usage with input files as produced by the VOU-Blazar Tool. The corresponding syntax is

```
 Frequency     nufnu     nufnu unc.  nufnu unc. start time   end time   Catalog     Reference
    Hz       erg/cm2/s     upper       lower        MJD         MJD  
```

for usage with the DNN classifier at least Frequency, nufnu, nufnu unc., and catalog must exist in the input file. After generation of the input file the nu-peak classification can be called as follows

```
from DNNSed.DNNnupeak import NuPeakCalculator 
nu_peak = NuPeakCalculator(src_dec)
nu_peak_res = nu_peak.do_classification(sed_file_path, dec=src_dec,
                                        exclude_nu_band=[],
                                        mask_catalog=['DEBL', 'SPIRE250',
                                                      'SPIRE350', 'SPIRE500'],
                                        return_sed = False, verbose=True)
```

the nu_peak_res output variable contains two numbers 

```
nu_peak_res[0] --> estimated nu-peak
nu_peak_res[1] --> 68% uncertainty on the nu-peak
```
