import sys
import os
sys.path.insert(1, os.getcwd() + "/../src/")

import math
import random
import numpy as np
import pandas as pd
from eval_tools import *
from protocols.shurmann import Shurmann_Siggs_Protocol

def shurmann_wrapper_func(arr, window_length, band_len):
    return Shurmann_Siggs_Protocol.sigs_algo(None, arr, window_len=window_length, bands=band_len)

def generate_bits(sf, bit_length, window_length, band_length, max_samples):
    samples_per_key = (
            math.ceil(
                ((bit_length) / int((window_length / 2 + 1) / band_length))
                + 1
            )
            * window_length
        )

    number_of_keys = max_samples // samples_per_key
    keys_generated = []
    for i in range(number_of_keys):
        samples = sf.read(samples_per_key)
        key = shurmann_wrapper_func(samples, window_length, band_length)
        keys_generated.append(key)
    return keys_generated, samples_per_key

def experiment(data_from_devices, ids, iterations, max_samples):
    bit_length = 128            # Hardcoded to always try to produce keys of a certain length

    file_name = f"shurmann_dev1_{ids[0]}_dev2_{ids[1]}.csv"

    # Min and Max values are arbitrary but somewhat relistic potential choices window_length
    min_window_length = 5000
    max_window_length = 48000*5
    min_band_length = 1

    for i in range(iterations):
        window_length = 147371 #random.randint(min_window_length, max_window_length)
        band_len = 31946 #random.randint(min_band_length, window_length // 2)

        device_bits = []
        samples_per_key = None
        for sf in data_from_devices:
            bits, samples_per_key = generate_bits(sf, bit_length, window_length, band_len, max_samples)
            device_bits.append(bits)
            sf.reset()
        avg_bit_err = get_average_bit_err(device_bits[0], device_bits[1], bit_length)
        min_entropy1_1bit = get_min_entropy(device_bits[0], bit_length, 1)
        min_entropy2_1bit = get_min_entropy(device_bits[1], bit_length, 1)
        min_entropy1_4bit = get_min_entropy(device_bits[0], bit_length, 4)
        min_entropy2_4bit = get_min_entropy(device_bits[1], bit_length, 4)
        min_entropy1_8bit = get_min_entropy(device_bits[0], bit_length, 8)
        min_entropy2_8bit = get_min_entropy(device_bits[1], bit_length, 8)
        
        results = {"Window Length": [window_length], 
                   "Band Length": [band_len], 
                   "Samples Per Key": [samples_per_key], 
                   "Average Bit Error": [avg_bit_err],  
                   "Min Entropy Device 1 Symbol Size 1 Bit": [min_entropy1_1bit], 
                   "Min Entropy Device 2 Symbol Size 1 Bit": [min_entropy2_1bit], 
                   "Min Entropy Device 1 Symbol Size 4 Bit": [min_entropy1_4bit], 
                   "Min Entropy Device 2 Symbol Size 4 Bit": [min_entropy2_4bit], 
                   "Min Entropy Device 1 Symbol Size 8 Bit": [min_entropy1_8bit], 
                   "Min Entropy Device 2 Symbol Size 8 Bit": [min_entropy2_8bit]}
        
        df = pd.DataFrame(results)
        df.to_csv(file_name, mode="a", index=False, header=(not os.path.isfile(file_name)))
        quit()


def perform_eval():
    iterations = 100
    max_samples = 48000*3600//2
    signal_directory = "/mnt/data/"
    file_name1 = "mic_id_10.0.0.231_date_2024062000.csv"
    file_name2 = "mic_id_10.0.0.232_date_2024062000.csv"
    sf1 = Signal_File(signal_directory, file_name1)
    sf2 = Signal_File(signal_directory, file_name2)
    
    ids = ["10.0.0.231", "10.0.0.232"]

    data_from_devices = [sf1, sf2]
    experiment(data_from_devices, ids, iterations, max_samples)
            
if __name__ == "__main__":
    perform_eval()
