# SDR Hardware and GNURadio

## Overview
In this section we will cover how to use GNURadio to interact with USRP SDR hardware for transmitting and receiving over-the-air signals. We will demonstrate how to obtain the USRP's hardware address, send and receive signals using USRP hardware, set command line parameters (when executing GNURadio flowgraphs outside of GRC), and observe frequency characteristics of carrier modulated waveforms. 

**Tutorial Video:** _Coming Soon_

### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03.png)

In this tutorial, we will develop the [SDR_Hardware flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) shown above. The primary intention of this tutorial is to introduce the methods for communicating with USRP hardware. In particular, we will focus on an instance using two **B200 mini** USRPs which connect to your computer via USB. We will also introduce methods for command line flowgraph execution where parameter values are defined in the Python call, and we will begin to observe some signal properties related to modulated waveforms with random data.

As key learnings for this tutorial, we will cover
* Signal transmission and reception using B200 mini USRPs and GNURadio.
* USRP connections and use of the Linux terminal to acquire the USRP Address(es)
* Use of parameters to enable command line specification of values associated with flowgraph variables
* Considerations related to sample rate, hardware, flowgraph complexity, and processing power
* Signal bandwidth and a basic understanding of multiplexing, and multiple access


### GNURadio Blocks to be Introduced
This tutorial will introduce the following GNURadio blocks:
* UHD: USRP Source Block
* UHD: USRP Sink Block
* Parameter Block
* Random Source Block
* Repeat Block






# USRP Hardware and GNURadio
We first aim to create a simple flowgraph, shown below, that allows GNURadio to send and receive signals to/from USRP hardware. To do this, we will confirm that the computer can communicate with the USRP, then we will set appropriate parameters in the GNURadio flowgraph to enable signal transmission and reception.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01.png)

## USRP Hardware Driver (UHD)
Now that we are moving from simulation to observation of signals in the physical world, we need to add SDR hardware into our setup. In the image below, we see our Linux computer running GRC and two B200 mini USRPs connected via USB. 

![Hardware Setup](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_01.jpg)

* **NOTE:** The USRP on the right has a VERT900 antenna attached the TRX connection, and the USRP on the left has a VERT900 antenna attached to the RX2 connection. This is relevant as we will be sending our signals in the 900MHz ISM band, and these antennas are optimized for that frequency range. 

When using the B200 mini USRPs, our ability to communicate with the devices should be as simple as plugging in the USB port, however, other USRPs require additional setup (e.g., N Series and X Series USRPs use Ethernet instead of USB and require IP address assignment to ensure that your computer's Ethernet network interface card is able to communicate with the USRPs). 

To confirm that we can communicate with the connected USPRs, we will use the `uhd_find_devices` command to search for connected USRPs and determine the address(es) of any USRPs that are found. Along with most installations of GNURadio, you will have also installed the UHD library. **UHD**, or USRP Hardware Driver, is how GNURadio communicates with USRPs. From the Linux terminal, you can type `uhd_find_devices`, as shown below. In this case, the two USRPs are found and the Serial addresses are reported. We will need these addresses when defining which USRPs we are using in the GNURadio flowgraph.

![UHD Find Devices](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_02.png)

* **NOTE:** You can notice in the image above that firmware is first loaded to each of the USRPs before they return their address information. Whenever the B200 mini USRPs are powered up the firmware must be loaded onto the hardware so that they know how to function. If you call `uhd_find_devices` a second time, you will notice that the response comes back quicker and you will not see the INFO message stating "_Loading Firmware Image_ ..." since the firmware has already been loaded to the USRPs. If you power cycle the USRPs (i.e., unplug the USB cables) the firmware will be loaded again the next time your computer attempts to communicate with the USRPs.

* **NOTE:** The first time you try to connect to a USRP, you may need to download the relevant USRP firmware images and/or set appropriate privileges. If you receive an error related to either of these issues, you can review the UHD and USRP Manual for instructions related to the [UHD images downloader](https://files.ettus.com/manual/page_images.html) tool or [setting Udev rules](https://files.ettus.com/manual/page_transport.html).




## Adding USRP Source and Sink Blocks
Once we have confirmed that our computer can communicate with the connected USRPs, we can create the GNURadio flowgraph below to actually send/receive signals to/from the USRPs.
* **NOTE:** Compared to the simulation flowgraphs we've seen before, we should notice that this flowgraph does NOT have a Throttle block. The USRPs are clocked devices that control the rate at which samples are accepted or generated, so we do not need to include the Throttle block to managing the flow rate of samples passing through our flowgraph. 

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01.png)

The signal path in this flowgraph connects the **Signal Source** and **QT GUI Sink** blocks that we've already seen to two new blocks, namely the **UHD: USRP Sink** and **UHD: USRP Source** blocks. Once these blocks are added, you can connect the Signal Source to the USRP Sink and the USRP Source to the QT GUI Sink. USRP Sink blocks use the UHD library to send signals to the USRPs.​ By default, USRP Sink blocks accept complex baseband samples from the flowgraph and handle the interpolation, digital to analog conversion, and carrier modulation so that the RF signal can be sent over the air with a user-defined center frequency. USRP Source blocks use the UHD library to receive signals from the USRPs. The USRP handles carrier demodulation, conversion to digital samples, and decimation to provide a digital stream of complex samples to the GNU Radio flowgraph. These samples relate to the complex-baseband representation of the RF signal received at the user-defined center frequency.

* **NOTE:** In the context of these UHD blocks, _Sink_ and _Source_ refer to the direction of data flow in GNURadio. In other words, the Sink block is accepting data from GNURadio (even though it is in fact for signal transmission) and the Source block is generating data within GNURadio (even though it is actually associated with the USRP that is receiving the physical signal).

Once we have added and connected the relevant blocks, we will set properties for each block. 
* First, set your parameters in the **Options** block as we have done previous 
  * e.g. ID for the name of the Python script that will be generated, title, author, documentation, etc.
* Next, set the value of _samp\_rate_ in the **Variable** block. 
  * By default, this variable should be already used in the blocks that you added. We have set this to 2.5e6.
* In your **Signal Source** block, set the signal's _frequency_ to a value below 1.25MHz and _amplitude_ to a value less than or equal to 1. 
  * We have it set the Frequency as 1e6 and the amplitude as 0.25.
  * The amplitude value is important as the UHD source expects values in the range of -1 to 1.
* Set the center frequency in the **QT GUI Sink** block to 915e6 (i.e., 915MHz). 
  * It is important to note that this is for _display purposes only_ when displaying frequency plots in terms of the RF Frequencies. 
  * The actual Tx and Rx carrier frequency values will be set in the UHD blocks. 
  * You can select to show RF frequencies in the GUI while the flowgraph is running, but we have set this to the default by setting the _Show RF Freq_ property to _Yes_.
* When opening the **UHD: USRP Sink** and **UHD: USRP Source** blocks, there is not much that needs to be changed in the General settings. In this tab, you will only need to set the _Device Address_ property to the serial address that was determined from the _uhd\_find\_devices_ call. We also set the _Sync_ property to _No Sync_. The _samp\_rate_ variable should already be assigned to the Samp Rate property. 
  * Make sure to include quotes and use the format shown below for the address property (i.e., "serial=\[address number\]"). 
  * For USRP devices connected via Ethernet, _serial_ would be replaced with _addr_ and the value would be the USRP's IP address.
* The second image below shows the _RF Options_ properties for the USRP source and Sink blocks. Here, we have set both _Center Frequency_ values to 915MHz so that our transmitter and receiver are aligned. We have also defined _Channel Gain_ settings and the _Antenna_ location (recall the physical antenna connections shown in the earlier image of the hardware setup.)

![UHD Source and Sink Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_03.png)

![UHD Source and Sink RF Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_04.png)

* **NOTE:** Make sure that you are clear about which serial address corresponds to which USRP! If you are unsure, you can unplug one of the devices and rerun the _uhd\_find\_devices_ command to determine the address of the device that is still connected.

At this point, you should be able to build and execute the flowgraph in GRC if you followed the steps above. However, if you attempt to run the completed [SDR_Hardware_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph from this repository you will get an error since the address should not be the same as your USRPs' addresses. We will first discuss how we've included parameter blocks to allow for user specification of the address, then we will discuss some observations about the running OTA transmission.


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


