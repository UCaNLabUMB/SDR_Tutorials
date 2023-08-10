# SDR Hardware and GNURadio

## Overview
In this section we will cover how to use GNURadio to interact with USRP SDR hardware for transmitting and receiving over-the-air signals. We will showcase how to obtain the USRP's hardware address, send and receive signals using USRP hardware, set command line parameters (when executing GNURadio flowgraphs outside of GRC), and observe frequency characteristics of carrier modulated waveforms. 

**Tutorial Video:** _Coming Soon_

### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03.png)

In this tutorial, we will develop the [SDR_Hardware flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) shown above. 


### GNURadio Blocks to be Introduced
This tutorial will introduce the following blocks from GNURadio:
* UHD: USRP Source Block
* UHD: USRP Sink Block
* Parameter Block
* Random Source Block
* Repeat Block





### Key Learnings

GNURadio can be utilized for a straightforward TX/RX setup with Ettus B200 mini USRPs.
It is important to be aware the we can utilize GNURadio for both traditional Radio Frequency applications and it can be also adapted for 
The Linux terminal is a handy tool to obtain the USRP Serial Address via UHD find devices.
GNU Radio Flowgraph allows the effective use of USRPs.

Practical Applications
Implement Ettus B200 mini USRPs in a simple TX/RX setup using GNURadio.
Use the Linux terminal to acquire the USRP Serial Address via UHD find devices for device identification.
Integrate USRP's in a GNU Radio Flowgraph for efficient signal processing.
Apply the USRP SINK Block for the TX USRP within a flowgraph to transmit signals.
Use the USRP Source for the RX USRP Flow to receive signals.
Leverage the QT GUI WaterFall Sink block for visualization of the receiver signal, facilitating real-time analysis and signal adjustment.









# USRP Hardware and GNURadio

## USRP Hardware Driver (UHD)
_Connecting USRPs to computer_

_Setting IP addresses (if needed... X or N Series)_

_Calling_ `uhd_find_devices`

_Getting USRP images if needed_

## Adding USRP Source and Sink Blocks
In this flowgraph we are going to make a couple of changes to one we created with the GNURadio basic flowgraph. We need to put a USRP Sink block place of the throttle block. This will send the singal generation into the B200 Mini. The next thing that we need to do is to imput a USRP Source block. This is responsible for recieving the collected signal from the USRP and then bringing it back into the flowgraph. Once we have this done all we need to do is reconnect the output into our QT GUI of Choice. For all of this to work we have to retrive the Serial Address from the computer terminal via the UHD_Find_Devices command. What this does is report the serial address of the usrp, and then we take this string unput and place it into the slot for serial addresses in both the USRP source and sink blocks. 

* UHD:USRP Sink allows us to send intended signal into USRPs.​ The USRP Sink block in GNU Radio streams samples to a connected USRP hardware device for transmission over the air. It takes in complex baseband samples from the flowgraph and handles modulation, interpolation, conversion to analog signals etc. needed for the USRP to transmit the signals wirelessly. The parameters like center frequency, gain, antennas can be configured. It is used to transmit signals generated and processed within GNU Radio over real hardware radios.
* UHD:USRP Source allows to retrieve intended signal from USRPs. The USRP Source block in GNU Radio receives samples from a connected USRP hardware device after reception from its antennas. It handles decimation, demodulation, conversion to digital samples etc. to provide a stream of complex baseband samples into the GNU Radio flowgraph. The parameters like center frequency, gain, sample rate, antennas can be configured to correctly receive the wireless signals. It is used to transfer signals received by the USRP into GNU Radio for further processing and analysis.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01.png)

_add and connect blocks... Mention no need for throttle_

_Setting Address and Sync properties_

_Note the signal range (-1 to 1)_

_Discuss RF Options: Antenna and carrier frequency properties_

## Parameter Blocks and Command Line Execution

_Discuss parameter blocks_

_Describe string concatenation in USRP source/sink blocks_

_Command line call with help and then to start flowgraph_

## Over-the-Air Transmission with GNURadio and USRPs

_Discuss observations from physical changes_

_Discuss sampling rate and gain settings_

_Discuss Overruns and Underruns_






# Dynamic Flowgraphs with USRP Hardware

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02.png)

## Flowgraph Generation
_Discuss merging with earlier flowgraphs_


## Observations

_Revisit real and complex sine with RF frequencies displayed_

_Change signal frequency_

_Change Tx and Rx center frequency_






# Observing OTA Waveforms

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03.png)

## BPSK Modulator

_Discuss basic modulators and relationship between signal bandwidth and parameters_

## Frequency Division Multiplexing

_Discuss multiplexing and multiple access_

## Observations




# References
_Coming Soon_

# Tutorial Chapters

* **Next Chapter:** [GNURadio Remote Command and Control](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_CaC.md) 
* **Previous Chapter:** [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)

| Chapter | Topic | Summary 
| --- | --- | --- |
|  1  | [GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)                   | Introduction to Flowgraphs, source/sink blocks, and data types
|  2  | [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)                       | Introduce flowgraph best practices, variables, and dynamic control
|  3  | SDR Hardware                                                                                                                    | Introduce USRPs, hardware addressing, and over-the-air waveform transmission
|  4  | [GNURadio Remote Command and Control](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_CaC.md)      | Introduce multi-node systems with XMLRPC and ZMQ
|  5  | [Basic Communicatons](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Comms.md)                    | Introduce simulation and over-the-air data transmission
|  6  | [Automated Data Collection](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Automation.md)         | Combine XMLRPC, ZMQ, and OFDM to automate Packet Error Rate Testing


