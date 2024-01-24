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
  * Make sure to include quotes and use the format shown below for the address property (i.e., `"serial=<address number>"`). 
  * For USRP devices connected via Ethernet, _serial_ would be replaced with _addr_ and the value would be the USRP's IP address.
* The second image below shows the _RF Options_ properties for the USRP source and Sink blocks. Here, we have set both _Center Frequency_ values to 915MHz so that our transmitter and receiver are aligned. We have also defined _Channel Gain_ settings and the _Antenna_ location.
  * Recall the physical antenna connections shown in the earlier image of the hardware setup.

![UHD Source and Sink Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_03.png)

![UHD Source and Sink RF Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_04.png)

* **NOTE:** Make sure that you are clear about which serial address corresponds to which USRP! If you are unsure, you can unplug one of the devices and rerun the _uhd\_find\_devices_ command to determine the address of the device that is still connected.

At this point, you should be able to build and execute the flowgraph in GRC if you followed the steps above. However, if you attempt to run the completed [SDR_Hardware_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph from this repository you will get an error since the defined addresses should not be the same as your USRPs' addresses. We will first discuss how we've included parameter blocks to allow for user specification of the address, then we will discuss some observations about the running OTA transmission.


## Parameter Blocks and Command Line Execution

To resolve the issue mentioned above, an easy solution is to open the flowgraph in GRC and change the address values in the USRP Source and Sink blocks. However, this process of manually changing the flowgraph can be unnecessarily tedious in situations where you might want to change a certain parameter value when running the flowgraph. With this in mind, GNURadio offers **parameter** blocks that behave similar to variables, but also allow for the value to be set when the flowgraph is started. In this example, we'll use parameter blocks for the USRP addresses so that these can be assigned when starting a flowgraph through the command line interface.

Going back to the flowgraph, our first step is to add the parameter blocks and update block settings. The figure below shows the settings assigned to the parameter, and how the parameter is used with string concatenation in the USRP Sink block. In this way, the address for the Tx USRP is defaulted as originally configured, but the parameter block also allows the address to be specified as a parameter when running the python code on the command line.

![Parameter Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_05.png)

In the figure below, we can see the process of running the flowgraph on the command line. Note that you must first build the flowgraph in GRC to create the python file. Now, if you open a terminal and move to the directory where your flowgraph is stored there should be a python file with the name defined by your flowgraph's ID (set earlier in the **Options** block). When you run the python file with the `-h` flag, as shown below, you should get a help menu that shows the available parameters for this flowgraph and the corresponding flags.

![Command Line Call with Parameters](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_06.png)

The last line in the example above is the call to execute the flowgraph with newly specified addresses for the Tx and Rx USRPs. Running this command with the addresses found from your specific `uhd_find_devices` call should start the flowgraph discussed in the following.

## Over-the-Air Transmission with GNURadio and USRPs

Once the flowgraph is running, you should see a GUI visualization similar to what is shown in the figure below. 

![over the air transmission results](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_07.png)

This basic flowgraph highlights some basic (but very important) signal processing concepts, and it is a good starting point to make sure you can recognize the impact of changing various parameters, as discussed below.

* Since the option is set to "Show RF Frequencies" you should see the **center frequency (fc)** at 915MHz based on the setting in our QT Sink block, defined earlier. You should also notice the **tone** at 916MHz in our Frequency display since our initial signal was defined as a 1MHz complex sinuisoid and our carrier modulation ultimately shifted this from being centered at 0 to being centered at fc.
  * Keep in mind that the displayed center frequency is based on what you define in the QT sink block, and is not directly related to the true carrier frequency associated with the receiver USRP. With this in mind, it is a good practice to use a variable to assign your carrier frequency, and then use this variable in both the USRP Source and the QT GUI. We will follow this in future flowgraphs.
* Notice that the observable range of frequencies is 913.75MHz to 916.25MHz. As expected, this bandwidth is equal to the **sample rate (fs)** defined in the flowgraph (i.e., 2.5MHz).
  * If you close the flowgraph and rerun it with a different sample rate, you should notice the difference in the observable frequencies where the range will always be fc-fs/2 to fc+fs/2. 
  * As you increase the sample rate, you will see this range increase; but be aware of the fact that your computer must generate and/or process samples faster when the sample rate increases. At some point, your computer will not be able to keep up and you will see repetitions of "O" or "U" in the terminal. This is an indicator that you are running into overruns or underruns where your computer can not keep up with the demands of the hardware.
* You will also notice that the default frequency resolution is not as high as shown in the image above. This is because the **FFT Size** has been increased to 4096, implying that there are 4096 dicsrete observation points across the observable frequency range. 
  * As a recall from basic signals, increasing the FFT size and maintaining the same fs requires that we observe the signal for a longer period in time, and doing so increases the _resolution_ in frequency.
* If you revisit the flowgraph and modify the **Tx and Rx Gain** settings in your USRP Source and Sink blocks, you can also observe the impacts on the observed power of the tone and of the noise.

In addition to the changes above, you can also observe the physical channel's impact on the signal by observing what happens to the magnitude of the frequncy component associated with the 1MHz tone when you block the path between the Tx and Rx USRPs, or when you move the USRPs closer or further apart.


# Dynamic Flowgraphs with USRP Hardware
In the [SDR_Hardware_02](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph, shown below, we merge the dynamically configurable tone generation example from the previous chapter with the hardware integration discussed above. This allows for observation of the basic tone characteristics discussed previously while considering the impact of carrier modulation / demodulation and over-the-air transmission.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02.png)

## Flowgraph Generation
The main structure of this flowgraph is similar to the GNURadio\_Basics\_04 flowgraph discussed in the last chapter. The main change is that we've replaced the simulated noise channel (i.e., the **Noise Source** and **Add** blocks) with an actual transmission using the **UHD: USRP Sink** and **UHD: USRP Source blocks**. As we've done above, we also added parameter blocks for the Tx and Rx USRP addresses to allow for user-specified addresses based on the connected USRPs when running the flowgraph. Lastly, we've included 4 **QT GUI Range** blocks for the Tx/Rx center frequency and gain. the ID for each of these adjustable variables is then assigned to the corresponding setting in the USRP Sink and Source blocks' RF Options tabs. This is done so that we can modify these parameter with the running flowgraph to observe the impact on the received signal characteristics.

To run the flowgraph, make sure to first build the flowgraph in GRC (to generate the python file) and then run the file in a terminal with the command:
* `python3 SDR\_Hardware\_02.py -t <tx\_address> -r <rx\_address>`

## Observations
Once we've run the flowgraph, we can first observe some of the same characteristics from the simulated tone generator example in the last chapter. The image below shows the waterfall plot as we vary some of the signal characteristics. From the discussion in the previous chapter, we can recognize that we started with a 100KHz real-valued sinusoid, with the key difference here being that the signal components show up at 914.9MHz and 915.1MHz, rather than +/- 0.1MHz. This again relates to the displayed RF Frequencies and the fact that our carrier frequency is set as 915MHz. Following the discussion from the previous chapter, we can also recognize the signal modifications in time as first converting to a complex-valued sinusoid (leaving only the tone at 915.1MHz), then bypassing the filter (increasing the noise floor outside the filter's range), and then increasing the signal frequency to 250KHz before switching back to a real-valued sinusoidal signal (observable through the reintroduction of the lower frequency component, now at 914.75MHz or, similarly, at fc-250KHz).

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_01.png)

Another important consideration for over-the-air transmission is the appropriate alignment of the Tx and Rx center frequencies (or carrier frequencies). In the figure below, we again start with the default 100KHz real-valued sinusoid with both Tx and Rx center frequency assigned to 915MHz. We then increase and decrease the Tx center frequency to recognize how this impacts the received signal. You can see that the frequency components associated with 100KHz signal are moved up and down together as we increase the Tx center frequency to 915.5MHz and then reduce to 914Mz. The key observation here is that the actual signal transmitted over the air is changing to different frequencies. In other words, the signal's components always show up at fc_tx +/- 100KHz. Since the Rx center frequency is assigned separately and associated with the USRP Source and the QT Sink, the observed frequency range remains consistent. Furthermore, the baseband implementation of the Rx filter does not account for the change in the Tx carrier, so the filtered range does not adjust. As a final observation in this figure, we should be able to recognize that the signal was changed to a complex sinusoid in the last 5 seconds before adjusting the Tx carrier back to 915MHz.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_02.png)

As a final observation from this flowgraph, we can also observe the relative impact of Tx and Rx gain on the received signal. The outcome below is achieved by starting with the default settings, and then first increasing the Tx Gain value and then increasing the Rx Gain setting. The key takeaway is the relative impact on the signal and noise. While both gain settings can increase the received signal power, it's important to observe that increasing the gain at the receiver also increases the noise floor! This becomes relevant when considering signal-to-noise ratio (SNR) and the impact on communication signals - both in point-to-point settings and also in multi-user settings. At a high level, the Rx Gain setting is essential for making sure that your signal is strong enough to avoid significant impacts of sampling and quantization when converting to a digital signal, but the impact on SNR is negligible. Increasing the Tx Gain ultimately leads to increased signal power AND improved SNR in most cases, but emitting higher power signals will have a more significant impact on other nearby transmissions in the same band. These tradeoffs are important to consider when designing and optimizing a wireless communications system.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_03.png)




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


