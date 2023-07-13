# Simple GNURadio TX/RX
## Overview
In this section we will cover how to utlize SDR's in GNURadio. It will showcase how to obtain the USB serial address of the USRP, and in addition show which relevant blocks are mandatory for USRP use in GNURadio. 

### Key Learnings

GNURadio can be utilized for a straightforward TX/RX setup with Ettus B200 mini USRPs.
The Linux terminal is a handy tool to obtain the USRP Serial Address via UHD find devices.
GNU Radio Flowgraph allows the effective use of USRPs.

Practical Applications
Implement Ettus B200 mini USRPs in a simple TX/RX setup using GNURadio.
Use the Linux terminal to acquire the USRP Serial Address via UHD find devices for device identification.
Integrate USRP's in a GNU Radio Flowgraph for efficient signal processing.
Apply the USRP SINK Block for the TX USRP within a flowgraph to transmit signals.
Use the USRP Source for the RX USRP Flow to receive signals.
Leverage the QT GUI WaterFall Sink block for visualization of the receiver signal, facilitating real-time analysis and signal adjustment.

### GNURadio Blocks to be Introduced
* USRP SINK



* USRP Source
* ...


## Keypoints
UHD:USRP Sink allows us to send intended signal into USRPs.​
UHD:USRP Source allows to retrieve intended signal from USRPs.
Command: uhd_find_devices [For usrp serial id] in the Linux terminal allows us to receive our USRPs serial address for usage in both 
## Video Example: Flowgraph Creation Example Utlizing Eltus USRB B200 Mini.
_Coming Soon_

## References
_Coming Soon_