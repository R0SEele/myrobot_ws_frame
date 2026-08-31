import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion

"""
根据获取TF变换,监听机器人位姿
"""
class TFListener(Node):

    def __init__(self):
        super().__init__('tf2_listener')
        self.buffer = Buffer()  # 创建一个tf2缓冲区，用于存储和管理坐标变换信息
        self.listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1, self.get_transform)

    """
    转换TF变换为欧拉角,计算机器人在地图坐标系下的位姿
    """
    def get_transform(self):
        try:
            tf = self.buffer.lookup_transform(
                'map', 'base_footprint', rclpy.time.Time(seconds=0), rclpy.time.Duration(seconds=1))
            transform = tf.transform
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w
            ])
            self.get_logger().info(
                f'平移:{transform.translation},旋转四元数:{transform.rotation}:旋转欧拉角:{rotation_euler}')
        except Exception as e:
            self.get_logger().warn(f'不能够获取坐标变换，原因: {str(e)}')


def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
