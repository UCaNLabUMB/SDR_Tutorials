# GNURadio Basics

## Overview
In this tutorial, we will extend our knowledge of GNURadio and consider some best practices for working with modifiable flowgraphs. This includes an extended discussion about the value and usage of GNURadio variables, and an introduction to how we can enable, disable, and bypass blocks prior to execution of a flowgraph. Furthermore, we will introduce additional QT GUI blocks that allow for modification of a flowgraph's variables and signal paths while a flowgraph is running.


**Tutorial Video:** _Coming Soon_


### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04.png)

This tutorial will work towards developing the [GNURadio_Basics flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) shown above. This flowgraph generates a noisy sinusoidal signal and creates a GUI with a single display. The GUI also includes an interactive interface that allows users to select the real- or complex-valued sinusoid, change the frequency of the signal, and enable/disable a band pass filter. From a signal perspective, this will provide a high-level demonstration of the benefits related to filtering out-of-band noise from a desired signal. We will also demonstrate the frequency characteristics of a square wave signal, and the associated impact of filtering a noisy square wave.

Along the way, we will discuss how to use GRC tools to modify flowgraphs without deleting blocks. This is a helpful process for debugging flowgraphs or creating multi-purpose flowgraphs. Specifically, we will show how GRC allows you to:
* Enable and Disable blocks to remove them from the flowgraph without deleting them completely.
* Bypass Blocks without the need to create a new connection.
* Use QT GUI blocks to manually change parameters and signal paths while a flowgraph is running.


### GNURadio Blocks to be Introduced
This tutorial will introduce the following blocks from the core GNURadio library:
* Noise Source Block
* Add Block
* Band Pass Filter Block
* Virtual Source/Sink Blocks
* QT GUI Range Block
* QT GUI Chooser Block
* Selector Block



# Modifying Flowgraphs Prior to Execution
This tutorial will demonstrate the value of observing impacts that come from changing a single parameter in a flowgraph (e.g., a variable, block used, presence or absence of a block, etc.). 
We have already seen how to add and connect blocks to create a desired flowgraph. As such, we could conceivably create multiple copies of a flowgraph and make the desired changes within the copies while keeping the rest of the signal processing chain common across copies of the original flowgraph. However, multiple copies of a flowgraph can become a problem if we want to modify the section of the signal processing chain that is common across copies. 
It can be beneficial to have a common signal processing chain where we can modify a small piece of the flowgraph for comparison, while keeping the rest of the flowgraph consistent. 

In the first flowgraph of this tutorial, [GNURadio_Basics_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) shown below, we start with two signal chains from our Overview tutorial (i.e., a complex- and real-valued signal source, both ultimately represented as a complex data type). We also include a noise source block that is set to generate an additive white Gaussian noise (AWGN) signal. The signal and noise are both combined in the addition block, and the resulting signal is passed through a band pass filter with the goal of isolating the desired signal and removing unwanted noise. After the filter, we have the throttle and QT GUI blocks that we have already seen.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01.png)

* **NOTE:** The portion of the signal chain that generates the real-valued signal is currently grayed out, meaning that it has been _disabled_. We will return to this shortly, but we note that the flowgraph would give an error if this was not disabled since it would lead to two different signals going into the same input port on the Add block. 



## Filters and Variables
We first discuss the **Bandpass Filter** block and how we can use variables to make sure that the filter stays aligned with our desired signal. You can notice in the flowgraph above that we have also included a new **Variable block** to introduce a variable named sig\_freq. This variable has been used to assign the Frequency property in both of our **Signal Source** blocks. The benefit of using a variable here is that we have a single location where we can change the variable's value. In this way, we do not need to open both signal sources to change the signal frequencies separately. 

* **NOTE:** While this might not seem significant in this case, the value of variables becomes much more significant as the flowgraphs scale in complexity and common values are shared across many blocks (in the same way that we use variables in conventional coding projects to avoid hard coding). 

In the figure below, we can also see how this sig\_freq variable is used to set the frequency bounds of our filter in a way that keeps our desired signal at the center of the filter's pass band. With this configuration, the filter's low/high cutoff range will always be 25KHz below/above the signal source's frequency.

![Filter Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_01.png)

When running the the flowgraph, we can observe the output below with the 50KHz default signal. We see that the peak signal power is at 50KHz and the initial additive noise is still present between 25KHz and 75KHz (i.e., the pass band for our band pass filter). When adjusting the sig\_freq variable to 200KHz and running again, we get the results in the second figure below. Here, the peak signal power shows up at 200KHz (as expected) and the filter's pass band has been updated to range from 175KHz to 225KHz. 

![50KHz Signal](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_02.png)

![200KHz Signal](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_03.png)

* **NOTE:** The key takeaway here is that we only need to update the single value of the sig\_freq variable, as opposed to editing the Frequency property in the signal source block _and_ the Low/High Cutoff Frequency prameters in the filter block.


## Block Status: Enable, Disable, Bypass
Continuing to observe the flowgraph in [GNURadio_Basics_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), we will now introduce GRC functionality for enabling/disabling blocks and bypassing blocks. Returning to the disabled signal path for the real-valued sinusoid, we can highlight the 3 blocks in this signal path and then select the enable icon in the menu bar. When we do this, the flowgraph will show an error since we now have two signals going into one port in the **Add** block. To resolve this, we select the complex Signal Source block and select the disable icon in the menu bar. 

![Enable Block](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_04.png)

![Disable Block](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_05.png)

If we run the flowgraph again, we should now see the presence of the signal at 50KHz and -50KHz (or at the positive and negative value of whatever frequency value you've set for _sig\_freq_). Recall that this is what we expect to see for a real-valued sinusoid: $cos(wt) = 0.5(e^{jwt} +e^{-jwt})$.

![50KHz Signal Real](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_06.png)

In addition to the option to enable/disable blocks, we can also bypass a block within GRC. To demonstrate the need for this, you can observe what happens when you disable the **Bandpass Filter** block. This creates an error in the flowgraph since the output of the **Add** block is no longer connected to anything, and there is no longer an input to the **Throttle** block. As an alternative, we can select the **Bandpass Filter** and then select the Bypass icon in the menu bar. This will cause the flowgraph to appear as seen below. When running this flowgraph, the **Bandpass Filter** block will no longer function and the input to this block will be immediately placed set as the block's output. 

![Bypass Block](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_07.png)

![Bypass Flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_08.png)

Running the flowgraph as shown above will now give the results below. In the absence of the filter, we still see the signal at the desired frequencies; but significantly more noise is present. This is more clearly seen when observing the signal in the time domain.

![Waterfall](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_09.png)

![Time Domain](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_01_10.png)





# Dynamic Flowgraphs
The ability to enable/disable/bypass blocks allows for realtively quick changes to a flowgraph in an offline manner. However, we also look to modify flowgraph parameters and characteristics while the flowgraph is running. In this section, we will observe the [GNURadio_Basics_02.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), [GNURadio_Basics_03.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), and [GNURadio_Basics_04.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) flowgraphs to demonstrate how we can incorporate GUI tools that allow users to manually control the flowgraph while the flowgraph is running.

## Dynamic Variable Modifications
Beginning with [GNURadio_Basics_02.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), shown below, we can notice that the only significant change in this flowgraph is that we've removed the **Variable** block where _sig\_source_ was set previously, and replaced it with a **GT GUI Range** block. 

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_02.png)

When selecting the **GT GUI Range** block, we see the set of properties shown below. Most noticeably, we see that the ID is defined as _sig\_freq_. This creates a variable in the same way as the **Variable** block, except we will now have the ability to manually change the value of the variable while the flowgraph is running. The Label property is what will be shown in the GUI (i.e., a human-readable description of the variable). The Start and Stop properties set the smallest and largest possible values of the variable, and the Step property indicates the step size for possible values of the variable. For example, the property settings below imply that we can set _sig\_freq_ to 50KHz, 100KHz, 150KHz, etc. with a maximum value of 500KHz. When the flowgraph starts, _sig\_freq_ will initially be set to 100KHz. 

![GUI Range Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_02_01.png)

When this flowgraph is run, we can see the slider bar and counter labeled "Signal Frequency" at the top of the GUI. In the image below, we have changed this variable's value while the flowgraph was running and the corresponding changes can be seen over time in the Waterfall view shown below.

![GUI Range Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_02_02.png)

* **NOTE:** The variable _sig\_freq_ is still associated with the signal frequency in the Signal Source block AND the high/low frequencies of the Band Pass filter block, so the filter is moving along with the signal in this scenario.


## Dynamic Path Selection
The final additions for this section, in [GNURadio_Basics_03.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) and [GNURadio_Basics_04.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), give an additional GUI option to include manual selection of configuration parameters from a list of options. In particular, we introduce the ability to dynamically make the changes that we had previously done by enabling/disabling/bypassing blocks in the offline manner. 

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_03.png)

The first thing to notice in the flowgraph above is that we have re-introduced the virtual sink/source blocks to make the signal paths more clear. In the lower portion of the signal chain, we also see that we've introduced two **Selector** blocks. These blocks simply take a set of inputs and define which input is assigned to the output (or, optionally, which inputs are assigned to which outputs). The first **Selector** block takes in both of our generated signals (i.e., the real- and complex- valued sinusoids) and passes one of the signals to the output port. Opening this block should bring up the properties below.

![Selector Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_03_01.png)

We can see that we have 2 inputs and 1 output specified. If you change these values, the number of ports available on the block will be updated in GRC. Since there is only one output port in our example, we set the output index to 0 so that the specified input will always go to this port. To determine which input signal goes to the specified output port, we specify a variable named _path\_select_ so that the selected input can be changed while the flowgraph is running. 

This is where the **QT GUI Chooser** block comes in. When opening the QT GUI Chooser block with ID _path\_select_, we see the properties below.

![QT GUI Chooser Properties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_03_02.png)

Similar to the **QT Range** block, the **QT GUI Chooser** block creates a variable that can manually changed while the flowgraph is running. However, in this case we have a more specific set of values that can be selected (rather than simply specifying a range of values). We have defined 2 options where Option 0 is the integer value 0 and Option 1 is the integer value 1. These are the values that are assigned to the _path\_select_ variable and, accordingly, the values that get set as the input index for the selector block. For readability, we use the labels to show "Real Sine" and "Complex Sine" in the GUI as the options that the user can select from.

Following a similar process, we have included a **Selector** block to optionally select between the output of the **Bandpass Filter** block or the output of the **Add** block. The input index property in this block is set to _filter\_select_ and we have created another **QT GUI Chooser** block that allows the user to choose between "Enable" or "Bypass" for the Filter Selection. This ultimatley allows the user to bypass the filter while the flowgraph is running. The image below shows the GUI that is created when this flowgraph is run. 

![Flowgraph Running](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_03_03.png)

* **NOTE:** In the waterfall plot above, we can see that we have started with a 100KHz real-valued sinusoid. After a few seconds, we changed the frequency to 150KHz and then changed the signal source to the complex sine. Shortly after, we selected the option to bypass the filter and then set the signal source back to a real sine. Finally, we increased the signal frequency to 200KHz and then, finally, to 350KHz.

The final flowgraph in this section, [GNURadio_Basics_04.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics), is a copy of the previous example with the addition of one more **QT GUI Chooser** block. This last block allows the user to select the waveform (i.e., Cosine or Square wave) while the flowgraph is running.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04.png)

The property settings for this **QT GUI Chooser** block, shown below, are similar to what we saw earlier; except we are calling values from the GNURadio analog library. Ultimately, this leads to integer values; however, this ensures that the values are understood correctly by the **Signal Source** blocks. 

![QT GUI Chooser Propreties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_01.png)

When opening the **Signal Source** blocks, we see that the variable name _Sig\_Type_ has been entered in the Waveform drop down menu. This can be somewhat confusing because you need to select whatever is initially in the drop down menu and type in the name of your variable.

![Signal Source Propreties](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_02.png)

Running this flowgraph produces the results below. We now see an additional selection box for "Waveform" that allow the user to switch between a Cosine and Square Wave signal.

![Flowgraph Running Waterfall](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_03.png)

* **NOTE:** In the waterfall plot above, we see that we initially started with a real valued sinusoid at 100KHz. The filter was then bypassed, and the waveform was changed to a square wave (leading to the higher frequncy components at multiples of the fundamental frequency). As the frequency of the square wave is increased to 150KHz and then 200KHz, the higher frequency components are also adjusted to multiples of the fundamental frequency. When the filter is then enabled, we can still see the higher frequency components from the initial square wave; but they are significantly reduced while the fundamental frequency remains consistent.

The series of snap shots below demonstrates some of this implications in the time domain. First, we see a 50KHz real-valued sinusoid with the additive noise filtered out. Comparing with the second image where the filter is bypassed, we can clearly see the noise filtering benefits of our **Band Pass Filter** block!

![Time Doman Cos Filter](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_04.png)

![Time Doman Cos No Filter](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_05.png)

The next image below shows the noisy square wave signal in time domain. We can clearly see the underlying square wave, but the signal is also very noisy since we are still bypassing the filter block. 

![Time Doman Square Filter](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_06.png)

When we re-enable the filter, we see the noise reduce as desired, but we have also significantly reduced the higher frequency components (and the DC component) of our square wave, so our observation now looks similar to a sinusoid!

![Time Doman Square No Filter](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/02_Basics/GRBasics_04_07.png)





# References
* [GNURadio Tutorials](https://wiki.gnuradio.org/index.php?title=Tutorials): General tutorials on building flowgraphs in GNU Radio.

# Tutorial Chapters

* **Next Chapter:** [SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md) 
* **Previous Chapter:** [GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)

| Chapter | Topic | Summary 
| --- | --- | --- |
|  1  | [GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)                   | Introduction to Flowgraphs, source/sink blocks, and data types
|  2  | GNURadio Basics                                                                                                                 | Introduce flowgraph best practices, variables, and dynamic control
|  3  | [SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md)                             | Introduce USRPs, hardware addressing, and over-the-air waveform transmission
|  4  | [GNURadio Remote Command and Control](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_CaC.md)      | Introduce multi-node systems with XMLRPC and ZMQ
|  5  | [Basic Communicatons](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Comms.md)                    | Introduce simulation and over-the-air data transmission
|  6  | [Automated Data Collection](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Automation.md)         | Combine XMLRPC, ZMQ, and OFDM to automate Packet Error Rate Testing


