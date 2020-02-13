# DNNSed - A tool to auotmatically calculate nu-peak & redshift of blazars

The spectral energy distribution (SED) of blazars consinsts in an ideal case of two bumps where the first bump is due to synchroton emission of accelerated particles in the jet. Hence the position of the first bump, the nu-peak, provides important information about the nature and the energetics of the object. Whenever the non-thermal emission of the jet isn't too strong the SED also shows feactures from the hot gas in the galaxy and the accretion on the disk. While this is a background for the fit of the nu-peak it can be used to estimate the redshift of the object. This project provides an easy to use deep-learning based nu-peak estimator that has several advantages

- *Automatized* prediction of the nu-peak & redshift in less than 100ms per source (even on a CPU)
- *Stability* against sparse data and background emission features
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

for usage with the DNN classifier at least Frequency, nufnu, nufnu unc., and catalog must exist in the input file. If you haven't installed VOU Blazar it is recommended that you fetch the SED file directly from OpenUniverse (http://www.openuniverse.asi.it/).  After generation of the input file the nu-peak classification can be called as follows (also compare the script `simple_example.py` in `/examples/`)

```
from DNNSed.DNNnupeak import NuPeakCalculator
from DNNSed.DNNredshift import RedshiftCalculator


src_dec = declination_of_the_source_in_degrees
nu_peak = NuPeakCalculator(dec=src_dec)
redshift = RedshiftCalculator(dec=src_dec)

nu_peak = nu_peak.make_prediction(path_to_sed_file, dec=src_dec,
                                  exclude_nu_band=[], mask_catalog=['DEBL'],
                                  return_sed = False, verbose=True)

redshift = redshift.make_prediction(path_to_sed_file, dec=src_dec,
                                    exclude_nu_band=[], mask_catalog=['DEBL'],
                                    return_sed = False, verbose=True)
```

the nu_peak_res output variable contains two numbers 

```
nu_peak_res[0] --> estimated nu-peak
nu_peak_res[1] --> 68% uncertainty on the nu-peak
```
