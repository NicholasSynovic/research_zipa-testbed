import multiprocessing as mp
import os
import time
import wave
from multiprocessing import shared_memory

import numpy as np
import pyaudio

from sensors.sensor_interface import SensorInterface


class Microphone(SensorInterface):
    def __init__(self, sample_rate, buffer_size, chunk_size, rms_filter_enabled=False):
        # When the RMS filter is enabled, the true sampling rate will be sample_rate/chunk_size.
        # Each chunk size will be converted into one sample by performing RMS on the chunk.
        SensorInterface.__init__(self)
        self.name = "mic"
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.chunk_size = chunk_size
        self.rms_filter_enabled = rms_filter_enabled
        self.format = pyaudio.paInt32
        self.pyaud = pyaudio.PyAudio()
        self.spl_sample_rate = self.sample_rate // self.chunk_size
        self.stream = self.pyaud.open(
            format=self.format,
            channels=1,  # Stereo audio
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.buffer_size,
        )

        # Data types will switch between using RMS filter or not, mostly because we have to be able to fit all the RMS data into a single datatype
        self.data_type = np.int32()
        if rms_filter_enabled:
            self.data_type = np.float64()

        self.start_thread()

    def start(self):
        # Start stream, recording for specified time interval
        self.stream.start_stream()

    def stop(self):
        self.buffer_ready.value = False
        self.stream.stop_stream()

    def calc_rms(self, signal):
        return np.array(
            np.sqrt(np.mean(signal.astype(np.int64()) ** 2)) / self.chunk_size,
            dtype=np.float64,
        )

    def read(self):
        output = self.stream.read(self.chunk_size)
        buf = np.frombuffer(output, dtype=np.int32)
        if self.rms_filter_enabled:
            buf = self.calc_rms(buf)
        return buf


# Test case
if __name__ == "__main__":
    from sensors.sensor_reader import Sensor_Reader

    mic = Microphone(120, 120 * 5, 120)
    sen_reader = Sensor_Reader(mic)
    time.sleep(3)
    print(sen_reader.read(240))
