Implementing RFNoC on X310 USRP

To get started with RFNoC, the computer you are using must have certain
dependencies installed:

-   GNU Radio

-   GNU Radio Companion

-   UHD 4.6.0 (As of the 4.0 version, RFNoC is automatically installed
    but does not have the required images.)

-   FPGA images

-   A Vivado install (2021.1 version with Kintex-7 license or Enterprise
    trial)

    Installing dependencies

In a Ubuntu install, we can use the default package manager to install
GNU Radio. To install UHD, the user can also install from the package
manager. I will also go through the steps to build UHD 4.6.0 from source
to have the proper make files for the FPGA images that we will build.

The Vivado version that I am using is the 2021.1 version. Depending on
the USRP model we might need a different application. For the purpose of
this tutorial we will be using Xilinx Vivado. The following image shows
the FPGA of each generation 3 USRP. Before installing Vivado, we need to
install additional libraries. Use the following command in the terminal:
sudo apt-get install libtinfo5.

After installing the additional libraries, we can install Vivado 2021.1.
Going to the Xilinx Vivado website, look for the download page and go to
the Vivado Archive. Find the 2021.1 version and download the unified
installer. To run the installer, run: sudo ./"name_of_installer.bin".
Ignore the version update and install ONLY the Kintex-7 files. This will
reduce the install size and speed up the process.

Building UHD from source

To get the proper configuration files for the building of FPGA images,
we need to have UHD from source. I recommend that the user make a folder
that will be easily accessible. The same name that I used is not
required, but will make it easier to find inside the terminal. (Insert
image from file explorer of the folder)

Make sure to remember where you created the folder. Inside the folder,
clone the UHD repository from GitHub. If Git is not installed, install
Git. (Insert steps of building UHD from source).

Checking USRP image

Before we start customizing our FPGA images, we need to check the image
in the USRP. This will help us identify the model and connection type.
This is important because 3^rd^ generation USRPs have different images
depending on the type of connection you use.

1.  Depending on the type of connection (USB or Ethernet) the USRP will
    use a different communication port. For the X300 USRP, I used
    Gigabit Ethernet. This means that our image is going to be the 'HG'
    version.

2.  Configure the host Ethernet interface with a static IP from the
    following table.

    Installing pre-built images

Now that we can interface with the USRP, we check the current image to
see if it has RFNoC blocks installed. To do this, we use the command
'uhd_usrp_probe'. This command outputs a detail of everything on the
USRP. Given that the USRP is a 3^rd^ Generation, it is compatible with
RFNoC but the previous command also confirms the compatibility.

We confirm that it is RFNoC compatible. This command also shows the
RFNoC blocks on the device. The output looks like this.

This is the default image that I got from 'uhd_images_downloader'. This
image includes 2 DDCs, 2 DUCs, 1 TX, 1 RX, and a replay block. To
include more blocks we need create a custom FPGA image with the blocks
that we want to include.

Customizing RFNoC image

After building UHD from source, we can build the custom FPGA image. To
add blocks into the image, copy the 'x300_rfnoc_image_core.yml' and name
it. I recommend naming it with a description of the blocks added. Avoid
changing the original .yaml file so that all your custom images start
with the default blocks and connections.