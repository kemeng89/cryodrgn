'''tSNE dimensionality reduction'''

import argparse
import numpy as np
import sys, os
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.manifold import TSNE

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Input z.pkl')
    parser.add_argument('--stride', type=int, help='Stride the dataset')
    parser.add_argument('-p', default=50.0, type=float, help='Perplexity (default: %(default)s)')
    parser.add_argument('-o', help='Output pickle')
    return parser
def main(args):
    z = pickle.load(open(args.input,'rb'))
    if args.stride:
        z = z[::args.stride]
    print(z.shape)
    z_embedded = TSNE(n_components=2, perplexity=args.p).fit_transform(z)
    pickle.dump(z_embedded, open(args.o,'wb'))

if __name__ == '__main__':
    main(parse_args().parse_args())
