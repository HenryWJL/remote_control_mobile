# Remote Control of Spark-H Robot

This is the Python implementation of Spark-H robot's remote control. For more details about Spark-H robot, please see [here](https://github.com/NXROBO/spark_noetic).

## Demonstration

<div align="center">
    <img src="https://github.com/HenryWJL/remote_control_socket/blob/main/image/pc.gif"/><img src="https://github.com/HenryWJL/remote_control_socket/blob/main/image/mobile.gif"/>
</div>

## Usage
#### (1) Git clone this repository to your robot's workspace.
```bash
cd spark_noetic/src
git clone https://github.com/HenryWJL/remote_control_socket.git
cd ..
catkin_make
source devel/setup.bash
```
#### (2) Create a `.apk` file from `client.py` and `data` using Buildozer and download the app on your mobile phone.

#### (3) Launch the server on your robot.
```bash
roslaunch remote_control_socket server.launch
```
#### (4) Open the app and get started.
