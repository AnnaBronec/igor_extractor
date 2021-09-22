import json
import png
import os
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
    path = path.replace('ibw', '')
    path = path.replace('input', 'output')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = pformat(data).splitlines()            
    with open(f'{path}.txt', 'w') as writer: 
        writer.writelines([line + "\n" for line in lines])
        # json.dump(data, writer, indent=4)
    with open(f'{path}.json', 'w') as writer:
        json.dump(values, writer, indent=4)

def plot_data(values, total_time, path, list2=None):  
    listxachs=np.linspace(0, total_time, len(values))
    plt.plot(listxachs, values, linewidth=0.3, color="red")
    if list2 is not None:
        plt.plot(listxachs, list2, linewidth=0.3, color="blue", label="last")
    plt.xlabel("Time [min]",
            family = 'serif',
            color='black',
            weight = 'normal',
            size = 10,
            labelpad = 5)
    plt.ylabel("Voltage [mV]",
            family = 'serif',
            color='black',
            weight = 'normal',
            size = 10,
            labelpad = 5)
    #x = np.array([listxachs])
    #plt.xticks(np.arange(min(listxachs), max(listxachs)+1), 1)
    #plt.xlim(0, 15600040)
    #scale_factor = 1/20
    #xmin, xmax = plt.xlim()
    #plt.xlim(xmin * scale_factor, xmax * scale_factor)
    #plt.savefig('graph.png', dpi=300, bbox_inches='tight')
    path = path.replace('ibw','png')
    path = path.replace('input','output')  #input, ouput = foldernames
    plt.savefig(f'{path}')                 #only if you want to safe it
    plt.show()


@click.command()
@click.option('--path', help='specify the path and filename: "Data/<date>/<filename>"')
@click.option('--plot', default=True, help='show plot')
@click.option('--store', default=True, help='store data: stores complete data as txt and values as json.')
@click.option('--joined', default=False, help='join lists')
def run(path, plot, store, joined):
    # Extract complete data and values 
    data, values = extract_data(path)

    print("joined: ", joined)
    
    stacks = len(values[0])
    lists = len(values)
    DT = 5*10 ** -5

    seconds = lists * DT
    time = seconds / 60

    print(f"Elements in list: {stacks} \nNumber of lists: {lists}")

    flat_lists = [ list() for x in range(stacks)]
    for l in values:
        for i in range(stacks):
            flat_lists[i].append(l[i])
    joined_lists = [] 
    total_time=0
    for i in range(len(flat_lists)):
        joined_lists += flat_lists[i]
        total_time += time
    print ("Recording time :", total_time)
     
    # Store data:
    if store:
        store_data(path, data, values)
    # Plot data: 
    if plot and joined=="stacked":    
        plot_data(values, time, path)
    elif plot and joined=="in_a_row":
        plot_data(joined_lists, total_time, path)
    elif plot and joined=="first_last":
        plot_data(flat_lists[0], time, path, flat_lists[-1])
if __name__ == '__main__': 
    run()
