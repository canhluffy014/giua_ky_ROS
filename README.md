Project giữa kỳ ROS:
Mecanum 4 bánh:
video điều khiển:
https://youtu.be/bkMwmFSSujk

-Gồm 2 package: meca và mecanum_steering_control
+ meca chưa file xacro,urdf,mesh
+ mecanum_steering_control diều khiển

- Chạy dòng lệnh dưới đây để chạy file launch khởi tạo Gazebo,Rviz và code điều khiển :

roslaunch mecanum_steering_control main.launch

- Điều khiển như sau

| Q  | W  | E  |    | U  | I  |
|----|----|----|----|----|----|
| A  | S  | D  |    | J  | K  |
|    | X  |    |    |    |    |

W: Tiến | X: Lùi | Q: Quay trái | E: Quay phải

A: Sang trái | D: Sang phải

U: Tăng arm1 | I: Giảm arm1 | J: Tăng arm2 | K: Giảm arm2

S: Dừng

