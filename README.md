# The Remote Control of Spark-H Robot

<div align="center">
    <img src="https://github.com/HenryWJL/remote_control_socket/blob/main/image/pc.gif" height=400/><img src="https://github.com/HenryWJL/remote_control_socket/blob/main/image/mobile.gif" height=400/>
</div>

This package is customized for the Spark-H robot with the purpose of using a mobile phone to control the robot. Python socket is used to realize the communication between the mobile phone and the robot's PC.
## Usage
#### (1) Git clone this repository to your workspace.
```bash
cd spark_noetic/src
git clone https://github.com/HenryWJL/remote_control_socket.git
cd ..
catkin_make
source devel/setup.bash
```
#### (2) Start the server.
```bash
roslaunch remote_control_socket server.launch
```
#### (3) Generate a `.apk` file from `client.py` and `data` using buildozer or other tools.
#### (4) Download the app on your mobile phone, and now you can manipulate the Spark-H robot with your phone.
