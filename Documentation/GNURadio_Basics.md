
# Simple GNURadio TX/RX
## Overview
This is the overview of an simple introdcution to GNURadio. In this section we will build a simple Signal Transmission and Receiving flowgraph within GNURadio.
The video will demonstrate the flowgraph creation from start to finish ending with a Flowgraph run.

### Key Learnings
GNURadio is a versatile toolkit for constructing and operating signal processing systems.
Signal Transmission and Receiving flowgraphs can be easily created in GNURadio.
These flowgraphs feature a signal source block that produces simulated signal waveforms.
The "Float to Complex" block is crucial for converting signal forms from floating point to complex exponential.
The throttle block effectively manages data flow throughout simulation.
The QT GUI Waterfall Sink enables real-time visualization of a waveform's spectrogram.

Practical Applications
Use GNURadio to construct comprehensive and functional signal processing systems.
Develop Signal Transmission and Receiving flowgraphs in GNURadio for diverse communication needs.
Leverage the signal source block for generating custom simulated signal waveforms.
Implement the "Float to Complex" block to transition signal data from floating point format to complex exponential format.
Control the pace and volume of data flow during simulation with the throttle block.
Employ QT GUI Waterfall Sink for real-time spectrogram visualization, aiding in signal analysis and troubleshooting.

### GNURadio Blocks to be Introduced

* Band Pass Filter

The Band Pass Filter block in GNU Radio applies a bandpass filter to the input signal, passing frequencies within a specified range while rejecting frequencies outside that range. It is used to isolate or filter out certain frequency components of a signal

* Virtual Sink

The Virtual Sink block in GNU Radio acts as a dummy sink that discards samples instead of doing any real processing or output. It is useful for flowgraph optimization by avoiding unnecessary processing blocks. The Virtual Sink allows samples to be thrown away earlier in the flowgraph.

* Virtual Source 
The Virtual Source block in GNU Radio acts as a dummy source that generates a stream of zero samples or a give signal generation. It is primarily used for flowgraph optimization purposes. When connected to a Virtual Sink, it allows building conceptual flowgraphs without unnecessary real data streams. The Virtual Source and Sink avoid wasted CPU cycles and memory when actual data transfer is not needed



### FLowgraph Image
![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Images/GNU_Basics.png)


## Flowgraph Creation
The first thing we need to do in order to setup our flowgraph is to create a signal source. The signal source block generates a simulated signal waveform within a GNU Radio flowgraph. It acts as the source of data entering the flowgraph. The next thing we will need to create is the float to complex block, this is responsible for converting the signal from traditional floating point number into a complex exponential. The next part of our flowgraph throttle block the throttle block is responsible only during simulation purposes, when we utilize the throttle block it is not needed. The next part of the flowgraph is the QT GUI Water fall Sink. This is responsible for visualizing the generated waveform in terms of the signal's spectrogram over time. The X-asis is frequency and Y-axsis shows time. 

## References
These are some relevant links for the documentation for GNURadio that might aid in this process. 
GNURadio Tutorials - General tutorials on building flowgraphs in GNU Radio.
https://wiki.gnuradio.org/index.php?title=Tutorials

QT GUI Waterfall Sink - Visualizing signals with the waterfall plot.
https://wiki.gnuradio.org/index.php/QT_GUI_Waterfall_Sink

## Next Chapter
_Coming Soon_