# Indoor postioning

## Overview
In this tutorial, we will use SDR to find the location of an object within a defined area in a stimulated environment then compare the results in practical settings. We will use the beacon-based locations method to find the approximate location of a point of interest. In this method, there will be four beacons/anchors set up as limit of the defined area. These anchors are signal transmitters which transmit 4 different signal frequencies. The point of interest/tag represents the location we are determining, and it is a signal receiver. The tag should have a bandwidth in which to cover all four signal frequencies from four beacons. As the tag approaches close to any beacon, the magnitude of that beacon’s frequency should increase and will be the peak in the observation. Based on where is the peak observed, we can approximate locates where is the tag in the designated area.

## Creating a stimulated multi-node environment
To stimulate the model, we will use GNU Radio to set up a virtual defined area with two coordinates, X and Y.

Four anchors will be at a stationary position with fixed coordinates while the tag coordinates can be changed so we can observe the difference in stimulation and compare with real life situations when we move the tag around the room.

First, add variable blocks and define our anchor locations on the XY plane as shown below. Repeat for the other 3 anchor locations.

![anchor](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_anchor.png)

Next, we define our tag coordinates. We need the beacon coordinates moveable. Add two QT GUI range blocks and define the limit of the tag coordinates.

![ref_point](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_ref_point.png)

When the area is defined, to observe how the environment we made looks like, we use QT GUI Constellation Sink. 

We have two coordinates for each point in our environment. We can combine the coordinates by passing point’s coordinates into a Float to Complex block. Complex coordinates have similar properties as XY plane coordinates, so we can use this block to represent beacons and tag locations.

* **NOTE:** Our coordinates are a constant, which is in GNU Radio is defined as float data type. 

![float_to_complex](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_float_to_complex.png)

Repeat the process for all other points.

When we have all locations set up, pass all coordinates through throttle block and then to QT GUI Constellation Sink.

![constellation_sink](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_constellationsink.png)

Run the flowgraph, you will see a plane with the beacon is in your defined area, and you can move the beacon in that area when you change its coordinates.

* **NOTE:** you can change color/style/marker and name of any point in the QT GUI Constellation Sink configuration tab. Do it from the beginning to reduce confusion as we progress through this tutorial.

![constellation_graph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_constellationgraph.png)

To reduce crowded looking flowgraph, you can creat a hierarchy flowgraph as follow.
Choose all the block in the middle from a point coordinate until throttle block, right click, more, create Hier.

A window will pop up with blocks that you chose from earlier. Run and save the flowgraph.

* **NOTE:** need to save the hierarchy flowgraph to use in your stimulation. Name it properly.

Come back to your main flowgrap, refresh the library with reload blocks button, then find your hier block.

More information about Hierarchy block can be found here [https://wiki.gnuradio.org/index.php/Hier_Blocks_and_Parameters] (Hier_Blocks_and_Parameters)

Your observation section should look like this after hier block is created. 

![constellation_with_hier](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_constellationwithhier.png)

Run the flowgraph, the result should be the same as previously described. By doing Hierarchy method, it reduces crowded blocks as your flowgraph might get more complex.

This is the point coordinator flowgraph hier. It performs the same as what we built prior to this hier creation.

![point_coordinate_hier](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_point_coordinate_hier.png)

## Implementing Beacon-based positioning in stimulation

From the pre-set environment, we now can start implementing beacon-based positioning.
First, to determine where the tag is located relative to all four anchors, we compare the distance from the tag to each anchor. The smallest distance implies the tag is probably in the quadrant close to that specific anchor. It means that we need to calculate the distance from the tag to all anchors and compare.  

### Distance calculation

To calculate distance between two points, we simply apply Pythagorean theorem. Given point A(x_1,y_1 ) and B(x_2,y_2)

![distanceformula](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distanceformular.png)

In GNU Radio, there are many ways to calculate distance between points. In this specific tutorial, we will inspect two methods: data streaming method and variable method. Both ways will show the same results but are different in the creating process. One way is faster than another.

### Data streaming method

![data_steam_flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_stream_flowgraph.png)

Data streaming method is when you send a variable through different blocks in sequence to perform a calculation. In this case, we are calculating distance between two points.
From distance formular, we need to perform 3 calculations to get the distance between two distinct points.
First, we find the difference between x coordinates and y coordinates between two points. We can do it by using a constant source.

![constantx](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_constant_source_x.png)

![constanty](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_constant_source_y.png)

Next, square the results. We can do this by using Complex to Mag^2 block. This block takes complex data input, calculates the magnitude of the input and gives result in float data type.

![complex_to_mag](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_complex_to_mag.png)

Then, we add the results together by an add block
Finally, we take the square root of the result by using Transcendental block. 

![sqrt](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_transcendental_sqrt.png)

![sqrt_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_transcendental_prop.png)

The result as well as any other calculation in the sequence will be put into a sink and stored there for later use. In our stimulation, we need to store the distance as well as the distance square. The distance calculation section will look like this for one point. Repeat the process with other points.

![distance_steam](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_stream.png)

* **HIER:** Create a hier for distance square calculation to make flowgraph look better as follow.

![devide_dsq_stream](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_devide_dsq_stream.png)

After tidying up the flowgraph, it should look like this

![data_stream_flowgraph_with_hier](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_stream_flowgraph_with_hier.png)

#### Signal observation

For simplified calculation purposes, we will divide our signals magnitude by the calculated distance square between reference point to other stationary points. 
We previously spontaneously stream distance square data while calculating distance. From that result, we just need to change it from float to complex data type. It is because the signal is in complex type, so we need to synchronize the data. Then, use divide block to obtain the result and put it to a virtual sink. Repeat the process with all other points. 

![distancesq](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distancesq_stream.png)

With all the flowgraphs component set up, put all of them into a QT GUI sink with noise to observe the the peaks

![QTGUI](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_qtguisink_stream.png)

* **NOTE:** create another hier for this observation as previously discussed to reduce the "complexity" of the flowgraph and to look like shown flowgraph as the beginning.

The result is presented below. By default, the reference point is at the center, in which case the distance to all points is equal. As we can see, all four peaks are at the same rate as shown. If we change the coordinate of the reference point, there will be a change in peaks, which we will use to determine where the reference point is closer to. 

![peakobservation](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_peak_stream.png)

### Variable block method

![variable_flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_variable_flowgraph_with_hier.png)

In this method, we are not required to use multiple blocks to calculate distance as in the previous method. We simply need a variable block to perform such mentioned calculations.
We need to import math modules from python into GNU Radio, even though GNU Radio is a python-based environment. To do so, we use import block.

![import_good](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_import_good.png)

* **NOTE:** When trying to use import block, if you see the block becomes error as below, check the properties of the block. To properly use the import block, in the properties tab, type “import (library module)” to fix the problem. 

![import_no](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_import_no_good.png)

![import_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_import_prop.png)

Math module is enough for the purpose of this stimulation. Import more modules if needed. To use math operation in the module, use python syntax for the operation to apply in the calculation. 

We will use 2 variable blocks to calculate distance from reference point to a stationary point and that distance square value as similar scenario in data streaming method. 

Calulating distance
![distance_var](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_variable_block.png)

![distance_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_variable_prop.png)

Calculating distance square

![distancesq_var](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_variablesq_block.png)

![distancesq_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_distance_variablesq_prop.png)

#### Signal obsevation 

We previously calculated distance square for all possible points in the stimulation. We can calculate the discussed method by dividing the signal as data stream method. However, we have another block which does the same calculation but requires less connections in the flowgraph. We use multiply const block.

![multiply_const_variable](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_multiply_const_variable.png)

Here is the calculation for Multiply const block

![multiply_const_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_multiply_const_variable_prop.png)

The frequency display by using this method is like what we saw in the data streaming method.

![peak_variable](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_peak_variable.png)

### Comparision between two methods

As we can see, by using two different methods, we receive the same result in the signal observation from the beacon. However, the process of making the flowgraph by using variable block is faster than the data streaming method. Also, the complexity of the flowgraph is less crowded in variable method. We just need to be cautious when performing the calculations.

### Free Space Path Loss (FSPL)

![FSPL_flowgraph](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_FSPL_flowgraph.png)

In practical settings, there is another factor that effect our calculations in beside distance, it is free space path loss. We need to include this in our stimulation model to estimate as close as possible to real world tests. This is what we mimic in previous examples by dividing our signal by distance square. 

Free space path loss is the attenuation of radio energy between antennas, which includes receiving antenna’s capability range plus the obstacle-free path through free space.

It means that, in practical situations when we work with signal, there is a loss of signal power between two ends of the transmitting process. There are many factors that affect the loss, and we can calculate it through the equation below.

![FSPLformular](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_FSPLformular.png)

* **NOTE:** 
* d: distance between two points
* f: signal frequency
* c: speed of light
* G_p: power gain 

One of the components is distance, which we just calculated with two different methods. We define signal frequency from the beginning. With all the information provided, we can calculate the path loss from reference point to other points.

* **NOTE:** we will use variable block to calculate this because it reduces the complexity of the flowgraph.

The provided equation is the power calculation. However, in our stimulation, we have amplitude of the signal is in voltage. It means that we must convert the calculation from power to voltage. Equation manipulation is shown below.

![FSPLmanipulate](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_FSPLmanipulate.png)

* **NOTE:** G_v: Voltage gain

Voltage gain is what we are looking for in this stimulation and is what we will replace with the distance square in the previous example to complete the stimulation. 
First, we need to create some variable blocks to assist us in the calculation. From FSPL formular, we need to define the value of pi and speed of light. 

Import math module. Pi is define in this libraby. In a variable block, define its value.

![pi](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_pi.png)

For speed of light, create another variable block and define its value. 

![lightspeed](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_light_speed.png)

Create four variable to define your signal frequencies from four beacons to complete varriable set-up

From the FSPL equation, we first calculate the power gain. In a variable block, insert the calculation with all variable. 

![GP](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GP.png)

![GP_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GP_prop.png)

Next, in another variable block, convert the power gain into dB.

![GP_dB](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GP_dB.png)

![GP_dB_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GP_dB_prop.png)

Finally, in another variable block, calculate the voltage gain.

![GV](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GV.png)

![GV_prop](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_GV_prop.png)

* **HIER:** FSPL Hier

![FSPL_hier](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_FSPL_hier.png)

#### Signal observation

The result is presented below. As you can see, we don't have four equal peaks anymore even though our tag is in the center of the area. It is because we have four different frequencies which is a factor in our calculations. The larger the frequency, the higher the peak.

However, if we move the tag around, we still receive similar results with previous examples. Adding FSPL in our calculation is a closer approach to practical testing we will perform later. 

![FSPL_peak](https://github.com/UCaNLabUMB/SDR_Tutorials/blob/main/Documentation/Images/07_IndoorPostioning/GR_position_FSPL_peak.png)

## Applying USRPs for experimental testing

COMING SOON