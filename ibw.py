import os.path
from matplotlib import pyplot as plt
import numpy as np
from igor.binarywave import load as loadibw

import util

def extract(filename):
    data = loadibw(filename)
    wave = data['wave']
    wData = np.nan_to_num(wave['wData']).tolist()
    return wData
