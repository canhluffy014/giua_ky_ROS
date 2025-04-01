#!/usr/bin/env python3

import rospy
import sys
import termios
import tty
from std_msgs.msg import Float64MultiArray, Float64
from geometry_msgs.msg import Twist

class TeleopMecanumArm:
    def __init__(self):
        rospy.init_node("teleop_mecanum_arm", anonymous=True)

        self.wheel_pub = rospy.Publisher("/meca/mecanum_drive_controller/command", Float64MultiArray, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.arm1_pub = rospy.Publisher('/meca/joint_arm1_position_controller/command', Float64, queue_size=10)
        self.arm2_pub = rospy.Publisher('/meca/joint_arm2_position_controller/command', Float64, queue_size=10)

        self.arm1_angle = 0.0
        self.arm2_angle = 0.0
        self.arm_step = 0.01

        rospy.loginfo("Teleop Mecanum Arm Node Started")

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def run(self):
        rospy.loginfo("Điều khiển robot:")
        rospy.loginfo("W: Tiến | X: Lùi | Q: Quay trái | E: Quay phải")
        rospy.loginfo("A: Sang trái | D: Sang phải")
        rospy.loginfo("U: Tăng arm1 | I: Giảm arm1 | J: Tăng arm2 | K: Giảm arm2")
        rospy.loginfo("S: Dừng")
        wheels = Float64MultiArray(data=[0.0, 0.0, 0.0, 0.0])
        cmd_vel = Twist()
        while not rospy.is_shutdown():
            key = self.get_key()
            
            

            if key == "w":
                wheels.data = [2, 2, 2, 2]
                cmd_vel.linear.x = 0.04
                cmd_vel.linear.y = 0.0
            elif key == "x":
                wheels.data = [-2, -2, -2, -2]
                cmd_vel.linear.x = -0.04
                cmd_vel.linear.y = 0.0
            elif key == "q":
                wheels.data = [-6, 6, -6, 6]
                cmd_vel.linear.x = 0.0
                cmd_vel.linear.y = 0.0
            elif key == "e":
                wheels.data = [6, -6, 6, -6]
                cmd_vel.linear.x = 0.0
                cmd_vel.linear.y = 0.0
            elif key == "a":
                wheels.data = [-6, 6, 6, -6]
                cmd_vel.linear.y = 0.04
                cmd_vel.linear.x = 0.0
            elif key == "d":
                wheels.data = [6, -6, -6, 6]
                cmd_vel.linear.y = -0.04
                cmd_vel.linear.x = 0.0
            elif key == "s":
                wheels.data = [0, 0, 0, 0]
                cmd_vel.linear.x = 0.0
                cmd_vel.linear.y = 0.0

            self.wheel_pub.publish(wheels)
            self.cmd_vel_pub.publish(cmd_vel)

            if key == "u":
                self.arm1_angle += self.arm_step
                self.arm1_pub.publish(Float64(self.arm1_angle))
            elif key == "i":
                self.arm1_angle -= self.arm_step
                self.arm1_pub.publish(Float64(self.arm1_angle))
            elif key == "j":
                self.arm2_angle += self.arm_step
                self.arm2_pub.publish(Float64(self.arm2_angle))
            elif key == "k":
                self.arm2_angle -= self.arm_step
                self.arm2_pub.publish(Float64(self.arm2_angle))
            
            elif key == "\x03":
                break

if __name__ == "__main__":
    teleop = TeleopMecanumArm()
    teleop.run()
