# Simple GNURadio Flowgraph

## Overview
This is an overview of GNURadio Flowgraph best practices. It will cover flowgraph creation in GNURadio, signal generation and utilizing the QT Gui Sink. It will cover how to use the throttle block for flowgraph creation as it is used for simulation purposes in GNURadio.

### Key Learnings
Mastering flowgraph creation is straightforward once you grasp its essential principles.
Leveraging variables significantly enhances flowgraph manageability and tidiness.
"Float to complex" is a frequently used block in diverse GNURadio flowgraph projects.
The QT GUI library emerges as the top choice for visualization in GNURadio.

Practical Applications

Build adaptable flowgraphs with variable parameters for easy customization.
Incorporate "Float to Complex" blocks to optimize conversion processes in your flowgraphs.
Manage your flowgraphs efficiently with Virtual Source & Sink.
Employ variables for streamlined value management in your flowgraphs.
Use QT GUI Range for on-the-fly adjustments in running flowgraphs.

### GNURadio Blocks to be Introduced

* Float to Complex block
The Float to Complex block in GNU Radio converts a stream of float (real) samples to complex samples by setting the imaginary part to zero.

* Throttle Block
The Throttle block in GNU Radio throttles the data rate of a flowgraph during simulations to avoid overloading the system.

* Signal Source
The Signal Source block in GNU Radio generates a simulated waveform to use as the input source for a flowgraph. It can produce different signal types like sinusoids, noise, analog waveforms, and data from files. The parameters of the signal can be adjusted as needed.

* Qt GUI Waterfall Sink

The Qt GUI Waterfall Sink in GNU Radio displays a spectrogram of the input signal data using a waterfall plot, enabling visualization of the signal in the frequency domain over time.

### FLowgraph Image
![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/GROverview.png)
### Flowgraph Creations
Variables are able to be used within existing GR Blocks.​
Variables allows for easy management of multiple GR values used in different blocks
QT Gui Range enables us to be able predefine ranges and default  values to utilize during a running flowgraph. ​
Showcase that we can utilize QT GUI Blocks to manipulate both filter and frequency values during flowgraph runtime. 

## Video Example
_Coming Soon_

## References
_Coming Soon_


## Next Chapter
_Coming Soon_