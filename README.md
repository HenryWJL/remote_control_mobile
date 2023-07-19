# Remote Control of Spark-H Robot
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
#### (3) Generate a `.apk` file from `client.py` using buildozer or other tools.
#### (4) Download the app on your mobile phone, and now you can manipulate the Spark-H robot.
