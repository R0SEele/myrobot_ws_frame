import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
import os


def generate_launch_description():
    # 获取默认的urdf路径
    urdf_package_path = get_package_share_directory('myrobot_description')
    default_urdf_path = os.path.join(
        urdf_package_path, 'urdf', 'myrobot', 'myrobot.urdf.xacro'
    )
    default_rviz_config_path = os.path.join(
        urdf_package_path, 'config', 'display_robot_model.rviz'
    )
    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=default_urdf_path,
        description='加载的模型文件路径',
    )
    # 通过文件路径获取内容并转换成参数值对象，以供传入 robot_state_publisher
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', LaunchConfiguration('model')]),
        value_type=str,
    )

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_value}],
        output='screen',
    )

    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'robot_description': robot_description_value}],
        output='screen',
    )

    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
        output='screen',
    )

    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])
