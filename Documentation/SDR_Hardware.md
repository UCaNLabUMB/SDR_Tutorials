# SDR Hardware and GNURadio

## Overview
In this section we will cover how to use GNURadio to interact with USRP SDR hardware for transmitting and receiving over-the-air signals. We will demonstrate how to obtain the USRP's hardware address, send and receive signals using USRP hardware, set command line parameters (when executing GNURadio flowgraphs outside of GRC), and observe frequency characteristics of carrier modulated waveforms. 

**Tutorial Video:** _Coming Soon_

### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03.png)

In this tutorial, we will develop the [SDR_Hardware flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) shown above. The primary intention of this tutorial is to introduce the methods for communicating with USRP hardware. In particular, we will focus on an instance using two **B200 mini** USRPs which connect to your computer via USB. We will also introduce methods for command line flowgraph execution where parameter values are defined in the Python call, and we will begin to observe some signal properties related to modulated waveforms with random data.

As key learnings for this tutorial, we will cover
* Signal transmission and reception using B200 mini USRPs and GNURadio,
* USRP connections and use of the Linux terminal to acquire the USRP Address(es),
* An introduction to the USRP hardware driver (UHD),
* Use of parameters to enable command line specification of values associated with flowgraph variables,
* Considerations related to sample rate, hardware, flowgraph complexity, and processing power,
* Signal bandwidth and a basic understanding of multiplexing, and multiple access


### GNURadio Blocks to be Introduced
This tutorial will introduce the following GNURadio blocks:
* UHD: USRP Source Block
* UHD: USRP Sink Block
* Parameter Block
* Random Source Block
* Chunks to Symbols Block
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

* **NOTE:** The reported serial address is NOT the same as the USRP serial number on the USRP's label! The USRPs serial number is associated with the USRP hardware, whereas the serial address that we find with `uhd_find_devices` is the serial address of the USB hardware (i.e., how we are communicating with the device).

![UHD Find Devices](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_02.png)

* **NOTE:** You can notice in the image above that firmware is first loaded to each of the USRPs before they return their address information. Whenever the B200 mini USRPs are powered up the firmware must be loaded onto the hardware so that they know how to function. If you call `uhd_find_devices` a second time, you will notice that the response comes back quicker and you will not see the INFO message stating "_Loading Firmware Image_ ..." since the firmware has already been loaded to the USRPs. If you power cycle the USRPs (i.e., unplug the USB cables) the firmware will be loaded again the next time your computer attempts to communicate with the USRPs.

* **NOTE:** The first time you try to connect to a USRP, you may need to download the relevant USRP firmware images and/or set appropriate privileges. If you receive an error related to either of these issues, you can review the UHD and USRP Manual for instructions related to the [UHD images downloader](https://files.ettus.com/manual/page_images.html) tool or [setting Udev rules](https://files.ettus.com/manual/page_transport.html).

In addition to the `uhd_find_devices` command, the UHD library has some other functionality that is readily available. If you type `uhd` in the terminal and use the linux terminal's autocomplete feature (i.e., the tab key) you should see a list of 10-20 uhd commands that can directly be run in the terminal. 

* If you are not familiar with the terminal autocomplete functionality, this is an incredibly useful trait of the terminal (and will greatly speed up the process of working with the command line). In this instance, hitting tab after typing `uhd` should show `uhd_` since there are multiple commands that start with `uhd`. Quickly hitting tab twice will provide the list of commands that can be run (with `uhd_find_devices` as one of the options). If you type `uhd_fi` and hit tab again, this will autocomplete `uhd_find_devices` since it is the only command that starts with that sequence of letters.

Another useful built-in uhd command is `uhd_fft`. Running `uhd_fft -h` in the terminal will display a short help menu that indicates the command line arguments that can be used. As a simple example, you can run the command below using the address for your receiving USRP in place of `<address>`. The `-a` flag indicates the address of your USRP, and the `-f` flag is to specify the center frequency that will be set on the hardware.

* `uhd_fft -a serial=<address> -f 915000000`

This should open up the GUI shown below. This offers a simple way to observe the received RF signal in time or frequency domain (or in a waterfall plot) and allows you to manipulate various configuration settings in a graphical interface.

![UHD FFT](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_08.png)



## Adding USRP Source and Sink Blocks
Once we have confirmed that our computer can communicate with the connected USRPs, we can create the GNURadio flowgraph below to actually send/receive signals to/from the USRPs.
* **NOTE:** Compared to the simulation flowgraphs we've seen before, we should notice that this flowgraph does NOT have a Throttle block. The USRPs are clocked devices that control the rate at which samples are accepted or generated, so we do not need to include the Throttle block to manage the flow rate of samples passing through our flowgraph. 

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
  * The actual Tx and Rx carrier frequency values for the over-the-air signal will be set in the UHD blocks. 
  * You can select to show RF frequencies in the GUI while the flowgraph is running, but we have set this to the default by setting the QT GUI Sink's _Show RF Freq_ property to _Yes_.
* When opening the **UHD: USRP Sink** and **UHD: USRP Source** blocks, there is not much that needs to be changed in the General settings. In this tab, you will only need to set the _Device Address_ property to the serial address that was determined from the _uhd\_find\_devices_ call. We also set the _Sync_ property to _No Sync_. The _samp\_rate_ variable should already be assigned to the Samp Rate property. 
  * Make sure to include quotes and use the format shown below for the address property (i.e., `"serial=<address number>"`). 
  * For USRP devices connected via Ethernet, _serial_ would be replaced with _addr_ and the value would be the USRP's IP address (i.e., `"addr=<IP address>"`).
* The second image below shows the _RF Options_ properties for the USRP source and Sink blocks. Here, we have set both _Center Frequency_ values to 915MHz so that our transmitter and receiver are aligned. We have also defined _Channel Gain_ settings and the _Antenna_ location.
  * Recall the physical antenna connections shown in the earlier image of the hardware setup.

![UHD Source and Sink Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_03.png)

![UHD Source and Sink RF Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_01_04.png)

* **NOTE:** Make sure that you are clear about which serial address corresponds to which USRP! If you are unsure, you can unplug one of the devices and rerun the _uhd\_find\_devices_ command to determine the address of the device that is still connected.

At this point, you should be able to build and execute the flowgraph in GRC if you followed the steps above. However, if you attempt to run the completed [SDR_Hardware_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph from this repository you will get an error since the defined addresses should not be the same as your USRPs' addresses. We will first discuss how we've included parameter blocks to allow for user specification of the address, then we will discuss some observations about the running OTA transmission.


## Parameter Blocks and Command Line Execution

To resolve the issue mentioned above, an easy solution is to open the flowgraph in GRC and change the address values in the USRP Source and Sink blocks. However, this process of manually changing the flowgraph can be unnecessarily tedious in situations where you want to specify a certain parameter value each time you run the flowgraph. With this in mind, GNURadio offers **parameter** blocks that behave similar to variables, but also allow for the value to be set when the flowgraph is started. In this example, we'll use parameter blocks for the USRP addresses so that these can be assigned when starting a flowgraph through the command line interface.

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

In addition to the changes above, you can also observe the physical channel's impact on the signal by observing what happens to the magnitude of the frequncy component associated with the 1MHz tone when you:
* block the path between the Tx and Rx USRPs, 
* rotate one of the USRPs, or 
* move the USRPs closer or further apart.


# Dynamic Flowgraphs with USRP Hardware
In the [SDR_Hardware_02](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph, shown below, we merge the dynamically configurable tone generation example from the previous chapter with the hardware integration discussed above. This allows for observation of the basic tone characteristics discussed previously while considering the impact of carrier modulation / demodulation and over-the-air transmission.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02.png)

## Flowgraph Generation
The main structure of this flowgraph is similar to the GNURadio\_Basics\_04 flowgraph discussed in the last chapter. The main change is that we've replaced the simulated noise channel (i.e., the **Noise Source** and **Add** blocks) with an actual transmission using the **UHD: USRP Sink** and **UHD: USRP Source blocks**. As we've done above, we also added parameter blocks for the Tx and Rx USRP addresses to allow for user-specified addresses based on the connected USRPs when running the flowgraph. Lastly, we've included 4 **QT GUI Range** blocks for the Tx/Rx center frequency and gain. The ID for each of these adjustable variables is then assigned to the corresponding setting in the USRP Sink and Source blocks' RF Options tabs. This is done so that we can modify these parameter with the running flowgraph to observe the impact on the received signal characteristics.

To run the flowgraph, make sure to first build the flowgraph in GRC (to generate the python file) and then run the file in a terminal with the command:
* `python3 SDR_Hardware_02.py -t <tx_address> -r <rx_address>`

## Observations
Once we've run the flowgraph, we can first observe some of the same characteristics from the simulated tone generator example in the last chapter. The image below shows the waterfall plot as we vary some of the signal characteristics. From the discussion in the previous chapter, we can recognize that we started with a 100KHz real-valued sinusoid, with the key difference here being that the signal components show up at 914.9MHz and 915.1MHz, rather than +/- 0.1MHz. This again relates to the displayed RF Frequencies and the fact that our carrier frequency is set as 915MHz. Following the discussion from the previous chapter, we can also recognize the signal modifications in time as first converting to a complex-valued sinusoid (leaving only the tone at 915.1MHz), then bypassing the filter (increasing the noise floor outside the filter's range), and then increasing the signal frequency to 250KHz before switching back to a real-valued sinusoidal signal (observable through the reintroduction of the lower frequency component, now at 914.75MHz or, similarly, at fc-250KHz).

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_01.png)

Another important consideration for over-the-air transmission is the appropriate alignment of the Tx and Rx center frequencies (or carrier frequencies). In the figure below, we again start with the default 100KHz real-valued sinusoid with both Tx and Rx center frequency assigned to 915MHz. We then increase and decrease the Tx center frequency to recognize how this impacts the received signal. You can see that the frequency components associated with 100KHz signal are moved up and down together as we increase the Tx center frequency to 915.5MHz and then reduce to 914Mz. The key observation here is that the actual signal transmitted over the air is changing to different frequencies. In other words, the signal's components always show up at fc_tx +/- 100KHz. Since the Rx center frequency is assigned separately and associated with the USRP Source and the QT Sink, the observed frequency range remains consistent. Furthermore, the baseband implementation of the Rx filter does not account for the change in the Tx carrier, so the filtered range does not adjust. As a final observation in this figure, we should be able to recognize that the signal was changed to a complex sinusoid in the last 5 seconds before adjusting the Tx carrier back to 915MHz.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_02.png)

As a final observation from this flowgraph, we can also observe the relative impact of Tx and Rx gain on the received signal. The outcome below is achieved by starting with the default settings, and then first increasing the Tx Gain value and then increasing the Rx Gain setting. The key takeaway is the relative impact on the signal and noise. While both gain settings can increase the received signal power, it's important to observe that increasing the gain at the receiver also increases the noise floor! This becomes relevant when considering signal-to-noise ratio (SNR) and the impact on communication signals - both in point-to-point settings and also in multi-user settings. At a high level, the Rx Gain setting is essential for making sure that your signal is strong enough to avoid significant impacts of sampling and quantization when converting to a digital signal, but the impact on SNR is negligible. Increasing the Tx Gain ultimately leads to increased signal power AND improved SNR in most cases, but emitting higher power signals will have a more significant impact on other nearby transmissions in the same band. These tradeoffs are important to consider when designing and optimizing a wireless communications system.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_02_03.png)




# Observing OTA Waveforms
In this section, we introduce the [SDR_Hardware_03](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph, shown below. This extends our observed signals beyond the simple tones that we've been observing. More specifically, we will first look at a very basic communications signal implementing binary phase shift keying (BPSK). We will then extend the concept to a multiplexed transmit signal implementing frequency division multiplexing (FDM) in order to combine multiple BPSK signals in a single transmission. The flowgraph uses the previously introduced **Chooser** and **Selector** blocks to allow for dynamic changing of the transmitted signal while the flowgraph is running.

* **NOTE:** Keep in mind that this example is purely to demonstrate basic _signal-level characteristics_ of modulated data transmissions. For practical over-the-air data transmission, additional overhead is needed in order to account for channel impairments before you can demodulate/decode the transmitted bits.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03.png)

There are two Tx signal paths in this flowgraph. Specifically, these signal paths generate the _TxSignal_BPSK_ and _TxSignal_FDM_ virtual signals that are passed into the selector block before the signal is sent to the transmitting USRP. The signal from the receiving USRP is simply passed into a QT GUI Sink for observation.

* **NOTE:** Both potential Tx signals are also passed into the **QT GUI Time Sink** and **QT GUI Frequency Sink** blocks (in the bottom right of the image above). These blocks have a more specific focus than the QT GUI Sink block, but they allow for multiple signals to be plotted in the same figure for comparison.



## BPSK Modulator

The signal chain for the basic BPSK signal generation is relatively straightforward. First, a random integer stream is generated with each value as either 0 or 1 representing the desired symbol number (or equivalently bits in this instance). This is implemented using the **Random Source** block with minimum set to $0$ and maximum set to $2$.

* **NOTE:** The **Random Source** block generates values in the range $[min, max)$ such that it is NOT inclusive of the max value! This is an important nuance of this blocks implementation that can lead to unexpected outcomes (and frustration!) if not used appropriately.

After the **Random Source** block, the stream of integers is passed through the **Chunks to Symbols** block. This block maps the integer values to specified complex values representing the actual symbol corresponding to the symbol number. In the case of BPSK, we are mapping to the real values $\pm 0.25$, but representing these values in a complex value stream (i.e., $\pm 0.25 + j0$). The output is then passed into a **Repeat** block which interpolates the signal with a specified number of repetitions. We have set a variable that defines the interpolation equal to sample rate divided by the signal frequency (i.e., symbol rate). This can be thought of as

$$ \frac{samples}{symbol} = \frac{\frac{samples}{second}}{\frac{symbols}{second}} = \frac{sample rate}{symbol rate}$$

* **NOTE:** For demonstration, we have a sample rate of 20MHz such that the desired symbol rates of 1MHz, 2MHz, 4MHz, or 5MHz all work out to integer interpolation values.

When running the flowgraph (via command line with appropriate address parameters for your USRPs), you should see the interface below. 

![BPSK in FFT](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_01.png)

The configuration settings are at the top. The QT GUI Sinks for the Tx and Rx signals are shown in the middle on the left and right, respectively. The only non-default configuration in the image above is that the average setting for the FFT is set to 10 in order to clean up the image and show a less variable result (i.e., compared to what you see when observing the FFT without averaging). The bottom two figures show the selectable Tx signals (i.e., baseline BPSK or two BPSK signals with FDM) in time domain and frequency domain.

In the figure above, the source signal (i.e., the signal that is being sent over-the-air) is set as the single BPSK signal, and the Tx/Rx QT GUI sinks are set to observe the frequency display. From this fixed configuration, we can make the following observations:
* The observable frequency range is from 905MHz to 925MHz since we are using a sample rate of 20MHz and a center frequency of 915MHz. 
* The received signal has lower peak power and is more noisy across the observable spectrum range. 
* The main lobe of our signal (i.e., between the nulls at 914MHz and 916Mhz) has a bandwidth of 2MHz, or twice the 1MHz signal frequency (i.e., symbol rate). 
* Each of the side lobes have a width of 1MHz (equal to the symbol rate), and the power of each side lobe decreases as we look further away from the main lobe.

Adjusting the Tx/Rx center frequency and gain settings should reiterate some of our observations from the previous section of this chapter. More specifically:
* Changing the Tx center frequency should move the location of the signal's main lobe in the RX frequency display, but the range in the Rx frequency display should remain consistent.
* Changing the Rx center frequency should change the observable range of frequencies in the Rx frequency display, but the main lobe of your signal should always be at the Tx center frequency.
* Increasing the Tx gain should start to raise the signal above the noise floor in the Rx frequency display, likely making more of the side lobes observable.
* Increasing the Rx gain should increase the power of the signal and noise, so the relative gain should increase across all frequencies in the Rx frequency display.

The carrier adjustment observations can be seen in the image below. With the Tx center frequency set to 910MHz, we can observe the Tx frequency display shows the range from 900MHz to 920MHz with the main lobe of the signal at 910MHz, as expected. Since the Rx center frequency is set to 920MHz, the Rx frequency display shows the received spectrum from 910MHz to 930MHz with our transmitted signal clearly observable in the range from 910MHz to 920MHz.

![BPSK adjusted carriers](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_06.png)

* **NOTE:** Notice that there aren't any observable side lobes beyond 920MHz in the Rx frequency display. This is related to the hardware filters in the transmitting USRP. These are implemented after upsampling to the transmitting hardware's DAC rate and before the DAC and analog upconversion. The purpose is to mitigate out-of-band interference. Similar filters are also implemented in the receiver to avoid aliasing of unwanted out-of-band received signals.

* **NOTE:** Notice the additional signal in the Rx frequency display near 930MHz. This is not something we are sending! Since the 900MHz ISM band operates from 902MHz through 928MHz, we are seeing an active transmission in the licensed band above 928MHz (assumedly [this](https://www.fcc.gov/wireless/bureau-divisions/mobility-division/narrowband-personal-communications-service-pcs) ).

Another observation to make with the single BPSK signal is the impact of the signal frequency (i.e., symbol rate). As you increase the signal frequency value, the size of the main lobe and side lobes should increase accordingly. You can observe this in the frequency display as you adjust the signal frequency, but we also include the image below showing the waterfall plot of the Tx and Rx signals as the signal frequency is adjusted from 1MHz to 2Mhz and then to 4MHz. Observing the time axis in the waterfall plot, we can recognize that the switch from 2MHz to 4MHz occurred around 7.5 seconds in the past and the change from 1MHz to 2MHz occurred approximately 7.5 seconds before that.

![BPSK in Waterfall](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_02.png)

* **NOTE:** The deep nulls between side lobes are clearly observable in the transmit signal since there isn't any additive noise, but the nulls in the receive signal are harder to see as you move away from the main lobe since signal power associated with frequencies further away from the Tx center frequency approaches the noise floor.

* **NOTE:** Observing the time domain characteristics of the transmitted signal in the lower left figure within the image obove, you see the baseband time domain signal for the BPSK signal with 4MHz symbol rate. 
  * The FDM signals have been deselected in the legend to look strictly at the BPSK signal.
  * The signal's Real component is set as either $\pm 0.25$ as expected, and the Imaginary component is always 0.
  * By center-clicking on the figure in your running flowgraph, you can bring up a display menu. Selecting "stem plot" from this menu will change the view to allow you to look at individual samples For any signal frequency (i.e., symbol rate) setting, the minimum number of samples between points where the value changes should be equal to the corresponding number of repetitions (i.e., interpolation). In other words, the samples per symbol value calculated in the equation above.

The final observation for our basic BPSK signal will be made using the constellation display in the Tx and Rx QT GUI Sinks. A screenshot of this output is shown below. At the Tx side, we see an idealized BPSK constellation as expected. In other words, the symbol values always show up on the real axis at either $0.25$ or $-0.25$. However, the Rx view shows a much more complicated picture that includes the channel impairments like attenuation, phase shift, frequency misalignment, and synchronization. Since we haven't accounted for any of these impairments, it is not feasible to decode this signal and get back our transmitted bits! We will discuss these impairments more in a future chapter when implementing a full system with modulation and demodulation.

![BPSK in Constellation](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_03.png)


## Frequency Division Multiplexing (FDM)

The alternative signal path in the [SDR_Hardware_03](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/03_Hardware) flowgraph demonstrates a simplistic FDM implementation where two separate BPSK signals are multiplexed in the digital domain before being upconverted in the hardware and transmitted over the air. FDM is a multiplexing method for sharing the available bandwidth across multiple data streams. Frequency division multiple access (FDMA) is one application of FDM where different frequency ranges are assigned to different users. The basic idea is that multiple signals with bandwidth much less than the sample rate can be merged at the transmit end and then filtered and decoupled at the receive end. 

Functionally, the FDM implementation in the flowgraph multiplies each baseband BPSK signal by a complex sinusoid with different frequencies. These are defined as the intermediate frequencies (IF). The two signals are then added together. Revisiting basic concepts from signals, we can conceptualize the impact by considering the following principles:
* Multiplication in time domain is convolution in frequency domain
* The Fourier Transform of a complex sinusoid (i.e., $e^{j \omega t}$) is a unit impulse at $\omega$
* Convolution with a unit impulse is equivalent to a shift of the signal

Mathematically, these concepts are highlighted below. For simplicity, we introduce the concepts within a continuous time framework; but the outcome is comparable with our digital (i.e., discrete time) implementation.

$$ y\left(t\right) = x\left(t\right) e^{j \omega_{IF} t} \Rightarrow Y\left(f\right) = \frac{1}{2\pi} X\left(\omega\right) * \mathcal{F} \left{e^{j \omega_{IF} t}\right} $$

$$ \mathcal{F} \left{e^{j \omega_{IF} t}\right} = 2\pi \delta\left(\omega - \omega_{IF}\right) $$

$$ Y\left(f\right) = X\left(\omega\right) *  \delta\left(\omega - \omega_{IF}\right) = X\left(\omega - \omega_{IF}\right)

This is seen in the default configuration when running the flowgraph and switching the source signal to the 2 BPSK w/ FDM selection. As seen below, the outcome in frequency domain shows the superposition of two BPSK signals - one centered at the Tx carrier frequency (i.e., at 915MHz) and one at 3MHz above the Tx carrier frequency (i.e., at 918MHz). This corresponds to the IF settings of 0 and 3MHz!

![BPSK adjusted carriers](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_04.png)

In this flowgraph's simplistic FDM implementation, the side lobes of each signal would still impact the other signal (even with the most optimal filtering at the receiver). The gap between the two main lobes is called the guard band, and a larger guard leads to less interference across signals. However, the guard band is essentially unused spectrum and reduces the overall spectral efficiency within the band. To address this, digital filtering can be applied to each baseband BPSK signal prior to IF modulation. In a later chapter, we will also discuss how orthogonal frequency division multiplexing (OFDM) can be applied to address this inefficiency. 

* **NOTE:** As we start to observe the frequency characteristics of the multiplexed signal when varying IF values and symbol rate, it is interesting to view the transmitted signal in time domain (i.e., lower left figure in the image above). Since this instance is the sum of a baseband BPSK signal and a BPSK signal with 3MHz IF, we see that the Imaginary component of the signal is just the Imaginary component of the IF modulated second signal (since the Imaginary component of the baseband BPSK signal, with IF=0, is always 0. The Real component is the Real component of the IF modulated second signal $\pm 0.25$ since the result of the first BPSK signal path is $\pm 0.25e^{j0t}$. 

* **NOTE:** Building on the note above, the interesting oddity of this flowgraph is what occurs when you change IF1 to a non-zero value and then set it back to 0. With GNURadio's implementation of the complex sinusoid in the **Signal Source** block, returning the frequency to 0 will hold the output constant; however, it does not guarantee that the constant will be $e^{j0t} = 1$. This is another minor implementation choice of the specific block that can lead to some confusion if you are not aware of the underlying operation.

The final result of interest in this chapter, shown below, demonstrates the impact of changing the IF values and symbol rate. In this instance, we see IF2 increased first (around the 15s mark). This increases the guard band between the two signals. Next, IF1 is changed to -3MHz and then -5MHz moving the first signal's main lobe _below_ the Tx carrier frequency and further increasing the guard band. Lastly, the signal frequency (i.e., symbol rate) is increased from 1MHz to 2MHz. This increases the rate of each signal and, accordingly, the size of each signal's main lobe. Since the IF values were set far enough apart, there is still a guard band between the two main lobes.

![BPSK adjusted carriers](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/03_Hardware/GRHardware_03_05.png)





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


