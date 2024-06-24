#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
import sys, getopt
import time


def main(argv):

   address       = 'localhost'
   port          = '8080'
   carrier_freq  = ''
   tone_freq     = ''
   sig_select    = ''
   bypass_filter = ''
   
   c_set = 0
   f_set = 0
   s_set = 0
   b_set = 0
   debug = 0
   
   try:
      opts, args = getopt.getopt(argv,"hc:f:s:b:d",["carrier_freq=","tone_freq=","sig_select=","bypass_filter="])
   except getopt.GetoptError:
      print ('  XML_Script_02.py -c <carrier frequency> -f <tone freq> -s <signal select> -b <bypass filter> ')
      sys.exit(2)   
   for opt, arg in opts:
      if opt == '-h':
         print ('  XML_Script_02.py -c <carrier frequency> -f <tone freq> -s <signal select> -b <bypass filter> ')
         sys.exit()
      elif opt in ("-c", "--carrier_freq"):
         carrier_freq = arg
         c_set = 1
      elif opt in ("-f", "--tone_freq"):
         tone_freq = arg
         f_set = 1
      elif opt in ("-s", "--sig_select"):
         sig_select = arg
         s_set = 1
      elif opt in ("-b", "--bypass_filter"):
         bypass_filter = arg
         b_set = 1
      elif opt in ("-d", "--debug"):
         debug = 1
         
   if debug == 1:
      if c_set == 1:
         print ('Carrier Frequency: ', carrier_freq)
      if f_set == 1:
         print ('Tone Frequency:    ', tone_freq)
      if s_set == 1:
         print ('Signal Select:     ', sig_select)
      if b_set == 1:
         print ('Bypass Filter:     ', bypass_filter)
   
   xmlrpc_control_client = ServerProxy('http://' + address + ':' + port)


   if c_set == 1:
      xmlrpc_control_client.set_fc_tx(int(carrier_freq))
      xmlrpc_control_client.set_fc_rx(int(carrier_freq))

   if f_set == 1:
      xmlrpc_control_client.set_sig_freq(int(tone_freq))
   
   if s_set == 1:
      xmlrpc_control_client.set_path_select(int(sig_select))

   if b_set == 1:
      xmlrpc_control_client.set_filter_select(int(bypass_filter))
   

if __name__ == "__main__":
   main(sys.argv[1:])
