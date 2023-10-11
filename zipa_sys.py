from network import Ad_Hoc_Network
from corrector import Reed_Solomon
from galois import *
from shurmann import sigs_algo
from microphone import Microphone
import time
import sys
import numpy as np

class ZIPA_System():
    def __init__(self, identifier, is_host, ip, other_ip, nfs_server_dir, sample_rate, seconds, exp_name, n, k):
        self.identifier = identifier
        self.ip = ip
        self.other_ip = other_ip
        self.nfs_server_dir = nfs_server_dir
        self.sample_rate = sample_rate
        self.seconds = seconds
        self.net = Ad_Hoc_Network(ip, other_ip, is_host)
        self.signal_measurement = Microphone(sample_rate, int(seconds*sample_rate)) 
        self.re = Reed_Solomon(n, k)
        self.exp_name = exp_name
        self.count = 0

    def send_to_nfs_server(self, signal_type, signal, bits, meta_data):
        root_file_name = self.nfs_server_dir + "/" + signal_type
        signal_file_name = root_file_name + "_signal_id" + str(self.identifier) + "_it" + str(self.count) + ".csv"
        bit_file_name = root_file_name + "_bits_id" + str(self.identifier) + "_it" + str(self.count) + ".csv"
        np.savetxt(signal_file_name, signal)
        np.savetxt(bit_file_name, bits)
 
    def extract_context(self):
        print()
        print("Extracting Context")
        signal = self.signal_measurement.get_audio()
        bits = sigs_algo(signal)
        print()
        return bits, signal

    def bit_agreement_exp_dev(self): 
        while (1):
            # Wait for start from host
            self.net.get_start()
            
            # Sending ack that they can start
            self.net.send_ack()

            # Extract bits from mic
            bits, signal = self.extract_context()

            # Send bits to compare agreement rate
            self.net.send_bits(bits)

            # Wait for Codeword
            C = self.net.get_codeword(8192)

            # Decode Codeword
            dec_C = self.re.decode_message(C, bits)

            # Send Authentication Token
            self.net.send_auth_token(dec_C)

            self.send_to_nfs_server("audio", signal, bits, None)

    def bit_agreement_exp_host(self):
        while (1):
            # Send start to device
            self.net.send_start()
            
            # Get Ack to make sure it isn't lagging from the previous iteration
            self.net.get_ack()

            # Extract key from mic
            bits, signal = self.extract_context()

            # Recieve bits to compare agreement rate
            other_bits = self.net.get_bits(len(bits))

            # Create Codeword
            auth_tok, C = self.re.encode_message(bits)
  
            # Sending Codeword
            self.net.send_codeword(C)

            # Recieve Authentication Token
            other_auth_tok = self.net.get_auth_token(8192)

            self.send_to_nfs_server("audio", signal, bits, None)
