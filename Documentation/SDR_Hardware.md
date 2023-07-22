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

The USRP Sink block in GNU Radio streams samples to a connected USRP hardware device for transmission over the air. It takes in complex baseband samples from the flowgraph and handles modulation, interpolation, conversion to analog signals etc. needed for the USRP to transmit the signals wirelessly. The parameters like center frequency, gain, antennas can be configured. It is used to transmit signals generated and processed within GNU Radio over real hardware radios.



* USRP Source

The USRP Source block in GNU Radio receives samples from a connected USRP hardware device after reception from its antennas. It handles decimation, demodulation, conversion to digital samples etc. to provide a stream of complex baseband samples into the GNU Radio flowgraph. The parameters like center frequency, gain, sample rate, antennas can be configured to correctly receive the wireless signals. It is used to transfer signals received by the USRP into GNU Radio for further processing and analysis.

### FLowgraph Image
![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Images/SDRHardware.png)
## Flowgraph Creation
In this flowgraph we are going to make a couple of changes to one we created with the GNURadio basic flowgraph. In this flowgraph they are only two things that we need to change. We need to put a USRP Sink block place of the throttle block. This will send the singal generation into the B200 Mini. The next thing that we need to do is to imput a USRP Source block. This is responsible for recieving the collected signal from the USRP and then bringing it back into the flowgraph. Once we have this done all we need to do is reconnect the output into our QT GUI of Choice. For all of this to work we have to retrive the Serial Address from the computer terminal via the UHD_Find_Devices command. What this does is report the serial address of the usrp, and then we take this string unput and place it into the slot for serial addresses in both the USRP source and sink blocks. 

UHD:USRP Sink allows us to send intended signal into USRPs.​
UHD:USRP Source allows to retrieve intended signal from USRPs.
Command: uhd_find_devices [For usrp serial id] in the Linux terminal allows us to receive our USRPs serial address for usage in both 
## Video Example: Flowgraph Creation Example Utlizing Eltus USRB B200 Mini.
_Coming Soon_

## References
_Coming Soon_

## Next Chapter
_Coming Soon_