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

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_01.png)

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

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_02.png)


### Define Flowgraph Options: 
Our first step is to define the flowgraph's high-level settings. This is done by double-clicking on the **Options** block to open the window below. Here, you see multiple settings that we can configure. Note that the ID value will ultimately be the name of the python file that is created by GRC. We will revisit this later. The title is what will be displayed on the GUI when the flowgraph is run, so this should be a short human-readable description.

![Options Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_03.png)


### Adding and Connecting Blocks: 
GNURadio's core library consists of an extensive set of signal processing blocks that can be used "out-of-the-box." The list on the right hand side of the GRC environment shows the available blocks that can be added to your flowgraph. To find a block, you can select the search icon in GRC's menu bar and begin typing the name of the block. Once you see the desired block in the list, you can either click on the name and drag it into the main windo, or double-click the name and it will be added. For our first flowgraph, we can search and add **Signal Source**, **Throttle**, and **QT GUI Sink** blocks. 

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_04.png)

Once the blocks have been added, you can click on the blocks and drag them around the main window to place them as desired. Once the blocks are placed, we need to connect block outputs to block inputs in order to determine how samples flow from block to block in our flowgraph. This is done by clicking on the _out_ port of one block and the _in_ port of another block. If done correctly, a line should be displayed to indicate the direction of the data flow.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_05.png)

* **NOTE:** The throttle block is incredibly important for _simulation_ flowgraphs since it manages the real-time rate of samples flowing through the block (and, accordingly, through your flowgraph). This is the only simulation block where the indicated sample rate actually manages the rate of samples. When sample rate is defined in other blocks (e.g., the Signal Source or QT GUI Sink blocks) the value is used for determining what values to generate at specific sample numbers or how to visualize/display the incoming signal stream. Generally speaking, most blocks are unaware of actual time and operate on digital samples, therefore we provide the _assumed_ sample rate as a parameter to these blocks so that the signal processing blocks can associate incoming samples with their relevant time characteristics. Alternatively, blocks that interact with hardware can also manage the rate of samples flowing through our flowgraphs (we will revisit this later).


### Setting Parameters: 
Once the blocks have been added and connected, we can change parameters of the various blocks to define how they work (e.g., how they generate, process, or display signals). For this example, we can simply double-click on the signal source to see the list of available parameters, and set the frequency to `200000` (or `2e5` if you prefer scientific notation). Click OK and the frequency will be updated in the parameters shown on the block. 

In the Signal Source block's parameters, we should also notice that the Sample Rate parameter is set to `samp_rate` and this shows up as 32k in the parameters displayed on the block. This is because `samp_rate` is defined as a variable in the variable block that was included in our flowgraph by default. Since 32k samples/sec is not going to do a great job of showing our 200KHz sinusoid, we can update the value of `samp_rate` by double clicking the variable block and changing our value to `5e6` (i.e., 5M samples/sec). Notice that this changes the sample rate shown on your Throttle block and your QT GUI Sink block as well! This is the benefit of the variable block - since `samp_rate` is used as the Sample Rate parameter for all of our blocks, we have a single centralized location where changing `samp_rate` updates the defined sample rate in all of these blocks. We will discuss more about variables in our [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md) tutorial.


## Flowgraph execution
We are now ready to run our flowgraph! We will first describe how GRC generates the desired Python code for our GNURadio flowgraph, then we will discuss some observation tools available in the QT GUI Sink.

### Generating Python Code
Since GRC is a _tool_ for creating GNURadio flowgraphs, we can use it to generate the python code that will ultimately run our desired flowgraph. This can done by selecting the Generate option in the top menu of GRC. At this point, you will be asked to provide a file name. When you give this file name, you are naming the _GRC file_. The generated _python file_ will be given a name that is defined by the ID value that we set earlier in the flowgraph's **Options** block!!

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_06.png)

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_07.png)

### Executing Flowgraph
If you look in the directory where you saved your `.grc` file, you should notice two different files. The `.grc` file which maintains the blocks, parameter settings, and connections to be displayed in GRC, and a `.py` file that has the actual python GNURadio flowgraph to be executed. If you open these files with a text editor, you can explore some of the characteristics of each; but for the purpose of this tutorial we are ready to execute the flowgraph. You can do this from the command line with Python (if you want to start the created flowgraph without opening GRC):

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_08.png)

Or, alternatively (and more commonly), you can execute the flowgraph directly in GRC with the execute button in the main menu. This will generate the python code AND execute the generated python code.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_09.png)


## Flowgraph Additions and Observations
_Add real sine example and real-sine with float-to-complex block, Discuss data types, conversions, GUI Hints_

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_01.png)

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_10.png)

## References
* GNURadio: [https://www.gnuradio.org/about/](https://www.gnuradio.org/about/)


## Next Chapter
[GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)

