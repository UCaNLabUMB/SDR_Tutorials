# GNURadio Overview

## Overview
This is an overview of GNURadio and the GNURadio Companion (GRC). It covers flowgraph creation in GRC, and use of GNURadio for implementing simulated signal processing chains. The examples in this section will introduce:
* GNURadio and GNURadio Companion (GRC)
* Flowgraph creation and execution in GRC
* GNURadio blocks for signal generation
* GNURadio data types and Real/Complex Sinusoids
* The QT GUI library for signal observation and visualization
* Techniques to manage GUI layout with GUI Hints

**Tutorial Video:** _Coming Soon_


### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_01.png)

We will ultimately create the [GNURadio_Overview flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/01_Overview) shown above. This flowgraph generates three different signals and displays them using different graphical display tools from the QT GUI (Graphical User Interface) library. 

We will discuss how to create and excute this flowgraph in GRC. We also introduce the differences related to the three different signals, namely:
* A complex-valued sinusoid represented as a complex data type
* A real-valued sinusoid represented as a float data type
* A real-valued sinusoid represented as a complex data type


### GNURadio Blocks to be Introduced
This tutorial will introduce the following blocks from the core GNURadio library:
* Options Block 
* Signal Source Block
* Throttle Block
* QT GUI Library:
  * QT GUI Sink Block
  * QT GUI Time Sink Block
  * QT GUI Frequency Sink Block
* Float to Complex Block




## Flowgraph Creation
We assume that you already have GNURadio [installed](https://wiki.gnuradio.org/index.php/InstallingGR). Historically, we have been using the PyBOMBs installation method; however, there are other suggested methods for installing newer versions of GNURadio (i.e., after V3.8). With a working installation of GNURadio, we can start creating our first flowgraph by following the steps below.

### Create Flowgraph in GRC: 
GNURadio is an open source software toolkit for software defined radio (SDR). While GNURadio is based in the Python programming language, many users stick to the _GNURadio Companion_ tool, or GRC, which provides a simple graphical environment for managing GNURadio flowgraphs (i.e., signal processing chains). To get started with GRC, you can simply type `gnuradio_companion` in a terminal. This will open the GRC tool for developing GNURadio flowgraphs. If this is your first time opening GRC, you should see a (mostly) blank window with two blocks: an **Options** block, where you will define various high-level flowgraph settings, and a **Variable** block with a value defined for a variable called "samp_rate".

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_02.png)


### Define Flowgraph Options: 
Our first step is to define the flowgraph's high-level settings. This is done by double-clicking on the **Options** block to open the window below. Here, you see multiple settings that we can configure. 

![Options Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_03.png)

* **NOTE:** The ID value will ultimately be the name of the python file that is created by GRC (we will revisit this later). The title is what will be displayed on the GUI when the flowgraph is run, so this should be a short human-readable description.

### Adding and Connecting Blocks: 
GNURadio's core library consists of an extensive set of signal processing blocks that can be used "out-of-the-box." The list on the right hand side of the GRC environment shows the available blocks that can be added to your flowgraph. To find a block, you can select the search icon in GRC's menu bar and begin typing the name of the block. Once you see the desired block in the list, you can either click on the name and drag it into the main window, or double-click the name and it will be added. For our first flowgraph, we can search and add **Signal Source**, **Throttle**, and **QT GUI Sink** blocks. 

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_04.png)

Once the blocks have been added, you can click on the blocks and drag them around the main window to place them as desired. Once the blocks are placed, we need to connect block outputs to block inputs in order to determine how samples flow from block to block in our flowgraph. This is done by clicking on the _out_ port of one block and the _in_ port of another block. If done correctly, a line should be displayed to indicate the direction of the data flow.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_05.png)

* **NOTE:** The throttle block is incredibly important for _simulation_ flowgraphs since it manages the real-time rate of samples flowing through the block (and, accordingly, through your flowgraph). The **Throttle** block is the only simulation block where the indicated sample rate actually manages the rate of samples. When sample rate is defined in other blocks (e.g., the Signal Source or QT GUI Sink blocks) the value is used for determining what values to generate at specific sample numbers or how to visualize/display the incoming signal stream. Generally speaking, most blocks are unaware of actual time and operate on digital samples, therefore we provide the _assumed_ sample rate as a parameter to these blocks so that the signal processing blocks can associate incoming samples with their relevant time characteristics. Alternatively, blocks that interact with hardware can also manage the rate of samples flowing through our flowgraphs (we will revisit this later).


### Setting Parameters: 
Once the blocks have been added and connected, we can change parameters of the various blocks to define how they work (e.g., how they generate, process, or display signals). For this example, we can simply double-click on the signal source to see the list of available parameters, and set the frequency to `200000` (or `2e5` if you prefer scientific notation). Click OK and the frequency will be updated in the parameters shown on the block. 

In the Signal Source block's parameters, we should also notice that the Sample Rate parameter is set to `samp_rate`. This causes Sample Rate to show up as 32k in the list of parameters displayed on the block. This is because `samp_rate` is defined as a variable in the variable block that was included in our flowgraph by default. Since 32k samples/sec is not going to do a great job of showing our 200KHz sinusoid, we can update the value of `samp_rate` by double clicking the variable block and changing our value to `5e6` (i.e., 5M samples/sec). Notice that this changes the value of Sample Rate shown on your Throttle block and your QT GUI Sink block as well! This is the benefit of the **Variable block**. Since `samp_rate` is used as the Sample Rate parameter for all of our blocks, we have a single centralized location where changing the value of `samp_rate` in this Variable block will update the defined Sample Rate in all of these blocks. We will discuss more about variables in our [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md) tutorial.


## Flowgraph execution
We are now ready to run our flowgraph! We will first describe how GRC generates the desired Python code for our GNURadio flowgraph, then we will discuss some observation tools available in the QT GUI Sink.

### Generating Python Code
Since GRC is a _tool_ for creating GNURadio flowgraphs, we can use it to generate the python code that will ultimately run our desired flowgraph. This can done by selecting the Generate option in the top menu of GRC. At this point, you will be asked to provide a file name. When you give this file name, you are naming the _GRC file_. The generated _python file_ will be given a name that is defined by the ID value that we set earlier in the flowgraph's **Options** block!!

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_06.png)

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_07.png)

### Executing Flowgraph
If you look in the directory where you saved your `.grc` file, you should notice two different files. The `.grc` file which maintains the blocks, parameter settings, and connections to be displayed in GRC, and a `.py` file that has the actual python GNURadio flowgraph to be executed. If you open these files with a text editor, you can explore some of the characteristics of each; but for the purpose of this tutorial we are ready to execute the flowgraph. You can do this from the command line with Python (if you want to start the created flowgraph without opening GRC):

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_08.png)

Or, alternatively (and more commonly), you can execute the flowgraph directly in GRC with the execute button in the main menu. This will generate the python code AND execute the generated python code.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_09.png)


## Flowgraph Additions and Observations
Now that we've created a simple flowgraph to generate and display a signal, we can extend the idea for some similar signals. We will use this opportunity to discuss a few different data types in GNURadio, and discuss some basic signal characteristics of real-valued and complex-valued sinusoids. The image below has three repetitions of the signal source and sink from our original flowgraph, with a few differences in each version. The first thing to notice is the difference in color of the various in and out ports for different blocks. The color represents different data types for the samples that flow out of or into the different blocks. There are many different data types in GNURadio, but this example shows `complex` data types in blue and `float` data types in orange. 

Many blocks in GNURadio can be set for use with different data types. Beginning with our original flowgraph, you can copy/paste the **Signal Source** block to create a new block. If you open the new block's parameter list, we can find a drop down list for "output type" and change this value to "float". If you apply the changes, you will notice that the out port on the new block has changed color! 

* **NOTE:** As a quick-key option, you can also select the block and press the up/down arrows on your keyboard to change the data type without needing to open the block's parameters list. This is a nice option if you want to quickly change the input/output types for a set of blocks. You can select all of the blocks of interest and press up/down to change all of their data types together (without needing to individually open the parameter list of each block).

This addresses the differences between the top two signal chains. Namely, the top left signal chain is generating and observing a complex-valued sinusoid where the samples are all `complex` data types, whereas the top right signal chain is generating a real-valued sinusoid where the samples are all `float` data types. If you are new to signal processing, it is important to note that these are different signals!! We will see this in shortly when observing the flowgraph's output.

It is also important to note that a `complex` data type in GNURadio is essentially the combination of two real-valued `float` types. Specifically, the real and imaginary components of the `complex` value are essentially two different `float` values that are stored together. This is seen in the bottom signal chain where we combine the real valued sinusoid with another real-valued signal (in this case, a constant value of 0) using the **Float to Complex** block. The complex output of this block is a real-valued sinusoid stored in the form of a `complex` data type. In other words, the complex signal coming out of this block has a real component equal to the input real-valued sinusoid and an imaginary component equal to 0.


![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_01.png)

When executing this flowgraph, we can see the results below. The left figure has our original output of the QT GUI Sink where we can observe the signal in a few different domains. The middle figures show the time domain representations of our two real-valued sinusoids. And the right figures show the frequency domain representations of the two real-valued sinusoids. 

* **NOTE:** If you create this flowgraph on your own, you will likely notice that the GUI structure is not as clean as in the figure below. This cleanliness comes from using a nice feature in the QT GUI blocks - the _GUI Hint_ parameter. This allows you to observe your GUI as a grid and specify the location and size of any GUI components. If you open the parameter list for one of the QT GUI blocks, you will see the _GUI Hint_ parameter towards the bottom of the list. This parameter takes 4 values separated by commas to indicate the starting row, starting column, number of rows, and number of columns. For example, the parameter for the GUI Sink is set as `0,0,2,1` to start in the top left corner (i.e., grid location 0,0) and extend over 2 rows and 1 column. Similarly, the top middle time domain figure has its _GUI Hint_ parameter set as `0,1,1,1` which specifies that it should located at row 0 column 1 and extend over 1 row and 1 column.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_10.png)

Notice that the top signal (the output of the time sink using the `float` data type) shows a single sinusoidal signal. The bottom signal (the output of the time sink using the `complex` data type) is displaying two signals representing the real and imaginary components of the incoming complex-valued signal. As expected, the imaginary component (i.e., Signal 2) is a constant value of 0 since this was what we assigned in the flowgraph. In the time domain view in the left figure (the complex sinusoid) we see two sinusoids with 90 degree phase shift. From a signals perspective, this should be familiar as a complex sinusoid in the form of $x(t) = e^{jwt}$ or similarly, $x(t) = e^{jwt} = cos(wt) + jsin(wt)$ by applying Euler's identity. The real and imaginary components of this signal (i.e., $cos(wt)$ and $sin(wt)$, respectively) are what we see in the plot!

Similarly, we know that the real valued cosine signal is defined as:

$$x(t) = cos(wt) = cos(wt) + j0 = 0.5(e^{jwt} +e^{-jwt})$$

where $cos(wt)$ and $cos(wt) + j0$ can be thought of as our two different representations for the real-valued sinusoid (i.e., the signals represented with `float` and `complex` data types, respectively). Obseving our frequncy plots for the complex sinusoid and the two real-valued sinusoid representations, we can notice the difference. Specifically, the complex sinusoid only has a single peak at 200KHz relating to the $w$ in $e^{jwt}$ whereas the real-valued sinusoids show peaks at 200KHz and -200KHz, representing the positive and negative frequencies present in $e^{jwt} +e^{-jwt}$. Furthermore, the 0.5 amplitude scale of each component in the real-valued sinusoid relates to a quarter of the power associated with $e^{jwt}$. This can be seen in the 6dB difference between the peak of the complex sinusoid and the peaks of the real valued sinusoids!

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/01_Overview/GROverview_11.png)

* **NOTE:** We use using a continuous time representation in the presented notation above, but it is important to reiterate that we are observing discrete time signals in the digital signal processing world of GNURadio. Even the time domain plots we observe can be somewhat misleading since the visualization here is essentially "connecting the dots" of discrete time samples. To see this more clearly, we can change the view in these plots by setting the _Stem Plot_ property to _yes_. We will revisit this later in the tutorial series.

## References
* GNURadio: [https://www.gnuradio.org/about/](https://www.gnuradio.org/about/)


## Next Chapter
[GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)

