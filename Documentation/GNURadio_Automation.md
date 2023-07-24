# GNURadio Automated Data Collection

## Overview
In this tutorial we will cover a couple of things. First we will see how to set up the GNURadio flowgraph via a command line start with intended parameters. Next after we will take our learning from the Networking and the GNURadio command and control in order to implement a PER test (packet error rate) witch will utilize both XML_RPC and ZMQ for control and monitoring of the flowgraph parameters. After this we will build upon this with the same flowgraph as the last tutorial but will that will cover OFDMA carrier allocation with will once again utilize XML_RPC. 

### Key Learnings

XML-RPC can help use with subcarrier selection by send the parameter update to the select blocks and picking which signal path we want to use. We can automate data collection with batch scripting and xml-rpc to save individual setup flowgraph denerations to a file naming convention we want. 

### GNURadio Blocks to be Introduced
* Channel Model Block 
Adds configurable channel impairments like noise, fading, distortion, and interference to the input signal.
Can model channel behaviors like AWGN, Rician fading, frequency selective fading etc.
Allows testing communications systems under realistic channel conditions.
Parameters can be adjusted to evaluate performance under different channel models.
Useful for simulating wireless channels like 5G, LTE, WiFi, satellite and more.
Models both analog effects like noise as well as digital effects like dropped packets.
Statistical models generate repeatable yet random channel behaviors.
Computationally efficient implementation of channel effects.
In summary, the Channel Model block adds realism to simulations.

* File Sink Block 
Stores complex samples or PDUs to a file in binary or text format.
Useful for capturing signals for later analysis and debugging.
Output file can be processed offline in tools like MATLAB, Python etc.
Supports streaming data to file in real-time during flowgraph execution.
File name and location can be configured programmatically.
Sample type (complex, float) and file format (binary, CSV) can be set.
Can control how often to write to file to limit size.
Handles buffering samples and threading for optimized high-speed file writing.

### FLowgraph Image
![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GNUPertestingpng.png)

## Flowgraph setup for cmd line start with parameters


## Repeatable PER test with XMLRPC and ZMQ


## References

## Next Chapter