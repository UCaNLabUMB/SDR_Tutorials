#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time




class Final_Packet_Error_Test_TX_B200(gr.top_block):

    def __init__(self, gain_factor_tx=60, multiply_constant_=0.08, tx_addr_0='32794C9'):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.gain_factor_tx = gain_factor_tx
        self.multiply_constant_ = multiply_constant_
        self.tx_addr_0 = tx_addr_0

        ##################################################
        # Variables
        ##################################################
        self.packet_len = packet_len = 50
        self.OC_low = OC_low = (list(range(-12, -2)),)
        self.sync_word2 = sync_word2 = [0j, 0j, 0j, 0j, 0j, 0j, (-1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1 +0j), (1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), 0j, (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j), (-1+0j), (-1+0j), 0j, 0j, 0j, 0j, 0j]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.samp_rate = samp_rate = 500000
        self.pilot_symbols = pilot_symbols = ((-1,1),)
        self.pilot_carriers = pilot_carriers = ((-15,-1),)
        self.occupied_carriers = occupied_carriers = OC_low
        self.len_tag_key = len_tag_key = packet_len
        self.fft_len = fft_len = 64
        self.OC_high = OC_high = (list(range(-22, -12)),)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('"serial=" + tx_addr', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0.set_center_freq(915000000, 0)
        self.uhd_usrp_sink_0.set_antenna('TX', 0)
        self.uhd_usrp_sink_0.set_gain(gain_factor_tx, 0)
        self.digital_ofdm_tx_0_0 = digital.ofdm_tx(
            fft_len=64,
            cp_len=fft_len//4,
            packet_length_tag_key='packet_len',
            occupied_carriers=occupied_carriers,
            pilot_carriers=pilot_carriers,
            pilot_symbols=pilot_symbols,
            sync_word1=None,
            sync_word2=None,
            bps_header=1,
            bps_payload=1,
            rolloff=0,
            debug_log=False,
            scramble_bits=False)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, "packet_len")
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(multiply_constant_)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/christopher/Desktop/DataCollection/out', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0_0, 0))
        self.connect((self.digital_ofdm_tx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def get_gain_factor_tx(self):
        return self.gain_factor_tx

    def set_gain_factor_tx(self, gain_factor_tx):
        self.gain_factor_tx = gain_factor_tx
        self.uhd_usrp_sink_0.set_gain(self.gain_factor_tx, 0)

    def get_multiply_constant_(self):
        return self.multiply_constant_

    def set_multiply_constant_(self, multiply_constant_):
        self.multiply_constant_ = multiply_constant_
        self.blocks_multiply_const_vxx_0.set_k(self.multiply_constant_)

    def get_tx_addr_0(self):
        return self.tx_addr_0

    def set_tx_addr_0(self, tx_addr_0):
        self.tx_addr_0 = tx_addr_0

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.set_len_tag_key(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_OC_low(self):
        return self.OC_low

    def set_OC_low(self, OC_low):
        self.OC_low = OC_low
        self.set_occupied_carriers(self.OC_low)

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len

    def get_OC_high(self):
        return self.OC_high

    def set_OC_high(self, OC_high):
        self.OC_high = OC_high



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-g", "--gain-factor-tx", dest="gain_factor_tx", type=intx, default=60,
        help="Set gain_factor_tx [default=%(default)r]")
    parser.add_argument(
        "-m", "--multiply-constant-", dest="multiply_constant_", type=eng_float, default=eng_notation.num_to_str(float(0.08)),
        help="Set multiply_constant_ [default=%(default)r]")
    parser.add_argument(
        "-t", "--tx-addr-0", dest="tx_addr_0", type=str, default='32794C9',
        help="Set TX Address [default=%(default)r]")
    return parser


def main(top_block_cls=Final_Packet_Error_Test_TX_B200, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(gain_factor_tx=options.gain_factor_tx, multiply_constant_=options.multiply_constant_, tx_addr_0=options.tx_addr_0)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
