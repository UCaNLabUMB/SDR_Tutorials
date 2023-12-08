How to use:

The first flowgraph is called Packet_test_file_in.grc is intended to be run with the GNURadio application. All flowgraphs included here take a txt file and use OFDM to transmit the file to rx.

There are 3 versions. The first mentioned above runs the flowgraph via the GNU applicartion. 
The second one Packet_test_file_in_bash uses a batch script to call the GNU Radio flowgraph which runs to completion, before outputing. 
The 3rd version is composed of two parts Final_Packet_Error_Test_Tx_B200 & ....Rx_B200 are two seperate flowgraphs. These two use a batch script in conjuction with flowgraph parameter flags, and a python script with XMLRPC. The bash script calls the TX the the relevant parameter flag values, and then upgrades the fn via xmlrpc on the rx side. In other words for tx we use flags and for the rx we use XMLRPC. The bash script also uses the ARFL_Control to called the relevant XMLRPC flowgraph parameters to ensure the filename commands are sent to the server. 