# SDR_Tutorials
This tutorial series introduces concepts related to software defined radio (**SDR**) and the **GNURadio** software toolkit for signal processing. 

## Overview
In this repository, you will find tutorial documents and a set of example **flowgraphs** to introduce the GNURadio software toolkit. The tutorial documentation, and the associated tutorial videos, are intended to familiarize the reader with GNURadio tools and workflows while simultaneously reviewing some fundamental concepts related to basic signal analysis. The complementary GNURadio Companion (**GRC**) files and relevant Python code are included in order to work through the tutorial exactly as described; however, it is strongly suggested that you first follow the tutorial discussion and attempt to build the flowgraphs on your own. This will be beneficial to your understanding of the tools available within GNURadio and GRC. 

Within the set tutorials, we will introduce:
* Basic flowgraph creation,
* The GNURadio Companion (GRC) tool,
* The **QT GUI** library for creation of a graphical user interface and manual configuration of flowgraph parameters,
* GNURadio tools for interacting with universal software radio peripheral (**USRP**) SDR hardware,
* Basic communication tools for over-the-air (**OTA**) data transmission, and 
* GNURadio tools that allow flowgraphs to be read from and controlled remotely (i.e., **XMLRPC** and **ZMQ**)

Ultimately, the tutorial will work towards the creation of an automated data collection system for evaluation of a point-to-point wireless communication link based on orthogonal frequency division multiplexing (**OFDM**).


## Directory Structure
This repository is structured as follows:
* The `Documentation` folder includes the tutorial descriptions and discussion 
* The `Flowgraphs` folder contains completed flowgraphs for each of the tutorials

## Chapters
| Chapter | Topic | Image | Summary 
| --- | --- | --- | --- |
|  1  | [GNURadio Overview](Documentation/GNURadio_Overview.md)               | (_Add Image_) | Introduction to Flowgraphs, source/sink blocks, and data types
|  2  | [GNURadio Basics](Documentation/GNURadio_Basics.md)                   | (_Add Image_) | Introduce flowgraph best practices, variables, and dynamic control
|  3  | [SDR Hardware](Documentation/SDR_Hardware.md)                         | (_Add Image_) | Introduce USRPs, hardware addressing, and over-the-air waveform transmission
|  4  | [GNURadio Remote Command and Control](Documentation/GNURadio_CaC.md)  | (_Add Image_) | Introduce multi-node systems with XMLRPC and ZMQ
|  5  | [Basic Communicatons](Documentation/GNURadio_Comms.md)                | (_Add Image_) | Introduce simulation and over-the-air data transmission
|  6  | [Automated Data Collection](Documentation/GNURadio_Automation.md)     | (_Add Image_) | Combine XMLRPC, ZMQ, and OFDM to automate Packet Error Rate Testing
