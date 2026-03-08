#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 OmerAndDolev.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class PWModulator(gr.sync_block):
    """
    docstring for block PWModulator
    """
    def __init__(self, t = 1,Fs = 32000, msg = "Hello World"):
        gr.sync_block.__init__(self,
            name="PWModulator",
            in_sig=None,
            out_sig=[np.float32, ])
        
        self._t = t
        self._Fs = Fs
        self._msg = msg
        self._queue = self._enqueue_from_string(self._msg)
        self._curr_idx = 0

    
    def _enqueue_from_string(self, message: str) -> np.float32:
        msg_bytes = message.encode("UTF_8")
        bytes_arr = np.frombuffer(msg_bytes, dtype = np.uint8)
        msg_bits = np.unpackbits(bytes_arr)
        
        samples_per_t = self._t *  self._Fs


        output_length = samples_per_t * (1 + 3*len(msg_bits))
        output = np.full(output_length, -1, dtype = np.float32)

        output_curr_idx = samples_per_t # skip the preamble
        for bit in msg_bits:
            if bit == 0:
                output[output_curr_idx: output_curr_idx + samples_per_t] = 1
            else:
                output[output_curr_idx : output_curr_idx + 2*samples_per_t] = 1

            output_curr_idx += 3*samples_per_t


        return output




    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        
        out[:] = self._queue[self._curr_idx : self._curr_idx + len(out)]
        self._curr_idx += len(out)

        return len(output_items[0])
