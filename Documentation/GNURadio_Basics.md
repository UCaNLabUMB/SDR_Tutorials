# Simple GNURadio TX/RX

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

* Trottle Block


* Signal Source

* Qt GUI Waterfall Sink


### Flowgraph Creations
Variables are able to be used within existing GR Blocks.​
Variables allows for easy management of multiple GR values used in different blocks
QT Gui Range enables us to be able predefine ranges and default  values to utilize during a running flowgraph. ​
Showcase that we can utilize QT GUI Blocks to manipulate both filter and frequency values during flowgraph runtime. 

## Video Example

## References



## Next Chapter