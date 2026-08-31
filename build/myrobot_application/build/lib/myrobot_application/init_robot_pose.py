from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main():
    rclpy.init()
    nav = BasicNavigator()

    """
    PoseStamped is a ROS2 message type that represents a pose in 3D space
    with a timestamp and frame of reference.
    """
    init_pose = PoseStamped()   # 定义消息类型
    init_pose.header.frame_id = "map"   # 定义坐标系，具体是在“map”坐标系下进行描述
    init_pose.header.stamp = nav.get_clock().now().to_msg() # 获取当前时间戳
    # 具体位姿
    init_pose.pose.position.x = 0.0
    init_pose.pose.position.y = 0.0
    init_pose.pose.orientation.w = 1.0
    nav.setInitialPose(init_pose)   # 设置初始位姿
    nav.waitUntilNav2Active() # 等待导航可用
    rclpy.spin(nav)
    rclpy.shutdown()