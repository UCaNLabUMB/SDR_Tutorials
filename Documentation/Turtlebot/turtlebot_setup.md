# Automated Data Collection Using TurtleBot 

## Overview

This instruction manual will walk through the process of setting up a TurtleBot4 Lite for usage in an indoor positioning SDR based localization algorithm testbed.

### Requirements

There are a few requirements that we need for setting up the TurtleBot4 and interface it with the Robot Operating System (ROS).

* Ubuntu 22.04 LTS
* [ROS 2 Humble](https://docs.ros.org/en/humble/index.html)
* TurtleBot4 Lite (Setup of the Lite and non-lite version is similar)

### Installation

For the setup we will be using a Linux environment. Follow the instructions in the link above to install ROS 2 Galactic. The install tutorial should be followed until the sourcing of the environment. This 'source' command tells the current terminal window which version of ROS to use. 

This is important in case multiple versions of ROS are installed in the same machine.

#### ROS Setup

To install ROS 2 Humble, we can run the following command in a terminal window:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

This ensures we have access to the Ubuntu Universe Repository and that we add the ROS repository to the system.

```bash
sudo apt update && sudo apt upgrade
sudo apt install ros-humble-desktop
```

This will update the repositories, upgrade them, and install ROS.

#### Setup of the work environment

We can source our setup file at shell startup by using the following command inside the terminal:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```
This command will allow a shell terminal to always use ROS 2 Galactic.

## Raspberry Pi 4 Troubleshooting

In case the access point of the Raspberry Pi does not appear in the available Wi-Fi networks, connect to it via Ethernet by removing the tray and connecting a cable to the Ethernet port of the Raspberry Pi.

Setup your Ethernet port to manual and to the following IP address: ```192.168.185.5```. Use the following command to establish a connection with the Raspberry Pi:

```bash
ssh ubuntu@192.168.185.3
```

If for some reason you still cannot connect to the Raspberry Pi, please remove the TurtleBot4 from the charging dock and press the power button until both the TurtleBot4 and Raspberry Pi are shutdown.

Once they are both off, remove the SD card inside the Raspberry Pi and insert it into your computer. Install the imaging tool ```dcfldd``` by using ```sudo apt install dcfldd``` in your terminal. Identify the SD card by running ```sudo fdisk -l```. This should show a disk ```/dev/mmcblk0```. This ```mmcblk0``` is the device we will be formatting and writing the new firmware onto.

Follow this link to obtain the latest TurtleBot 4 image. [Raspberry Pi 4 TurtleBot Images](http://download.ros.org/downloads/turtlebot4/) We select the latest Lite Humble version and download it. Extract the .zip file and this is the image we will be using. Keep in mind the location of the file as it will be needed later.

Run the following command to download the flash script:

```bash
wget https://raw.githubusercontent.com/turtlebot/turtlebot4_setup/humble/scripts/sd_flash.sh
bash sd_flash.sh /path/to/downloaded/image
```

Now we use the name of the device we are formatting, in this case it's the ```mmcblk0``` device.

Wait and your SD card is flashed. Now you can remove it and insert it onto the Raspberry Pi. Power the TurtleBot 4 by placing it back onto the dock. Wait some time and you should see the TurtleBot 4 access point show up. Connect to it and continue the setup.

* Note: Raspberry Pi IP address in UCanLab5Ghz is 192.168.1.21

## Discovery Server versus Simple Discovery

There are two ways of setting up the Raspberry Pi 4 and Create 3 to interface with the user computer, simple discovery and discovery server. They each have advantages and disadvantages. For this tutorial we are using the discovery server because with this setup only the Raspberry Pi 4 is connected to the Wi-Fi network. Simple discovery needs both the Raspberry Pi 4 and Create 3 are connected to the same Wi-Fi network. 

In this configuration, the Raspberry Pi 4 acts as the server, while the user PC and Create 3 are the clients of this server. We chose this as our network configuration does not need to have both 2.4 GHz and 5 GHz bands.

## Discovery Server Setup

We need to setup the Create 3 to use the Raspberry Pi as the discovery server and the RMW implementation to use Fast DDS. To access the Create 3 setup website, open a web browser and insert your Raspberry Pi 4 IP address with port 8080.

![create3_server](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Turtlebot/create3_server.png)

To finish setting up the Discovery Server, the TurtleBot 4 manual has the instructions for the Raspberry Pi 4, Create 3, and User PC. 

The changes to the Create 3 can be done via the webserver. Additional Raspberry Pi setup needs an SSH connection into the Raspberry Pi. 

After all the configuration is done, test in your computer with the following command on a new terminal:

```bash
ros2 topic list
```

This command should list all the topics your computer is now subscribed to. The output should look like this:

![Local topic](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Turtlebot/local_pc_topic.png)

We can see that the topics match between the Raspberry Pi and the host computer. This shows succesful setup of the Discovery Server.

![Dual topic list](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Turtlebot/pc_raspberry_topic.png)


# References

| Number | Reference 
| --- | --- | 
| 1. | [*Robot Operating System 2*](https://docs.ros.org/en/humble/index.html)
| 2. | [*TurtleBot 4 User Manual*](https://turtlebot.github.io/turtlebot4-user-manual)

