import numpy as np
import time
from common.Controller import Controller
from common.State import State, BehaviorState
from common.Command import Command
from pupper.TrainingInterface import TrainingInterface
from pupper.Config import Configuration
from pupper.Kinematics import four_legs_inverse_kinematics

def main(use_imu=False):
    """Main program
    """

    # Create config
    config = Configuration()
    training_interface = TrainingInterface()

    # Create controller and user input handles
    controller = Controller(
        config,
        four_legs_inverse_kinematics,
    )
    state = State()

    # Behavior to learn
    state.behavior_state = BehaviorState.TROT

    speed = 0.4

    training_interface.set_reward(speed)

    print("Summary of gait parameters:")
    print("overlap time: ", config.overlap_time)
    print("swing time: ", config.swing_time)
    print("z clearance: ", config.z_clearance)
    print("x shift: ", config.x_shift)

    while True:
        # Parse the udp joystick commands and then update the robot controller's parameters
        command = Command()

        speed = min(1.0, max(-1.0, 0.4 + np.random.randn() * 0.03))
        training_interface.set_reward(speed)

        # Go forward at max speed
        command.horizontal_velocity = np.array([1.0, 0.0]) * speed

        quat_orientation = (
            np.array([1, 0, 0, 0])
        )
        state.quat_orientation = quat_orientation

        # Step the controller forward by dt
        controller.run(state, command)

        # Update the agent with the angles
        training_interface.set_actuator_positions(state.joint_angles)


main()