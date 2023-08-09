# GNURadio Comms

## Overview
In this tutorial we will combine our learning over the past tuturials and combine them in order to achive different functional flowgraph. First we will start with OFDM Simulation with no hardware elementets and then go into packet error rate testing flowgraph.

### Key Learnings
Here is an expanded explanation of the OFDMA Subcarrier selection flowgraph:

The flowgraph starts with a random source block that generates random data samples to act as the input source. 

This random data is then fed into the chunks to symbols block which converts the stream of byte values into complex symbols based on a modulation scheme like QPSK or QAM. This modulates the data onto constellation points.

The stream to tagged stream block takes this symbol stream and packets it into chunks of a specified packet length by adding length tags. This packets the data.

A virtual sink is used to discard the samples at this stage to avoid wasting processing if the data stream is not actually being used.

The original source stream is branched off and passed into the OFDM carrier allocator block which divides the input data into subcarriers to be transmitted via OFDM. 

The OFDM FFT block then performs FFT processing to convert the frequency domain input signals into time domain samples.

The cyclic prefixer adds a cyclic prefix to each symbol to mitigate inter-symbol interference due to multipath effects.

Finally, the output of the cyclic prefixed OFDM symbols can be visualized on a QT GUI sink to see the OFDM signal structure.

In summary, it takes a random data source, packets and modulates it, applies OFDM modulation for multicarrier transmission, and plots the output signal. This demonstrates the basic operations in an OFDMA digital communications loopback flowgraph.

### GNURadio Blocks to be Introduced
* Random Source

Generates random data samples to act as a source signal.


* Chunks to Symbols

Converts streams of bytes or chunks to complex symbols based on a modulation scheme. Modulates data

* OFDM Carrier Allocatior
Divides an input signal into subcarriers to implement OFDM modulation.

* FFT
Performs an FFT to convert between frequency and time domain representations. Used in OFDM.
* Stream to Tagged Stream
Packetizes a stream by adding length tags. Used for creating packets.
* OFDM Cyclic Prefixer 
Adds a cyclic prefix to OFDM symbols to mitigate inter-symbol interference.
* Selector Block
Dynamically routes input streams to one of several outputs based on a control signal. Acts like a switch.
### FLowgraph Image
![Flowgraph Image](hhttps://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Images/GNUComms.png)

## OFDM Loopback Carrier Allocation 
Random Source Block: Start by placing this block in your flowgraph. It's responsible for creating the random data samples that will act as the input source for the rest of the process.

Chunks to Symbols Block: Next, connect the Random Source Block to this block. It takes the stream of random data and converts it into complex symbols. This is done through a modulation scheme like QPSK or QAM, which essentially reshapes the data for easier transmission.

Stream to Tagged Stream Block: Connect the Chunks to Symbols Block to this block. Its job is to take the symbol stream and packet it into chunks of a specified length by adding length tags. This effectively organizes the data into neat packets.

Virtual Sink: At this stage, you should also connect a Virtual Sink. Its purpose is to throw away any samples that aren't needed, which saves processing power.

OFDM Carrier Allocator Block: Now, take a branch from the original source stream and connect it to the OFDM Carrier Allocator Block. This block's role is to divide the data into subcarriers that can be transmitted using the OFDM method.

OFDM FFT Block: Connect this block next. It performs a process called FFT to convert the frequency domain input signals into time domain samples.

Cyclic Prefixer: Add this block to add a 'cyclic prefix' to each symbol. This step helps to prevent interference between symbols due to multipath effects.

QT GUI Sink: Finally, connect the output from the Cyclic Prefixer to the QT GUI Sink. This allows you to visualize the OFDM signal structure and the output of your flowgraph.




## References

## Tutorial Chapters

* **Next Chapter:** [GNURadio Remote Command and Control](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_CaC.md)
* **Previous Chapter:** [Automated Data Collection](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Automation.md)

| Chapter | Topic | Summary 
| --- | --- | --- |
|  1  | [GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)                   | Introduction to Flowgraphs, source/sink blocks, and data types
|  2  | [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)                       | Introduce flowgraph best practices, variables, and dynamic control
|  3  | [SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md)                             | Introduce USRPs, hardware addressing, and over-the-air waveform transmission
|  4  | [GNURadio Remote Command and Control](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_CaC.md)      | Introduce multi-node systems with XMLRPC and ZMQ
|  5  | Basic Communicatons                                                                                                             | Introduce simulation and over-the-air data transmission
|  6  | [Automated Data Collection](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Automation.md)         | Combine XMLRPC, ZMQ, and OFDM to automate Packet Error Rate Testing

