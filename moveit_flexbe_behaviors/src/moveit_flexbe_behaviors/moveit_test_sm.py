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
from moveit_flexbe_states.compute_grasp_state import ComputeGraspState
from moveit_flexbe_states.output_pose_test import HandOverPoseStamped
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Dec 18 2020
@author: injae
'''
class moveit_testSM(Behavior):
	'''
	moveit
	'''


	def __init__(self):
		super(moveit_testSM, self).__init__()
		self.name = 'moveit_test'

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
		target_pose = [0.597,-0.040,0.469]
		arm_joint = ["panda_joint1","panda_joint2", "panda_joint3", "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"]
		# x:861 y:484, x:232 y:335
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

			# x:741 y:54
			OperatableStateMachine.add('move home',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=group, action_topic='/move_group'),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'home_pose', 'joint_names': 'joint_names'})

			# x:520 y:57
			OperatableStateMachine.add('move_extend',
										flexbe_manipulation_states__MoveitToJointsDynState(move_group=group, action_topic='/move_group'),
										transitions={'reached': 'move home', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pose', 'joint_names': 'joint_names'})

			# x:256 y:50
			OperatableStateMachine.add('Compute jointstate from pose',
										ComputeGraspState(group=group, offset=0, joint_names=arm_joint, tool_link='panda_hand', rotation=0),
										transitions={'continue': 'move_extend', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'pose', 'joint_values': 'target_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
