# GNURadio Basics

## Overview
In this tutorial, we will extend our knowledge of GNURadio and consider some best practices for working with modifiable flowgraphs. This includes an extended discussion about the value and usage of GNURadio variables, and an introduction to how we can enable, disable, and bypass blocks prior to execution of a flowgraph. Furthermore, we will introduce additional QT GUI blocks that allow for modification of a flowgraph's variables and signal paths while a flowgraph is running.


**Tutorial Video:** _Coming Soon_


### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_03.png)

This tutorial will work towards developing the [GNURadio_Basics flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) shown above. This flowgraph generates a noisy sinusoidal signal and creates a GUI with a single display. The GUI also includes an interactive interface that allows users to select the real- or complex-valued sinusoid, change the frequency of the signal, and enable/disable a band pass filter. From a signal perspective, this will provide a high-level demonstration of the benefits related to filtering out-of-band noise from a desired signal. We will also demonstrate the frequency characteristics of a square wave signal, and the associated impact of filtering a noise square wave.

Along the way, we will discuss how to use GRC tools to modify flowgraphs without deleting blocks. This is a helpful process for debugging flowgraphs or creating multi-purpose flowgraphs. Specifically, we will show how GRC allows you to:
* Enable and Disable blocks to remove them from the flowgraphing without deleting them completely.
* Bypass Blocks without the need to create a new connection.


### GNURadio Blocks to be Introduced
This tutorial will introduce the following blocks from the core GNURadio library:
* Noise Source Block:
* Add Block:
* Band Pass Filter Block
* Virtual Source/Sink Blocks
* QT GUI Range Block
* QT GUI Chooser Block
* Selector Block



# Modifying Flowgraphs Prior to Execution
The high level goal of this tutorial relates observation of the impacts that come from changing a single parameter in a flowgraph (e.g., a variable, block used, presence or absence of a block, etc.). 
We have already seen how to add and connect blocks to create a desired flowgraph. As such, we could conceivably create multiple copies of a flowgraph and make the desired changes within the copies while keeping the rest of the signal processing chain common across copies of the original flowgraph. However, multiple copies of a flowgraph can become a problem if we want to modify the section of the signal processing chain that is common across copies. 
It can be beneficial to have a common signal processing chain where we can modify a small piece of the flowgraph for comparison, while keeping the rest of the flowgraph consistent. 

In the first flowgraph of this tutorial, [GNURadio_Basics_01.grc](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/02_Basics) shown below, we start with two signal chains from our Overview tutorial (i.e., a complex- and real-valued signal source, both ultimately represented as a complex data type). We also include a noise source block that is set to generate an additive white Gaussian noise (AWGN) signal. The signal and noise are both combined in the addition block, and the resulting signal is passed through a band pass filter with the goal of isolating the desired signal and removing unwanted noise. After the filter, we have the throttle and QT GUI blocks that we have already seen.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_01.png)

* **NOTE:** The portion of the signal chain that generates the real-valued signal is currently grayed out, meaning that it has been _disabled_. We will return to this shortly, but we note that the flowgraph would give an error if this was not disabled since it would lead to two different signals going into the same input port on the Add block. 



## Filters and Variables
We first discuss the **Bandpass Filter** block and how we can use variables to make sure that the filter stays aligned with our desired signal. You can notice in the flowgraph above that we have also included a new **Variable block** to introduce a variable named sig\_freq. This variable has been used to assign the Frequency parameter in both of our **Signal Source** blocks. The benefit of using a variable here is that we have a single location where we can change the variable's value. In this way, we do not need to open both signal sources to change the signal frequencies separately. 

* **NOTE:** While this might not seem significant in this case, the value of variables becomes much more significant as the flowgraphs scale in complexity and common values are shared across many blocks (in the same way that we use variables in conventional coding projects to avoid hard coding). 

In the figure below, we can also see how this sig\_freq variable is used to set the frequency bounds of our filter in a way that keeps our desired signal at the center of the filter's pass band. With this configuration, the filter's low/high cutoff range will always be 25KHz below/above the signal source's frequency.

![Filter Parameters](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_01_01.png)

When running the the flowgraph, we can observe the output below with the 50KHz default signal. We see that the peak signal power is at 5KHz and the initial additive noise is still present between 25KHz and 75KHz (i.e., the pass band for our band pass filter). When adjusting the sig\_freq variable to 200KHz and running again, we get the results in the second figure below. Here, the peak signal power shows up at 200KHz (as expected) and the filter's pass band has been updated to range from 175KHz to 225KHz. 

![50KHz Signal](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_01_02.png)

![200KHz Signal](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_01_03.png)

* **NOTE:** The key takeaway here is that we only need to update the single value of the sig\_freq variable, as opposed to editing the Frequency parameter in the signal source block _and_ the Low/High Cutoff Frequency prameters in the filter block.


## Block Status: Enable, Disable, Bypass
_Describe add block and noise source, and ability to bypass the filter_

_Describe second path, and ability to enable/disable for switching paths_




## Dynamic Flowgraphs
![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_02.png)

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/Basics/GRBasics_03.png)

_Describe range for signal frequency_

_Describe selector/chooser to update flowgraph while running_

_Discuss the filtering impact on a square wave... changing the source signal to square from cos_

## References
* [GNURadio Tutorials](https://wiki.gnuradio.org/index.php?title=Tutorials): General tutorials on building flowgraphs in GNU Radio.

* [QT GUI Waterfall Sink](https://wiki.gnuradio.org/index.php/QT_GUI_Waterfall_Sink): Visualizing signals with the waterfall plot.


## Next Chapter
[SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md) 

## Previous Chapter
[GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)
