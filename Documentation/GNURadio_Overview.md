# GNURadio Overview

## Overview
This is an overview of GNURadio and the GNURadio Companion (GRC). It covers flowgraph creation in GRC, and use of GNURadio for implementing simulated signal processing chains. The examples in this section introduce signal generation and use of the QT GUI tools for signal observation and analysis.

**Tutorial Video:** _Coming Soon_

### Key Learnings
In this tutorial, we will introduce the following concepts:
* GNURadio and GNURadio Companion (GRC)
* Flowgraph creation and execution in GRC
* GNURadio blocks for signal generation
* The QT GUI library for signal observation and visualization
* Organizing GUI layout with GUI Hints
* GNURadio data types and Real/Complex Sinusoids


### GNURadio Blocks to be Introduced
This tutorial will introduce the following blocks from the core GNURadio library:

* Options Block 
* Signal Source Block
* Throttle Block
* Qt GUI Library
  * QT GUI Sink Block
  * QT GUI Time Sink Block
  * QT GUI Frequency Sink Block
* Float to Complex Block

We will ultimately create the flowgraph shown below. This flowgraph is also available in the [flowgraphs](https://github.com/UCaNLabUMB/SDR_Tutorials/tree/main/Flowgraphs/01_Overview) directory.

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_01.png)


## Flowgraph Creation
We assume that you already have GNURadio [installed](https://wiki.gnuradio.org/index.php/InstallingGR). Historically, we have been using the PyBOMBs installation method; however, there are other suggested methods for installing newer versions of GNURadio (i.e., after V3.8). With a working installation of GNURadio, we can start creating our first flowgraph by following the steps below.

### Create Flowgraph in GRC: 
_Discuss GNURadio vs. GRC_

### Define Flowgraph Options: 
_Discuss options block (ID/title/.etc) and ID as file name for python file to be generated_

### Adding Blocks: 
_sig source, throttle, QT Sink... discuss complex blocks and purpose of throttle_

### Connecting Blocks: 

### Setting Parameters: 
_Discuss frequency in sig source, sample rate variable and change of values in all blocks (to revisit later)_

## Flowgraph execution

### Generating Python Code

### Executing Flowgraph with Python

### Executing Flowgraph within GRC


## Flowgraph Additions and Observations
_Add real sine example and real-sine with float-to-complex block_


![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview_02.png)

## References
_Coming Soon_


## Next Chapter
[GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)

