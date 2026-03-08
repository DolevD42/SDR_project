#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 OmerAndDolev.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

BITS_PER_BYTE = 8

class PWDemodulator(gr.sync_block):
    """
    docstring for block PWDemodulator
    """ 

    NO_SIGNAL = -1
    def __init__(self, t=1,Fs=32000,sensetivity=1,timeout=5):
        gr.sync_block.__init__(self,
            name="PWDemodulator",
            in_sig=[np.float32, ],
            out_sig=None)
        
        self._t = t

        self._Fs = Fs

        self._Ts = int(t*Fs)
        print(f"Time: {t} Fs: {Fs} T: {self._Ts}")

        self._preamble = np.full(self._Ts, -1, dtype=np.float32)
        
        self._bits = np.zeros(BITS_PER_BYTE, dtype=int)
        self._curr_bit_idx = 0
        
        
        self._preamble_detect_threshold = sensetivity
        self._is_preamble_already_detected = False
        self._step_size = int(0.05 * self._Ts)
        self._steps_inserted = 0

        self._samples_buffer_detection = np.zeros(self._Ts, dtype=np.float32) 
        
        self._samples_data_buffer = np.zeros(3*self._Ts, dtype=np.float32)
        self._buffer_data_size = 3*self._Ts
        self._data_buffer_filled = 0

        self._data_threshold = 0.5

    def is_preamble(self) -> bool:
        match_filter_res = sum(self._samples_buffer_detection * self._preamble) / sum(abs(self._preamble)**2)
        return match_filter_res >= self._preamble_detect_threshold

    def extract_bit(self):
        middle_part = self._samples_data_buffer[self._Ts:2*self._Ts]

        if np.mean(middle_part) > self._data_threshold:
            return 1
        elif np.mean(middle_part) <  -self._data_threshold:
            return 0
        else:
            return PWDemodulator.NO_SIGNAL
	
    def decode_message(self) -> str:        
        binary_str = ''.join(self._bits.astype(str))       
        return  chr(int(binary_str, 2))
 

    def work(self, input_items, output_items):
        in0 = input_items[0]

        given_samples_amount = len(in0)
        idx_curr_sample = 0
        while given_samples_amount > 0:
            if not self._is_preamble_already_detected:
                if given_samples_amount >= (self._step_size-self._steps_inserted):                    
                    self._samples_buffer_detection = np.roll(self._samples_buffer_detection, -(self._step_size-self._steps_inserted))
                    self._samples_buffer_detection[-(self._step_size-self._steps_inserted):] = in0[idx_curr_sample:idx_curr_sample+(self._step_size-self._steps_inserted)]
        
                    # activate detection
                    if self.is_preamble():
                        self._is_preamble_already_detected = True
                    
                    given_samples_amount -= (self._step_size-self._steps_inserted)
                    idx_curr_sample += (self._step_size-self._steps_inserted)
                    self._steps_inserted = 0
                else:
                    self._samples_buffer_detection = np.roll(self._samples_buffer_detection, -given_samples_amount)
                    self._samples_buffer_detection[-given_samples_amount:] = in0[idx_curr_sample:]
                    self._steps_inserted += given_samples_amount
                    break
            else:
                if given_samples_amount >= (self._buffer_data_size-self._data_buffer_filled):
                    self._samples_data_buffer = np.roll(self._samples_data_buffer, -(self._buffer_data_size-self._data_buffer_filled))
                    self._samples_data_buffer[-(self._buffer_data_size-self._data_buffer_filled):] = in0[idx_curr_sample:idx_curr_sample+(self._buffer_data_size-self._data_buffer_filled)]

                    # check if there are 8 bits, and turn them to char    
                    given_samples_amount -= (self._buffer_data_size-self._data_buffer_filled)
                    idx_curr_sample += (self._buffer_data_size-self._data_buffer_filled)
                    self._data_buffer_filled = 0

                    data = self.extract_bit()
                    if data == PWDemodulator.NO_SIGNAL:    
                        self._preamble = np.full(self._Ts, -1, dtype=np.float32)
                        
                        self._bits = np.zeros(BITS_PER_BYTE, dtype=int)
                        self._curr_bit_idx = 0
                                                
                        self._is_preamble_already_detected = False
                        self._steps_inserted = 0

                        self._samples_buffer_detection = np.zeros(self._Ts, dtype=np.float32) 
                        
                        self._samples_data_buffer = np.zeros(3*self._Ts, dtype=np.float32)
                        self._data_buffer_filled = 0
                        print(f"***********waiting for new signal ***********")
                    
                    else:                    
                        self._bits[self._curr_bit_idx] = self.extract_bit()
                        self._curr_bit_idx += 1
                        
                        if self._curr_bit_idx == 8:
                            print(self.decode_message(), end = "")
                            self._curr_bit_idx = 0
                        

                else:
                    self._samples_data_buffer = np.roll(self._samples_data_buffer, -given_samples_amount)
                    self._samples_data_buffer[-given_samples_amount:] = in0[idx_curr_sample:idx_curr_sample+given_samples_amount]
                    self._data_buffer_filled += given_samples_amount
                    break


        return len(input_items[0])
    
