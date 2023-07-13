# Simple GNURadio TX/RX
## Overview
This is the overview of an simple introdcution to GNURadio. In this section we will build a simple Signal Transmission and Receiving flowgraph within GNURadio.
The video will demonstrate the flowgraph creation from start to finish ending with a Flowgraph run.

### Key Learnings
GNURadio is a software toolkit for building and executing signal processing systems.

A simple Signal Transmission and Receiving flowgraph is created in GNURadio.

The flowgraph includes a signal source block, which generates a simulated signal waveform.

The float to complex block converts the signal from floating point to complex exponential.

The throttle block controls data flow during simulation.

The QT GUI Waterfall Sink visualizes the waveform's spectrogram over time.

### GNURadio Blocks to be Introduced
* Block 1
* Block 2
* ...



## Flowgraph Creation
The first thing we need to do in order to setup our flowgraph is to create a signal source. The signal source block generates a simulated signal waveform within a GNU Radio flowgraph. It acts as the source of data entering the flowgraph. The next thing we will need to create is the float to complex block, this is responsible for converting the signal from traditional floating point number into a complex exponential. The next part of our flowgraph throttle block the throttle block is responsible only during simulation purposes, when we utilize the throttle block it is not needed. The next part of the flowgraph is the QT GUI Water fall Sink. This is responsible for visualizing the generated waveform in terms of the signal's spectrogram over time. The X-asis is frequency and Y-axsis shows time. 

## References
These are some relevant links for the documentation for GNURadio that might aid in this process. 
GNURadio Tutorials - General tutorials on building flowgraphs in GNU Radio.
https://wiki.gnuradio.org/index.php?title=Tutorials

QT GUI Waterfall Sink - Visualizing signals with the waterfall plot.
https://wiki.gnuradio.org/index.php/QT_GUI_Waterfall_Sink

## Next Chapter