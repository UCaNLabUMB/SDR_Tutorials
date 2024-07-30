# GNURadio Command and Control

## Overview
In this section, we will discuss how we can interact with GNURadio flowgraphs from external programs (or remotely over a network connection). We will cover how to setup a command and control flowgraph that allows for remote configuration of flowgraph parameters and remote access to measurements within the flowgraph. By the end of this tutorial you should be able utilize the XML-RPC remote parameter control functionality along with the zeroMQ (i.e., ZMQ) functionality to remotely access flowgraph data. We will also cover the physical network configuration to connect to multiple distributed nodes from a central controller.

**Tutorial Video:** _Coming Soon_

### Objective

![Flowgraph Image](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/04_CaC/GR_CaC_03.png)

In this tutorial, we will work with GNURadio's xmlrpc and ZMQ tools to build the flowgraphs shown above, along with the corresponding control script, and implement a centrally controlled automatic gain controller that adjusts Tx gain in order to keep the Rx signal power within a desired range.

As key learnings, we will cover
* GNURadio's built-in tools for remote control (xmlrpc) and access (ZMQ),
* Python script generation to remotely configure flowgraph parameters,
* Python script generation to automate a sequence of configurations,
* Python script generation to define configurations remotely via the command line,
* Client/Server interactions in a publish/subscribe model for remotely accessing flowgraph measurements,
* Streaming signals across GNURadio flowgraphs for distributed processing,
* Python scripts for creating automated control loops with feedback from ZMQ and parameter configuration with xmlrpc,
* Fundamental networking topics related to IP addresses and static network configurations


### GNURadio Blocks to be Introduced
* XMLRPC Server Block
* ZMQ PUB Sink Block
* Complex to Mag^2 Block
* Moving Average Block
* QT GUI Number Sink Block

# Remote Parameter Control via XMLRPC
The XML_RPC Server block in GNU Radio allows external applications to communicate with and control a running GNU Radio flowgraph over the network using XML RPC requests.

Some key functions of the XML_RPC Server block:

Exposes methods that can be called remotely to get/set flowgraph parameters, variables, and block values.
Enables building custom controllers and dashboards to control GNU Radio remotely.
Allows parameter tweaking, flowgraph control without directly modifying the code.
Provides information like performance metrics to remote clients.
Handles concurrent XML RPC requests from multiple clients.
Useful for connecting GNU Radio to higher level applications and controlling it programmatically.
In summary, it enables remote procedure call-based integration of GNU Radio with external programs and systems over a network.

# Remote Access to Flowgraph Data via Zero MQ (ZMQ)

The ZMQ Pub Sink block in GNU Radio publishes stream data from a flowgraph to connected subscribers over a ZeroMQ PUB/SUB socket.

Some key functions:

Enables real-time data streaming from GNU Radio to other applications.
Implements the publish-subscribe pattern for data distribution.
Subscribers can filter data by topic without affecting the publisher.
Handles PUB/SUB socket creation, binding, connections in the background.
Efficient for high speed real-time data transfer.
Useful for connecting GNU Radio to data collection systems, machine learning pipelines, visualization tools etc.
Data is published as PDUs (protocol data units) over TCP or IPC transports.
In summary, it allows other programs to subscribe to real-time data streams from a GNU Radio flowgraph over efficient ZeroMQ connections. Enables interfacing with external data processing systems.






# Remote Command and Control

## Hardware Setup
For the networking setup both XML-RPC and ZMQ utilize server for the communication messaging. If you have multiple computer, with different flowgraphs operating, you would want to utilize a ethernet switch along with proper cabling in order to ensure that all computers can talk to each other. 
After this a good thing to do is to perform a ping test to see if you can communicate with the other ip addresses for the respective flowgraph. 

## XMLRPC
XMLRPC is a standard python module that is also utilize within GNURadio. In a simple way XMLRPC basically exposes the Flowgraph Variables by once you put the block inside the flowgraph. You can specify the ip address along with the port number. This is how you communicate with the variables. The key two things that you can do with XML RPC is to update the parameters in a GNURadio flowgraph and in addition you can utilize it to get the current value in a GNURadio variable. This ability become very powerfull once you utilize the variables in the GNURadio flowgraph blocks. For example lets say you have a flowgraph running and we have a variable amplitude in our signal generation block. With xml_rpc we can push a new value update to the amplitude during flowgraph operation, once the variable parameters updates the value used in the signal generation also updates. This allows us to controll and paramets we want for any GNURadio block. Its very simple how it all works, we predefine the function name syntax corrent with the variable in the flowgraph, and pass the command the the XML Server block ip and port number. The flowgraph will recieve the command and update the parameter respecfully.  In addition another benefit of XML_RPC is that its batch scriptable. For example if you have a setting of different parameter configuration's you wanted to test in your flowgraph you would utilize  batch scripting to send updated parameters to the flowgraph in bulk. This is particularly usefull for data collection purposes. For example testing different parameters for your antenea connected to your usrp, or even optical systems. 

## ZMQ
ZMQ is part of the standard python libary. Our usable will only involve the ZMQ PUB Sink however there are more features and its flexible in its usage in a GNURadio flowgraph. For more information contact th GNURadio Wiki, for further explaination. 


## Combined Example - AGC FlowGraph & Code
In this example we will be utilizing both XML_RPC and ZMQ in order to build an automatic gain controller in GNURadio. XML_RPC will be responsible for dispatching command to the respective server while ZMQ will be responsible for retriving the relevant information that would tie into the decision making for the amplitude controll.
In terms of the flowgraph setup we will be utilizing 2x USRP B200 mini for this example. In our flowgrpah we start of with a signal source and a constant source both which flow into a FLoat to Complex block. From here we connect the output from this block into our USRP Sink block. This block should have the serial address of the connected USRP for this to work, as we learned from the previous tutorial. Next we add our USRP Source block again with its own respective serial address. We can then add the QT GUI sink for visualization.

Next in order to set up to measure the RX power, we add in a RMS block with alpha 100u, we connect this to a decimating Fir filter with deicmation at 1k and Taps: 1. We then hook it up to our QT Time sink for visualization, as in the flowgraph we would want to visualize this. Next we will add the command and control aspect to this flowgraph. We will add the ZMQ Pub Sink connected to the FIR Filter. We can then initialize the address to a local tcp address, since we are working on the same computer environment as the flowgraph, for the code we will utilize for command and control. Another key step is to add the XMLRPC Server block with the address initilized to localhost. Another key aspect is to a variable called amplitude with your chosen defualt value, here we use 250m, and place the variable name inside the lot in the singal source where it says amplitude. Afer this flowgraph aspect is done. 

## Code For flowgrpah Explanation.
How doest the code to connect everything work?
Setting Up Connections: It connects to multiple servers via XML-RPC and a ZMQ Subscriber socket. The XML-RPC servers are used to retrieve and set the 'amplitude' value, while the ZMQ connection is used to receive data, presumably from some type of data producer or sensor.

Setting Up Function to Adjust Amplitude: A function (set_amplitude) is defined to set the amplitude on the XML-RPC server, which is used later in the control loop.

Control Loop:

The initial 'amplitude' is obtained from one of the servers and displayed.
Then, a continuous loop is started, which runs once every second.
In each iteration of the loop, it checks if there's any new data available from the ZMQ socket, retrieves the latest data if available.
This data is converted to a numpy array and the average value (avg_power) is calculated.
It then compares avg_power with a predefined target power value (the midpoint of an upper and lower bound). If avg_power is within a certain tolerance level of the target, no action is taken and the loop continues.
If avg_power is outside the tolerance level, an error value is calculated based on how far avg_power is from the target. The error is limited to a range of -1 to 1.
This error is then used to calculate an adjustment to the amplitude. The amplitude is adjusted by a maximum of 15% of its current value (this value is adjustable in the code).
This new 'amplitude' value is then set on the server and the loop continues, now using this new amplitude for further calculations.

With this the feedback system with our python code together with the flowgraph, we have created an automatic gain controller.




## References

## Tutorial Chapters

* **Next Chapter:** [Basic Communicatons](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Comms.md) 
* **Previous Chapter:** [SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md)

| Chapter | Topic | Summary 
| --- | --- | --- |
|  1  | [GNURadio Overview](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Overview.md)                   | Introduction to Flowgraphs, source/sink blocks, and data types
|  2  | [GNURadio Basics](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Basics.md)                       | Introduce flowgraph best practices, variables, and dynamic control
|  3  | [SDR Hardware](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/SDR_Hardware.md)                             | Introduce USRPs, hardware addressing, and over-the-air waveform transmission
|  4  | GNURadio Remote Command and Control                                                                                             | Introduce multi-node systems with XMLRPC and ZMQ
|  5  | [Basic Communicatons](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Comms.md)                    | Introduce simulation and over-the-air data transmission
|  6  | [Automated Data Collection](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/GNURadio_Automation.md)         | Combine XMLRPC, ZMQ, and OFDM to automate Packet Error Rate Testing

