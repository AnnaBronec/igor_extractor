import json
import os.path
import numpy as np
from pprint import pformat

import click
from matplotlib import pyplot as plt
from igor.binarywave import load as loadibw


def extract_data(path):
    data = loadibw(path)
    wave = data['wave']
    values = np.nan_to_num(wave['wData']).tolist()
    del data['wave']['wData']
    return (data, values)

def store_data(path, data, values): 
    path.replace('ibw', '')
    path = path.replace('input', 'output')
    lines = pformat(data).splitlines()
    with open(f'{path}.txt', 'w') as writer:
        writer.writelines([line + "\n" for line in lines])
        # json.dump(data, writer, indent=4)
    with open(f'{path}.json', 'w') as writer:
        json.dump(values, writer, indent=4)

def plot_data(values):
    plt.plot(values)
    plt.show()


@click.command()
@click.option('--path', help='specify the path and filename: "Data/<date>/<filename>"')
@click.option('--plot', default=True, help='show plot')
@click.option('--store', default=True, help='store data: stores complete data as txt and values as json.')
def run(path, plot, store):
    # Extract complete data and values 
    data, values = extract_data(path)

    # Store data:
    if store:
        store_data(path, data, values)

    # Plot 
    if plot:
        plot_data(values)

if __name__ == '__main__': 
    run()
