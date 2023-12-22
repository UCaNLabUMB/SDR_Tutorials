# RFNoC Tutorial

## Overview

This tutorial will go through the steps to implement the RFNoC framework to offload intensive calculations to a dedicated hardware processor inside a USRP.

### Objective

![FIR RFNoC Flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/hw_FIR_filter.png)

The goal is to familiarize the reader with RFNoC, customization of RFNoC, and usage in GRC. This tutorial will introduce RFNoC, required dependencies for usage, validation, and flowgraph creation.

#### GNURadio Blocks to be introduced

This tutorial will introduce the following blocks from the UHD library:
* RFNoC
    * Blocks
        * RFNoC RX Radio Block
        * RFNoC TX Radio Block
        * RFNoC Fast Fourier Transform Block
        * RFNoC Digital Down Converter Block
        * RFNoC FIR Filter Block
        * RFNoC RX Streamer Block
        * RFNoC TX Streamer Block
    * Device Control
        * RFNoC Graph Block

## Introduction to RFNoC

RFNoC or RF Network on Chip, is a framework used to implement signal processing using FPGA logic and communicate via software. RFNoC is installed automatically alongside the 4.0 version of UHD. It is only compatible with 3rd generation USRPs. To process data, RFNoC utilizes a new block type called ‘RFNoC Blocks’. These blocks allow the user to offload data processing to the FPGA inside the USRP to reduce software data processing. Some of these blocks are pre-built and the user can also include their custom blocks using an out-of-tree library. 

![RFNoC high level](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/rfnoc_sans_flowgraph.png)

RFNoC is located inside a structure called a NoC core, which is generated automatically inside the USRP. The user does not have to worry about generating this core.

## Terminology

This tutorial will introduce different aspects of RFNoC. For better clarification in later steps, this section was included to address any new terminology.

* Field Programmable Gate Array (FPGA): Chip that will host our NoC core and blocks. The size of the FPGA limits the amount of blocks we can include in the image.

* Stream Endpoint (SEP): All RFNoC block connections must begin and end on an SEP. The SEPs allow us to connect blocks together without having to make a static connection inside the FPGA image. If multiple blocks are within one SEP, data cannot be sent or processed without going through all the blocks first.

* RFNoC Blocks: Blocks that are instantiated onto the FPGA. The blocks can be connected statically or dynamically. UHD provides pre-built blocks that can be included in any FPGA image and the user is also able to develop their own blocks for different applications.

* CHDR Crossbar: The crossbar is our dynamic router for any RFNoC traffic. It can be used to configure routes between SEPs and transport adapters. If a block is being used, the crossbar changes the routes at runtime.

* Transport Adapter: An abstraction for physical transports like Ethernet, USB, etc. They are specific to the hardware RFNoC is running on.

## How RFNoC Works

Generation 3 USRPs include an FPGA image that allows the user to interface with the RF hardware. This can be a simple receive or transmit signal. An RFNoC FPGA image interfaces via UHD to our host PC. Inside this image, a NoC core is generated that will host the control crossbar, SEPs, and CHDR crossbar. Each NoC block can communicate with other NoC blocks by sending the data to the CHDR crossbar. When the flowgraph is being generated and sent to the USRP, the NoC core configures any dynamic connection between the blocks. 

![RFNoC diagram](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/rfnoc_diagram.png)

When creating a flowgraph, keep in mind that all static connections must be included as we cannot bypass the physical connections inside the FPGA.

# Getting Started with RFNoC

Before we can use RFNoC we need to install certain dependencies, verify our USRP is RFNoC compatible, customize and build FPGA image, and test the custom image. All the steps in the Customizing RFNoC image section follow the tutorial provided by Ettus Research that can be found in the following link:

[Getting Started with RFNoC in UHD 4.0](https://kb.ettus.com/Getting_Started_with_RFNoC_in_UHD_4.0)

## Dependencies

To get started with RFNoC, the computer you are using must have certain
dependencies installed:

*  GNU Radio

*  GNU Radio Companion

*  UHD 4.6.0 

*  FPGA images

*  A Vivado install (2021.1 version with Kintex-7 license or Enterprise
    trial)
    * Vivado Patch AR76780

Note: The version of UHD that was used while writing this tutorial might be different than the lastest version. In this case, I have included instructions on how to find previous versions of UHD and how to build UHD from source.

### Installing dependencies

In a Ubuntu install, we can use the default package manager to install
GNU Radio. To install UHD, the user can also install from the package
manager. Installation using the package manager will allow the user to interface with the USRP. But for RFNoC customization a UHD built from source is required. This tutorial will also go through the steps to build UHD 4.6.0 from source to have the proper make files for the FPGA images that we will build.

The Vivado version that is required for FPGA image customization is the 2021.1 version with a license for the FPGA or an Enterprise license. Depending on
the USRP model we might need a different application. For the purpose of
this tutorial we will be using Xilinx Vivado. The following image shows
the FPGA of each generation 3 USRP and the required application.

![fpga models](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/usrp_fpga_model.png)

Before installing Vivado, we need to
install additional libraries. Use the following command in the terminal:

'sudo apt-get install libtinfo5'

After installing the additional libraries, we can install Vivado 2021.1.
Going to the Xilinx Vivado website, look for the download page and go to
the Vivado Archive. Find the 2021.1 version and download the unified
installer. To run the installer, run:

'sudo ./"name_of_installer.bin"'

Ignore the version update and install **ONLY** the Kintex-7 files. This will
reduce the install size and speed up the process.

#### Additional Vivado dependencies

To use the Vivado tools a patch needs to be installed for usage with Linux. Follow this link to find the .zip file of the patch. To install it, we need to extract it to a folder named patches inside the Vivado install folder. To do this, I ran the file explorer using super user privileges to write to the root directory. If the patches folder is not there, create it and extract the patch there.  

Verify the Vivado installation by running the following commands in a terminal window: 

'''
Source /tools/Xilinx/Vivado/2021.1/settings64.sh 
vivado 
'''

After successful verification, run the Vivado License Manager to authenticate Vivado. To run the license manager, open Vivado and from the Project Navigator select help -> Manage License. Select the Obtain License tab from the left menu and choose the 30 day trial. This will send you to a Xilinx website and you can follow the instructions to obtain and download the license file for Vivado. Without this license you will be unable to build FPGA images. 

#### Building UHD from source

To get the proper configuration files for the building of FPGA images,
we need to have UHD from source. I recommend that the user make a folder
that will be easily accessible. The same name that I used is not
required, but will make it easier to find inside the terminal. Inside your folder, clone the UHD 4.6.0 repo. 

[UHD 4.6.0 Repo](https://github.com/EttusResearch/uhd/tree/UHD-4.6)

Run:

'git clone https://github.com/EttusResearch/uhd/tree/UHD-4.6'


### Checking USRP image

Before we start customizing our FPGA images, we need to check the image
in the USRP. This will help us identify the model and connection type.
This is important because 3^rd^ generation USRPs have different images
depending on the type of connection you use.

* 1.  Depending on the type of connection (USB or Ethernet) the USRP will use a different communication port. For the X300 USRP, I used Gigabit Ethernet. This means that our image is going to be the 'HG' version.

* 2.  Configure the host Ethernet interface with a static IP from the following table.

### Installing pre-built images

Now that we can interface with the USRP, we check the current image to
see if it has RFNoC blocks installed. To do this, we use the command
'uhd_usrp_probe'. This command outputs a detailed description of everything on the
USRP. Given that the USRP is a 3^rd^ Generation, it is compatible with
RFNoC but the previous command also confirms the compatibility.

![uhd_usrp_probe](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/uhd_usrp_probe_x300.png)

We confirm that it is RFNoC compatible. This command also shows the
RFNoC blocks on the device. The output looks like this.

![default image RFNoC blocks](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/08_RFNoC/default_rfnoc_on_image.png)

This is the default image that I got from 'uhd_images_downloader'. This
image includes 2 DDCs, 2 DUCs, 1 TX, 1 RX, and a replay block. To
include more blocks we need create a custom FPGA image with the blocks
that we want to include.

## Customizing RFNoC image

This part of the tutorial is identical to the provided tutorial from Ettus Research. If there is anything that is not clear, please read through the tutorial.

After building UHD from source, we can build the custom FPGA image. Our working directory is going to be the inside the fpga folder inside the UHD repo built from source (e.g., inside '/<repo>/fpga/usrp3/top/x300').
To add blocks into the image, copy the 'x300_rfnoc_image_core.yml' and name
it something descriptive. This file will be edited to include an FFT block.

'cp x300_rfnoc_image_core.yml x300_with_fft.yml'

I recommend naming it with a description of the blocks added. Avoid
changing the original .yaml file so that all your custom images start
with the default blocks and connections.

The next step is to change the buffer size for some SEPs. We do this to 