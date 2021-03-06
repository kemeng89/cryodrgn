'''Parse CTF parameters from a RELION .star file'''

import argparse
import numpy as np
import sys, os
import pickle

sys.path.insert(0, '{}/../lib-python'.format(os.path.dirname(os.path.realpath(__file__))))
import utils
import starfile
import ctf
log = utils.log 

HEADERS = ['_rlnDefocusU', '_rlnDefocusV', '_rlnDefocusAngle', '_rlnVoltage', '_rlnSphericalAberration', '_rlnAmplitudeContrast', '_rlnPhaseShift']

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('star', help='Input')
    parser.add_argument('--Apix', type=float, required=True, help='Angstroms per pixel')
    parser.add_argument('-D', type=int, required=True, help='Image size in pixels')
    parser.add_argument('-o', type=os.path.abspath, required=True, help='Output pkl of CTF parameters')
    parser.add_argument('--png', metavar='PNG', type=os.path.abspath, help='Optionally plot the CTF')

    group = parser.add_argument_group('Overwrite CTF parameters')
    group.add_argument('--kv', type=float, help='Accelerating voltage (kV)')
    group.add_argument('--cs', type=float, help='Spherical abberation (mm)')
    group.add_argument('-w', type=float, help='Amplitude contrast ratio')
    return parser

def main(args):
    assert args.star.endswith('.star'), "Input file must be .star file"
    assert args.o.endswith('.pkl'), "Output CTF parameters must be .pkl file"
    
    s = starfile.Starfile.load(args.star)
    N = len(s.df)
    log('{} particles'.format(N))
    
    overrides = {}
    if args.kv is not None:
        log(f'Overriding accerlating voltage with {args.kv} kV')
        overrides[HEADERS[3]] = args.kv
    if args.cs is not None:
        log(f'Overriding spherical abberation with {args.cs} mm')
        overrides[HEADERS[4]] = args.cs
    if args.w is not None:
        log(f'Overriding amplitude contrast ratio with {args.w}')
        overrides[HEADERS[5]] = args.w

    ctf_params = np.zeros((N, 9))
    ctf_params[:,0] = args.D
    ctf_params[:,1] = args.Apix
    for i,header in enumerate(['_rlnDefocusU', '_rlnDefocusV', '_rlnDefocusAngle', '_rlnVoltage', '_rlnSphericalAberration', '_rlnAmplitudeContrast', '_rlnPhaseShift']):
        ctf_params[:,i+2] = s.df[header] if header  not in overrides else overrides[header]
    log('CTF parameters for first particle:')
    ctf.print_ctf_params(ctf_params[0])
    log('Saving {}'.format(args.o))
    with open(args.o,'wb') as f:
        pickle.dump(ctf_params.astype(np.float32), f)
    if args.png:
        import matplotlib.pyplot as plt
        assert args.D, 'Need image size to plot CTF'
        ctf.plot_ctf(args.D, args.Apix, ctf_params[0,2:])
        plt.savefig(args.png)
        log(args.png)
    

if __name__ == '__main__':
    main(parse_args().parse_args())
