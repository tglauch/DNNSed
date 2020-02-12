# Run as python simple_example.py --dec declination_of_the_source --sed_path path/to/the/sed/file

from DNNSed.DNNnupeak import NuPeakCalculator
import argparse

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sed_path", type=str)
    parser.add_argument(
        "--dec", type=float)
    args = parser.parse_args()
    return args

args = parseArguments()
nu_peak = NuPeakCalculator(dec=args.dec) #dec in degrees
nu_peak_res = nu_peak.do_classification(args.sed_path, dec=args.dec,
                                        exclude_nu_band=[],
                                        mask_catalog=['DEBL', 'SPIRE250',
                                                      'SPIRE350', 'SPIRE500'],
                                        return_sed = False, verbose=True)
