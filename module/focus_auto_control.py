from module.tools import *


# focus auto control event line
# 国策自动控制事件链

# namespace
add_namespace='add_namespace = {character_key}_focus_control\n'



# control characters start focus 控制人物开始国策
start_event = '''country_event = {{# start focus event
	id = {character_key}_focus_control.01
	
	hidden = yes

	is_triggered_only = yes

	trigger = {{
		{is_on_the_seat_trigger} = yes
		NOT = {{has_country_flag = {has_start_focus_control_event_flag}}}
	}}

	immediate = {{
		set_country_flag = {has_start_focus_control_event_flag}
		{many_focus_many_if}
		{all_completed_else}
		{no_focus_else}
	}}
}}
'''# character_key,focus_in_progress_flag,is_on_the_seat_trigger,many_focus_many_if,all_completed_else,no_focus_else,has_start_focus_control_event_flag



# has event_control_type one if
one_focus_start_one_if_event_control_type='''		else_if = {{
			limit = {{
{limit}
				NOT = {{ has_shine_effect_on_focus = {focus_id}}}
				NOT = {{ has_completed_focus = {focus_id} }}
                NOT = {{ has_country_flag = {project_code}_{focus_id}_waiting }}
			}}
			country_event = {{ id = {event_id}}}

		}}
'''# limit,character_key,character_id,focus_id,in_progress_flag,costX7_add_1,who_is_doing_variable




# event_choose
one_focus_event_choose_event_namespace='{project_code}_{character_key}_choose.{focus_id}'
one_focus_event_choose_event='''country_event = {{
	id = {project_code}_{character_key}_choose.{focus_id}.01

	is_triggered_only = yes

	trigger = {{
		{is_on_the_seat_trigger} = yes
	}}

	immediate = {{
		set_country_flag = {circle_event_pending_flag}
        {set_waiting_flags}
	}}
	{options}
}}
'''#character_key, focus_id, postion_num_of_focus, is_on_the_seat_trigger, circle_event_pending_flag,pause_while_events_are_pending_other_code


choose_focus_event_option = '''option = {{
	name = {project_code}_{character_key}_choose.{focus_id}.{choose_focus_id}
	custom_effect_tooltip = {project_code}_{character_key}_choose.{focus_id}.{choose_focus_id}_tt
	ai_chance = {{
		base = 1
	}}
	trigger = {{
		{limit}
	}}
	hidden_effect = {{
		activate_shine_on_focus = {choose_focus_id}
		set_country_flag = {{ flag = {in_progress_flag} days = {costX7_add_1} value = 1 }}
		set_variable = {{ {who_is_doing_variable} = {character_id} }}
		country_event = {{ id = {character_key}_focus_control.02 days = {costX7_add_1} }}
        clr_country_flag = {circle_event_pending_flag}
		{clr_waiting_flags}
        
	}}
}}
'''


# event_redline
one_focus_event_redline_event_namespace='{project_code}_{character_key}_redline.{focus_id}'
one_focus_event_redline_event='''country_event = {{
	id = {project_code}_{character_key}_redline.{focus_id}.01

	is_triggered_only = yes

	trigger = {{
		{is_on_the_seat_trigger} = yes
	}}

	immediate = {{
		set_country_flag = {circle_event_pending_flag}
		set_country_flag = {project_code}_{focus_id}_waiting
	}}
	{options}
}}
'''#character_key, focus_id, postion_num_of_focus, is_on_the_seat_trigger, circle_event_pending_flag,pause_while_events_are_pending_other_code

redline_event_start_focus_option = '''	option = {{ 
		name = {project_code}_{character_key}_redline.{focus_id}.continue
		custom_effect_tooltip = {project_code}_{character_key}_redline.{focus_id}.continue_tt
		ai_chance = {{
			base = 1
		}}
		hidden_effect = {{
			activate_shine_on_focus = {focus_id}
			set_country_flag = {{ flag = {in_progress_flag} days = {costX7_add_1} value = 1 }}
			set_variable = {{ {who_is_doing_variable} = {character_id} }}
			clr_country_flag = {circle_event_pending_flag}
            clr_country_flag = {project_code}_{focus_id}_waiting
			country_event = {{ id = {character_key}_focus_control.02 days = {costX7_add_1} }}

		}}
	}}
'''
redline_event_stop_focus_option = '''	option = {{
		name = {project_code}_{character_key}_redline.{focus_id}.stop
		custom_effect_tooltip = {project_code}_{character_key}_redline.{focus_id}.stop_tt
		ai_chance = {{
			base = 1
		}}
		hidden_effect = {{
			set_country_flag = {focus_id}_was_stopped
            clr_country_flag = {circle_event_pending_flag}
            clr_country_flag = {project_code}_{focus_id}_waiting
			country_event = {{ id = {character_key}_focus_control.01 days = {days_to_start_focus} random_days = {days_to_start_focus_random_days} }}
		}}
	}}
'''


# event_remind
one_focus_event_remind_event_namespace='{project_code}_{character_key}_remind'
one_focus_event_remind_event='''country_event = {{
	id = {project_code}_{character_key}_remind.{focus_id}

	is_triggered_only = yes

	trigger = {{
		{is_on_the_seat_trigger} = yes
	}}

	immediate = {{
		activate_shine_on_focus = {focus_id}
		set_country_flag = {{ flag = {in_progress_flag} days = {costX7_add_1} value = 1 }}
		set_variable = {{ {who_is_doing_variable} = {character_id} }}
		country_event = {{ id = {character_key}_focus_control.02 days = {costX7_add_1} }}
	}}
	option = {{
		name = {project_code}_{character_key}_remind.{focus_id}.ok
		custom_effect_tooltip = {project_code}_{character_key}_remind.{focus_id}.ok_tt
		ai_chance = {{
			base = 1
		}}

	}}
}}
'''#character_key, focus_id, postion_num_of_focus, is_on_the_seat_trigger, circle_event_pending_flag,pause_while_events_are_pending_other_code


# no_control

one_focus_start_one_if_no_control='''		else_if = {{
			limit = {{
{limit}
				NOT = {{ has_shine_effect_on_focus = {focus_id}}}
				NOT = {{ has_completed_focus = {focus_id} }}
                NOT = {{ has_country_flag = {project_code}_{focus_id}_waiting }}
			}}
			activate_shine_on_focus = {focus_id}
			set_country_flag = {{ flag = {in_progress_flag} days = {costX7_add_1} value = 1 }}
			set_variable = {{ {who_is_doing_variable} = {character_id} }}
			country_event = {{ id = {character_key}_focus_control.02 days = {costX7_add_1} }}

		}}
'''# limit,character_key,character_id,focus_id,in_progress_flag,costX7_add_1,who_is_doing_variable


all_completed_else='''		else_if = {{
			limit = {{
				{all_focus_completed_trigger} = yes
			}}
			#log = "{character_key} completed all his focus"
		}}

'''

one_focus_start_no_focus_else='''		else = {{ #Debug logs
			#log = "SOMETHING WENT WRONG WITH {character_key}'s FOCUS BRANCH - Cannot start new focus"
			set_country_flag = {has_start_focus_control_event_flag}
			country_event = {{ id = {character_key}_focus_control.01 days = {days_to_start_focus} random_days = {days_to_start_focus_random_days} }}
		}}
'''

# control characters complete focus 控制人物完成国策
complete_event = '''country_event = {{
	id = {character_key}_focus_control.02

	hidden = yes

	is_triggered_only = yes

	trigger = {{
		{is_on_the_seat_trigger} = yes
	}}

	immediate = {{
		{many_focus_many_if}
		{no_focus_else}
	}}
}}
'''

one_focus_complete_one_if='''		else_if = {{
			limit = {{
				has_shine_effect_on_focus = {focus_id}
				check_variable = {{ {who_is_doing_variable} = {character_id} }} 
				{limit}
			}}
			complete_national_focus = {{
				focus = {focus_id}
				use_side_message = yes
				originator_name = {character_key}
			}}
			clr_country_flag = {in_progress_flag}
			clr_country_flag = {has_start_focus_control_event_flag}
			country_event = {{ id = {character_key}_focus_control.01 days = {days_to_start_focus} random_days = {days_to_start_focus_random_days} }}
		}}
'''

one_focus_complete_one_limit=''
one_focus_complete_no_focus_else='''		else = {{ #Debug logs
			#log = "SOMETHING WENT WRONG WITH {character_key}'s FOCUS BRANCH - Cannot complete focus"
			clr_country_flag = {in_progress_flag}
			clr_country_flag = {has_start_focus_control_event_flag}
			country_event = {{ id = {character_key}_focus_control.01 days = {days_to_start_focus} random_days = {days_to_start_focus_random_days} }}

		}}
'''

# 一个character完成全部国策trigger
# trigger checks if one character completed all his focus

def all_focus_completed_trigger(csv_characters, csv_focus, project_code, dir_output):
    Df_characters = pandas.read_csv(csv_characters)
    Df_focus = pandas.read_csv(csv_focus)

    # 创建输出目录和子目录
    # Create output directory and subdirectories
    create_dir(dir_output)
    create_dir(os.path.join(dir_output, 'common'))
    create_dir(os.path.join(dir_output, 'common', 'scripted_triggers'))

    # 生成scripted trigger，检查某个character的所有国策是否完成
    # Generate scripted trigger to check if one character's all focuses are completed
    text_all_focus_completed_trigger = ''
    text_one_character_all_focus_completed = '''{project_code}_{character_KEY}_all_focus_completed = {{
    AND = {{
        {all_focus_check}
    }}
}}
'''

    for s_character in Df_characters.iterrows():
        character_KEY = s_character[1].loc['KEY']
        complete_focus_order_data = s_character[1].loc['complete_focus_order']
        all_focus_check = ''

        if type(complete_focus_order_data) == str:
            try:
                list_can_complete_focus = json.loads(complete_focus_order_data)
            except Exception as e:
                print('Read character_csv {0}\'s {1} data failed. 读取character_csv中{0}的{1}数据失败。'.format(str(character_KEY), 'complete_focus_order'))
                raise e

            if type(list_can_complete_focus) == list and len(list_can_complete_focus) > 0:
                all_focus_check = ''.join(['has_completed_focus = {}\n'.format(focus_id) for focus_id in list_can_complete_focus])
            else:
                print(character_KEY, ': Read complete_focus_order failed, require a list. 读取"complete_focus_order"数据失败，请输入一个列表。（csv_character）')

        text_all_focus_completed_trigger += text_one_character_all_focus_completed.format(
            project_code=project_code,
            character_KEY=character_KEY,
            all_focus_check=all_focus_check
        )

    with open(os.path.join(dir_output, 'common', 'scripted_triggers', project_code + "_characters_completed_all_focus_scripted_triggers.txt"), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text_all_focus_completed_trigger)

# start_focus_event
def start_focus_event(csv_characters,csv_focus,project_code, circle_event_pending_flag, days_to_start_focus, days_to_start_focus_random_days, dir_output):
	Df_characters=pandas.read_csv(csv_characters)
	Df_focus=pandas.read_csv(csv_focus)
	#mkdir
	try:
		os.mkdir(dir_output)
	except:
		pass
	try:
		os.mkdir(os.path.join(dir_output,'events'))
	except:
		pass
	# event control all focus start
	start_focus_event_all_namespace=''
	start_focus_event_all_events=''
	# event control focus start event_control_type
	event_control_type_event_namespace_all=''
	event_control_type_event_all=''

	for row in Df_characters.iterrows():
		s_character=row[1]
		character_KEY=s_character['KEY']
		character_id=s_character['ID']
		complete_focus_order_data = s_character['complete_focus_order']

		# namespace
		namespace=add_namespace.format(character_key=character_KEY)
		start_focus_event_all_namespace+=namespace
		# event control focus start event_control_type
		event_control_type_event_namespace_one_character=[]
		event_control_type_event_one_character=''
		# focus control events
		if type(complete_focus_order_data)==str:
			try:
				list_can_complete_focus=json.loads(complete_focus_order_data)
			except Exception as e :
				print('Read character_csv {0}\'s {1} data failed. 读取character_csv中{0}的{1}数据失败。'.format(str(character_KEY,'complete_focus_order')))
				print()
				raise e

			if not type(list_can_complete_focus)==list:
				print(character_KEY,': Read complete_focus_order failed, require a list. 读取"complete_focus_order"数据失败，请输入一个列表。（csv_character）')
			else:
				if len(list_can_complete_focus)>0:
					many_focus_many_if = ''



					for focus_id in list_can_complete_focus:
						series_focus=Df_focus.loc[Df_focus['ID']==focus_id].iloc[0, :]

						limit=''
						# check about "aviliable" in focus 
						if type(series_focus['available'])==str:
							limit+=series_focus['available']
						else:
							pass
						limit+='\n'
						
						# prerequisite focus check
						data_prerequisite = series_focus['prerequisite']
						text_prerequisite=''
						if not pandas.isnull(data_prerequisite):
							list_prerequisite = load_json(series_focus, 'prerequisite', '', "csv_focus", focus_id) 
							if type(list_prerequisite)!=list:# error: wrong data type
								print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(series_focus['ID'],'prerequisite')))
							else:
								if get_list_depth(list_prerequisite)!=2:# error: wrong depth
									print('Read focus_csv row {0} columns {1}failed, require depth = 2 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个2层的list'.format(str(series_focus['ID'],'prerequisite')))
								else:
									for row in list_prerequisite:
										text_row='OR = {'
										for focus in row:
											text_row+=' has_completed_focus = '+focus+'\n			'
										text_row+='}\n			'
										text_prerequisite+=text_row
						
						limit+=text_prerequisite
						# mutually_exclusive focus check
						data_mutually_exclusive = series_focus['mutually_exclusive']
						text_mutually_exclusive=''
						# has_start_focus_control_event_flag
						has_start_focus_control_event_flag=character_KEY+'_has_start_focus_control_event_flag'
						if not pandas.isnull(data_mutually_exclusive):
							list_mutually_exclusive=load_json(series_focus, 'mutually_exclusive', '', "csv_focus", focus_id) 
							if type(list_mutually_exclusive)!=list:# error: wrong data type
								print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(series_focus['ID'],'mutually_exclusive')))
							else:
								if get_list_depth(list_mutually_exclusive)!=1:# error: wrong depth
									print('Read focus_csv row {0} columns {1}failed, require depth = 1 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个2层的list'.format(str(series_focus['ID'],'mutually_exclusive')))
								else:
									text_row=''
									for focus in list_mutually_exclusive:
										text_row+='NOT = {\n		 has_completed_focus = '+focus +'\n		has_shine_effect_on_focus = '+focus +'\n		}\n		'
									text_mutually_exclusive+=text_row+'\n        '
						limit+=text_mutually_exclusive

						focus_in_progress_flag = project_code+"_"+focus_id+"_in_progress_flag"
						costX7_add_1= str(int(series_focus['cost'])*7+1)
						who_is_doing_variable=project_code+"_"+focus_id+"_doing_focus_advisor"
						is_on_the_seat_trigger='{0}_{1}_is_on_the_seat'.format(project_code, character_KEY)
						#### event_choose
						if series_focus['event_control_type']=="event_choose":
							# event namespace
							event_control_type_event_namespace_one_character+=['add_namespace = {}\n'.format(
								one_focus_event_choose_event_namespace.format(project_code=project_code,character_key=character_KEY,focus_id=focus_id))]
							#options
							options=''
							clr_waiting_flags = ''
							set_waiting_flags = ''
							for choose_focus_id in [focus_id]+list_mutually_exclusive:
								set_waiting_flags += 'set_country_flag = {project_code}_{focus_id}_waiting\n'.format(
									project_code=project_code,
									focus_id=choose_focus_id
								)
								clr_waiting_flags += 'clr_country_flag = {project_code}_{focus_id}_waiting\n'.format(
									project_code=project_code,
									focus_id=choose_focus_id
								)
								options+=choose_focus_event_option.format(
									project_code=project_code,
									character_id=character_id,
									character_key=character_KEY,
									focus_id=focus_id,
									limit=limit,
									choose_focus_id=choose_focus_id,
									in_progress_flag=project_code+"_"+choose_focus_id+"_in_progress_flag",
									costX7_add_1=costX7_add_1,
									who_is_doing_variable=project_code+"_"+choose_focus_id+"_doing_focus_advisor",
									circle_event_pending_flag=circle_event_pending_flag,
									clr_waiting_flags=clr_waiting_flags
								)
							# event_control_type_event
							event_control_type_event_one_character+=one_focus_event_choose_event.format(
									project_code=project_code,
									character_key=character_KEY,
									focus_id=focus_id,
									is_on_the_seat_trigger=is_on_the_seat_trigger,
									circle_event_pending_flag=circle_event_pending_flag,
									options=options,
									set_waiting_flags=set_waiting_flags
							)

							# oneif
							many_focus_many_if+=one_focus_start_one_if_event_control_type.format(
								limit=limit,
								focus_id=focus_id,
								project_code=project_code,
								event_id='{project_code}_{character_key}_choose.{focus_id}.01'.format(
									character_key=character_KEY,
									project_code=project_code,
									focus_id=focus_id
								)
							)

						#### event_redline
						elif series_focus['event_control_type']=="event_redline":
							# event namespace
							event_control_type_event_namespace_one_character+=['add_namespace = {}\n'.format(
								one_focus_event_redline_event_namespace.format(
									project_code=project_code,
									character_key=character_KEY,
									focus_id=focus_id
									)
								)
							]
							# event_control_type_event_options
								# start option
							redline_event_start_focus_option_temp=redline_event_start_focus_option.format(
								project_code=project_code,
								character_id=character_id,
								character_key=character_KEY,
								focus_id=focus_id,
								in_progress_flag=focus_in_progress_flag,
								circle_event_pending_flag=circle_event_pending_flag,
								costX7_add_1=costX7_add_1,
								who_is_doing_variable=who_is_doing_variable

							)
								# stop option
							redline_event_stop_focus_option_temp=redline_event_stop_focus_option.format(
								project_code=project_code,
								character_id=character_id,
								character_key=character_KEY,
								focus_id=focus_id,
								circle_event_pending_flag=circle_event_pending_flag,
								days_to_start_focus=days_to_start_focus,
								days_to_start_focus_random_days=days_to_start_focus_random_days

							)

							options= redline_event_start_focus_option_temp+redline_event_stop_focus_option_temp
							# event_control_type_event
							event_control_type_event_one_character+=one_focus_event_redline_event.format(
									project_code=project_code,
									character_key=character_KEY,
									character_id=character_id,
									focus_id=focus_id,
									is_on_the_seat_trigger=is_on_the_seat_trigger,
									circle_event_pending_flag=circle_event_pending_flag,
									options=options
							)
							# one_if
							many_focus_many_if+=one_focus_start_one_if_event_control_type.format(
								limit=limit,
								focus_id=focus_id,
								project_code=project_code,
								event_id="{project_code}_{character_key}_redline.{focus_id}.01".format(
									project_code=project_code,
									character_key=character_KEY,
									focus_id=focus_id
									)
							)

						#### event_remind
						elif series_focus['event_control_type']=="event_remind":
							# event namespace
							event_control_type_event_namespace_one_character+=[
								'add_namespace = {}\n'.format(
									one_focus_event_remind_event_namespace.format(
										project_code=project_code,character_key=character_KEY
									)
								)
							]
							# event_control_type_event
							event_control_type_event_one_character+=one_focus_event_remind_event.format(
									project_code=project_code,
									character_key=character_KEY,
									character_id=character_id,
									focus_id=focus_id,
									is_on_the_seat_trigger=is_on_the_seat_trigger,
									in_progress_flag=focus_in_progress_flag,
									costX7_add_1=costX7_add_1,
									who_is_doing_variable=who_is_doing_variable
							)
							# one_if
							many_focus_many_if+=one_focus_start_one_if_event_control_type.format(
								limit=limit,
								focus_id=focus_id,
								project_code=project_code,
								event_id="{project_code}_{character_key}_remind.{focus_id}".format(
									project_code=project_code,
									character_key=character_KEY,
									focus_id=focus_id
								)
							)
						
						#### do_nothing
						else:
							# one_if
							many_focus_many_if+=one_focus_start_one_if_no_control.format(
								limit=limit,
								has_start_focus_control_event_flag=has_start_focus_control_event_flag,
								character_key=character_KEY,
								character_id=character_id,
								focus_id=focus_id,
								in_progress_flag=focus_in_progress_flag,
								costX7_add_1=costX7_add_1,
								who_is_doing_variable=who_is_doing_variable,
								days_to_start_focus=days_to_start_focus,
								days_to_start_focus_random_days=days_to_start_focus_random_days,
								project_code=project_code
							)

					many_focus_many_if=many_focus_many_if.replace('else_if','if',1)
					one_start_event=start_event.format( 
							character_key=character_KEY,
							focus_in_progress_flag=focus_in_progress_flag,
							is_on_the_seat_trigger='{0}_{1}_is_on_the_seat'.format(project_code, character_KEY),
							many_focus_many_if=many_focus_many_if,
							all_completed_else=all_completed_else.format(
								all_focus_completed_trigger=project_code+'_'+character_KEY+'_all_focus_completed',
								character_key=character_KEY,
								),
							no_focus_else=one_focus_start_no_focus_else.format(
								character_key=character_KEY,
								days_to_start_focus=days_to_start_focus,
								days_to_start_focus_random_days=days_to_start_focus_random_days,
								has_start_focus_control_event_flag=has_start_focus_control_event_flag
							),
							has_start_focus_control_event_flag=has_start_focus_control_event_flag
						)
					# add
					start_focus_event_all_events+=one_start_event

					#event
					event_control_type_event_all+=event_control_type_event_one_character
					
					#namespace
					event_control_type_event_namespace_all+="".join(list(set(event_control_type_event_namespace_one_character)))

	# main start event txt
	start_focus_event_alltext=start_focus_event_all_namespace+'\n'+start_focus_event_all_events

	# event_control_type focus event txt
	event_control_type_focus_events_alltext=event_control_type_event_namespace_all+'\n'+event_control_type_event_all

	# write main start event txt
	with open(os.path.join(dir_output,'events',project_code+'_start_focus_event.txt'),'w',encoding='utf_8', newline='\n')as f:
		f.write(start_focus_event_alltext)

	# write event_control_type focus event txt
	with open(os.path.join(dir_output,'events',project_code+'_event_control_type_focus_event.txt'),'w',encoding='utf_8', newline='\n')as f:
		f.write(event_control_type_focus_events_alltext)


# complete_focus_event
def complete_focus_event(csv_characters,csv_focus, project_code, days_to_start_focus, days_to_start_focus_random_days, dir_output):
	Df_characters=pandas.read_csv(csv_characters)
	Df_focus=pandas.read_csv(csv_focus)
	#mkdir
	try:
		os.mkdir(dir_output)
	except:
		pass
	try:
		os.mkdir(os.path.join(dir_output,'events'))
	except:
		pass

	complete_focus_event_all_namespace=''
	complete_focus_event_all_events=''

	for row in Df_characters.iterrows():
		s_character=row[1]
		character_KEY=s_character['KEY']
		character_id=s_character['ID']
		complete_focus_order_data = s_character['complete_focus_order']
		has_start_focus_control_event_flag=character_KEY+'_has_start_focus_control_event_flag'

		# namespace
		namespace=add_namespace.format(character_key=character_KEY)
		complete_focus_event_all_namespace+=namespace

		#events
		if type(complete_focus_order_data)==str:
			try:
				list_can_complete_focus=json.loads(complete_focus_order_data)
			except Exception as e :
				print('Read character_csv {0}\'s {1} data failed. 读取character_csv中{0}的{1}数据失败。'.format(str(character_KEY,'complete_focus_order')))
				print()
				raise e

			if not type(list_can_complete_focus)==list:
				print(character_KEY,': Read complete_focus_order failed, require a list. 读取"complete_focus_order"数据失败，请输入一个列表。（csv_character）')
			else:
				if len(list_can_complete_focus)>0:
					many_focus_many_if = ''
					for focus_id in list_can_complete_focus:
						series_focus=Df_focus.loc[Df_focus['ID']==focus_id].iloc[0, :]

						limit=''
						# check about "aviliable" in focus 
						if type(series_focus['available'])==str:
							limit+=series_focus['available']
						else:
							pass
						limit+='\n'
						
						# prerequisite focus check
						data_prerequisite = series_focus['prerequisite']
						text_prerequisite=''
						if pandas.isnull(data_prerequisite):
							pass
						else:
							list_prerequisite = load_json(series_focus, 'prerequisite', '', "csv_focus", focus_id) 
							if type(list_prerequisite)!=list:# error: wrong data type
								print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(series_focus['ID'],'prerequisite')))
							else:
								if get_list_depth(list_prerequisite)!=2:# error: wrong depth
									print('Read focus_csv row {0} columns {1}failed, require depth = 2 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个2层的list'.format(str(series_focus['ID'],'prerequisite')))
								else:
									for row in list_prerequisite:
										text_row='OR = {'
										for focus in row:
											text_row+=' has_completed_focus = '+focus+'\n			'
										text_row+='}\n			'
										text_prerequisite+=text_row
						limit+=text_prerequisite
						# mutually_exclusive focus check
						data_mutually_exclusive = series_focus['mutually_exclusive']
						text_mutually_exclusive=''
						# has_complete_focus_control_event_flag
						has_complete_focus_control_event_flag=character_KEY+'_has_complete_focus_control_event_flag'
						if not pandas.isnull(data_mutually_exclusive):
							list_mutually_exclusive = load_json(series_focus, 'mutually_exclusive', '', "csv_focus", focus_id) 
							if type(list_mutually_exclusive)!=list:# error: wrong data type
								print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(series_focus['ID'],'mutually_exclusive')))
							else:
								if get_list_depth(list_mutually_exclusive)!=1:# error: wrong depth
									print('Read focus_csv row {0} columns {1}failed, require depth = 1 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个2层的list'.format(str(series_focus['ID'],'mutually_exclusive')))
								else:
									text_row=''
									for focus in list_mutually_exclusive:
										text_row+='NOT = { has_completed_focus = '+focus +'\n		has_shine_effect_on_focus = '+focus +'}\n		'
									text_mutually_exclusive+=text_row+'\n        '
						limit+=text_mutually_exclusive

						focus_in_progress_flag = project_code+"_"+focus_id+"_in_progress_flag"

						many_focus_many_if+=one_focus_complete_one_if.format(
                            focus_id=focus_id,
                            character_key=character_KEY,
							who_is_doing_variable=project_code+"_"+focus_id+"_doing_focus_advisor",
							character_id=character_id,
							limit=limit,
							in_progress_flag=focus_in_progress_flag,
							has_start_focus_control_event_flag=has_start_focus_control_event_flag,
							days_to_start_focus=days_to_start_focus,
							days_to_start_focus_random_days=days_to_start_focus_random_days

						)

					many_focus_many_if=many_focus_many_if.replace('else_if','if',1)
					one_complete_event=complete_event.format( 
							character_key=character_KEY,
                            focus_in_progress_flag=focus_in_progress_flag,
							is_on_the_seat_trigger='{0}_{1}_is_on_the_seat'.format(project_code, character_KEY),
                            many_focus_many_if=many_focus_many_if,
							no_focus_else=one_focus_complete_no_focus_else.format(
								character_key=character_KEY,
								in_progress_flag=focus_in_progress_flag,
								has_start_focus_control_event_flag=has_start_focus_control_event_flag,
								days_to_start_focus=days_to_start_focus,
								days_to_start_focus_random_days=days_to_start_focus_random_days)
						)
					complete_focus_event_all_events+=one_complete_event
	
	complete_focus_event_alltext=complete_focus_event_all_namespace+'\n'+complete_focus_event_all_events
	# write txt
	with open(os.path.join(dir_output,'events',project_code+'_complete_focus_event.txt'),'w',encoding='utf_8', newline='\n')as f:
		f.write(complete_focus_event_alltext)