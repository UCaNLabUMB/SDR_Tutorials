# GNURadio Command and Control

## Overview
In this tutorial we are going to cover more advanced GNURadio flowgraphs and topics. We will cover how to setup a command and control flowgraph. By the end of this tutorial you should be able utilize the XML-RPC Module for command and control  along with the ZMQ module which provides a feedback mechanism. In addition we will also cover the hardware setup in terms of network on how to get distributed nodes up and running and in addition, networking wiring for multiple flowgraph control.

### Key Learnings
_Coming Soon_

### GNURadio Blocks to be Introduced
* XML_RPC Server Block
* ZMQ Pub Sink
* ...



## Hardware Setup
For the networking setup both XML-RPC and ZMQ utilize server for the communication messaging. If you have multiple computer, with different flowgraphs operating, you would want to utilize a ethernet switch along with proper cabling in order to ensure that all computers can talk to each other. 
After this a good thing to do is to perform a ping test to see if you ca communicate with the other ip addresses for the respective flowgraph. 

## XMLRPC
XMLRPC is a standard python module that is also utilize within GNURadio. In a simple way XMLRPC basically exposes the Flowgraph Variables by once you put the block inside the flowgraph. You can specify the ip address along with the port number. This is how you communicate with the variables. The key two things that you can do with XML RPC is to update the parameters in a GNURadio flowgraph and in addition you can utilize it to get the current value in a GNURadio variable. This ability become very powerfull once you utilize the variables in the GNURadio flowgraph blocks. For example lets say you have a flowgraph running and we have a variable amplitude in our signal generation block. With xml_rpc we can push a new value update to the amplitude during flowgraph operation, once the variable parameters updates the value used in the signal generation also updates. This allows us to controll and paramets we want for any GNURadio block. Its very simple how it all works, we predefine the function name syntax corrent with the variable in the flowgraph, and pass the command the the XML Server block ip and port number. The flowgraph will recieve the command and update the parameter respecfully.  In addition another benefit of XML_RPC is that its batch scriptable. For example if you have a setting of different parameter configuration's you wanted to test in your flowgraph you would utilize  batch scripting to send updated parameters to the flowgraph in bulk. This is particularly usefull for data collection purposes. For example testing different parameters for your antenea connected to your usrp, or even optical systems. 

## ZMQ

## Combined Example - AGC


## References

## Next Chapter