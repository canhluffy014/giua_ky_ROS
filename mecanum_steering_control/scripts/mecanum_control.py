#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState

class JointStateListener:
    def __init__(self):
        rospy.init_node("joint_states_listener", anonymous=True)
        rospy.Subscriber("/joint_states", JointState, self.joint_states_callback)

        # Lưu giá trị vận tốc cũ
        self.encoder_velocities = {
            "encoder_left_forward_joint": 0.0,
            "encoder_left_back_joint": 0.0,
            "encoder_right_back_joint": 0.0,
            "encoder_right_forward_joint": 0.0
        }

        # Thời gian khi lần in cuối cùng
        self.last_log_time = rospy.Time.now()

        rospy.loginfo("Listening to /joint_states topic...")

    def joint_states_callback(self, msg):
        current_time = rospy.Time.now()
        
        # Kiểm tra nếu đã qua 1 giây kể từ lần in trước
        if (current_time - self.last_log_time).to_sec() >= 1.0:
            rospy.loginfo("Received joint states:")

            for joint_name in self.encoder_velocities.keys():
                try:
                    index = msg.name.index(joint_name)
                    velocity = msg.velocity[index] if index < len(msg.velocity) else self.encoder_velocities[joint_name]
                except ValueError:
                    velocity = self.encoder_velocities[joint_name]  # Dùng giá trị cũ nếu thiếu dữ liệu

                self.encoder_velocities[joint_name] = velocity
                rospy.loginfo(f"{joint_name}: Velocity={velocity:.6f}")
            
            # Cập nhật thời gian khi đã in
            self.last_log_time = current_time

    def run(self):
        rospy.spin()

if __name__ == "__main__":
    listener = JointStateListener()
    listener.run()
