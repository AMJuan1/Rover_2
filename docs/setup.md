# Machine setup (Ubuntu)

## 1. ROS 2

Install the ROS 2 distro matching your Ubuntu version (22.04 → Humble, 24.04 → Jazzy) following the official instructions, then:

```bash
echo "source /opt/ros/<distro>/setup.bash" >> ~/.bashrc
source ~/.bashrc
sudo apt install -y python3-colcon-common-extensions python3-rosdep git
sudo rosdep init   # only once per machine
rosdep update
```

## 2. Clone and build

```bash
mkdir -p ~/rover_ws/src && cd ~/rover_ws/src
git clone https://github.com/AMJuan1/Rover_2.git
cd ~/rover_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## 3. Device permissions

```bash
sudo usermod -aG dialout,video,plugdev $USER
# log out and back in
```

## 4. Claude Code

```bash
# install per official docs, then from the repo root:
cd ~/rover_ws/src/Rover_2
claude
```

Claude Code reads `CLAUDE.md` automatically at the repo root.

## 5. Verify

```bash
ros2 doctor
ros2 topic list
```
