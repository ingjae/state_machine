#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_manipulation_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as flexbe_manipulation_states__MoveitToJointsDynState
from flexbe_states.wait_state import WaitState
from moveit_flexbe_states.compute_grasp_state import ComputeGraspState
from moveit_flexbe_states.output_pose_test import HandOverPoseStamped
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Dec 18 2020
@author: injae
'''
class moveit_test_pleaseSM(Behavior):
	'''
	moveit
	'''


	def __init__(self):
		super(moveit_test_pleaseSM, self).__init__()
		self.name = 'moveit_test_please'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		group = 'panda_arm'
		ready_pose = [0,-0.785,0,-2.356,0,1.571,0.785]
		extend_pose = [0,0,0,-0.698,0,1.571,0.0]
		target_pose = [0.403,-0.334,0.587]
		arm_joint = ["panda_joint1","panda_joint2", "panda_joint3", "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"]
		push_pose = [0.503,-0.334,0.587]
		end_link = 'panda_hand'
		# x:998 y:645, x:1024 y:159
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.joint_names = ["panda_joint1","panda_joint2", "panda_joint3", "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"]
		_state_machine.userdata.joint_values = [0,0,0,-1.57,1.57,1.57,0]
		_state_machine.userdata.preset_pose = extend_pose
		_state_machine.userdata.home_pose = ready_pose
		_state_machine.userdata.target_values = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:68 y:42
			OperatableStateMachine.add('Handover Pose',
										HandOverPoseStamped(target_pose=target_pose, world_frame='world'),
										transitions={'continue': 'Compute jointstate from pose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:266 y:474
			OperatableStateMachine.add('Compute jointstate from pose(push)',
										ComputeGraspState(group=group, offset=0, joint_names=arm_joint, tool_link=end_link, rotation=0),
										transitions={'continue': 'move_target(push)', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose', 'joint_values': 'target_values', 'joint_names': 'joint_names'})

			# x:43 y:471
			OperatableStateMachine.add('Handover Pose(push)',
										HandOverPoseStamped(target_pose=push_pose, world_frame='world'),
										transitions={'continue': 'Compute jointstate from pose(push)', 'failed': 'Compute jointstate from pose(push)'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose'})

			# x:938 y:486
			OperatableStateMachine.add('move home',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=group, action_topic='/move_group'),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'home_pose', 'joint_names': 'joint_names'})

			# x:528 y:38
			OperatableStateMachine.add('move_target',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=group, action_topic='/move_group'),
										transitions={'reached': 'wait 3secend', 'planning_failed': 'failed', 'control_failed': 'wait 3secend'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'target_values', 'joint_names': 'joint_names'})

			# x:523 y:477
			OperatableStateMachine.add('move_target(push)',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=group, action_topic='/move_group'),
										transitions={'reached': 'wait 3secend_2', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'target_values', 'joint_names': 'joint_names'})

			# x:800 y:41
			OperatableStateMachine.add('wait 3secend',
										WaitState(wait_time=3),
										transitions={'done': 'Handover Pose(push)'},
										autonomy={'done': Autonomy.Off})

			# x:774 y:480
			OperatableStateMachine.add('wait 3secend_2',
										WaitState(wait_time=3),
										transitions={'done': 'move home'},
										autonomy={'done': Autonomy.Off})

			# x:269 y:45
			OperatableStateMachine.add('Compute jointstate from pose',
										ComputeGraspState(group=group, offset=0, joint_names=arm_joint, tool_link=end_link, rotation=0),
										transitions={'continue': 'move_target', 'failed': 'move_target'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose', 'joint_values': 'target_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
