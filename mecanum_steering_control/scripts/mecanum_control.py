#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState

class JointStateListener:
    def __init__(self):
        rospy.init_node("joint_states_listener", anonymous=True)
        rospy.Subscriber("/joint_states", JointState, self.joint_states_callback)

        # Publisher cho encoder velocities
        self.encoder_pub = rospy.Publisher("/encoder_velocities", JointState, queue_size=10)

        # Lưu giá trị vận tốc cũ
        self.encoder_velocities = {
            "encoder_left_forward_joint": 0.0,
            "encoder_left_back_joint": 0.0,
            "encoder_right_back_joint": 0.0,
            "encoder_right_forward_joint": 0.0
        }

        self.last_log_time = rospy.Time.now()
        rospy.loginfo("Listening to /joint_states topic...")

    def joint_states_callback(self, msg):
        current_time = rospy.Time.now()

       
        if (current_time - self.last_log_time).to_sec() >= 1.0:
            rospy.loginfo("Received joint states:")

            for joint_name in self.encoder_velocities.keys():
                if joint_name in msg.name:
                    index = msg.name.index(joint_name)
                    if len(msg.velocity) > index:  
                        velocity = msg.velocity[index]
                    else:
                        velocity = 0.0  
                else:
                    velocity = 0.0  
                self.encoder_velocities[joint_name] = velocity
                rospy.loginfo(f"{joint_name}: Velocity={velocity:.6f}")

            # Cập nhật thời gian log lần cuối
            self.last_log_time = current_time

            # Gửi velocity tới topic /encoder_velocities
            encoder_msg = JointState()
            encoder_msg.name = list(self.encoder_velocities.keys())
            encoder_msg.velocity = list(self.encoder_velocities.values())
            encoder_msg.effort = [0.0] * len(encoder_msg.name)
            self.encoder_pub.publish(encoder_msg)

    def run(self):
        rospy.spin()

if __name__ == "__main__":
    listener = JointStateListener()
    listener.run()
