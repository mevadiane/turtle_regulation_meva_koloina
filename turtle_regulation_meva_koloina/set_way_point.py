import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class SetWayPoint(Node):
    def __init__(self):
        super().__init__('set_way_point')
        self.pose = None
        self.waypoint = [7.0, 7.0]
        self.Kp = 3.0
        self.Kpl = 1.0
        self.pose_subscriber = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        # Partie 2, exercice 4
        self.is_moving_publisher = self.create_publisher(Bool, "/turtle1/is_moving", self.pose_callback, 10)
        self.timer = self.create_timer(0.1, self.calculs)

    def pose_callback(self, msg):
        self.pose = msg

    def calculs(self):
        if self.pose is None:
            return

        # Partie 1, exercice 4
        theta_desired=math.atan2(
            self.waypoint[1] - self.pose.y,
            self.waypoint[0] - self.pose.x
        )

        # Partie 1, exercice 5
        e = math.atan2(
            math.sin(theta_desired-self.pose.theta), 
            math.cos(theta_desired-self.pose.theta)
        )
        u = self.Kp * e
        msg = Twist()
        msg.angular.z = u
        # self.cmd_vel_publisher.publish(msg)

        # Partie 2, exercice 1
        e1 = math.sqrt((self.waypoint[1] - self.pose.y)**2 + (self.waypoint[0] - self.pose.x)**2)

        # Partie 2, exercice 2
        v = self.Kpl * e1

        # Partie 2, exercice 3 + exercice 4
        distance_tolerance = 0.5
        # msg.angular.z = u
        msg.linear.x = v
        if e1 > distance_tolerance:
            self.is_moving_publisher.publish(True) 
            self.cmd_vel_publisher.publish(msg)
        else:
            self.cmd_vel_publisher = False
            self.is_moving_publisher.publish(False)
        
        

def main(args=None):
	rclpy.init(args=args)
	node = SetWayPoint()
	rclpy.spin(node)
	rclpy.shutdown()

if __name__=="__main__":
	main()