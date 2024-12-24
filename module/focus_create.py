from module.tools import *

focus_basic="""    focus = {{
        id = {focus_id}
        icon = {icon}

        {text_prerequisite}
        {text_mutually_exclusive}
        {comment_event_control_type}

        x = {x}
        y = {y}
        cost = {cost}
        {relative_position_id}

        available = {{
            {text_available_explain_for_auto_control}
            {available}
            {pause_while_events_are_pending_available}
        }}

        {pause_while_events_are_pending_other_code}

        completion_reward = {{
            {completion_reward}
        }}

    }}

"""

available_explain_for_auto_control='''if = {{ #ADVISOR WORKING ON THE FOCUS (Show progress)
                limit = {{
                    has_country_flag = {focus_in_progress_flag}
                }}
                set_temp_variable = {{ temp_focus_days = {focus_cost} }} #For tooltip purposes
                multiply_temp_variable = {{ temp_focus_days = 7 }} #The constant uses focus cost which is in weeks, so convert to days
                
                {text_available_for_auto_control_someone_is_working}
            }}

            {text_available_for_auto_control_no_one_is_working}
'''# focus_in_progress_flag, focus_cost, text_available_for_auto_control_someone_is_working, text_available_for_auto_control_no_one_is_working

available_for_auto_control_one_character_is_working='''                else_if = {{ #someone working on it
                    limit = {{
                        check_variable = {{ {doing_focus_advisor} = {character_id} }}
                    }}
                    custom_override_tooltip = {{
                        tooltip = {{
                            localization_key = {inner_circle_focus_in_progress_tt}
                            CHARACTER = {character_key}
                            FLAG_DAYS = [?{focus_in_progress_flag}:days]
                        }}
                        always = no 
                    }}
                }}
'''# focus_in_progress_flag, focus_cost, doing_focus_advisor(variable name), character_id, character_key, inner_circle_focus_in_progress_tt

available_for_auto_control_no_one_is_working='''else = {{ #NOT BEEN WORKED ON (Just Explain)
                custom_override_tooltip = {{
                    tooltip = {{
                        localization_key = {focus_can_only_be_completed_by_advisor_tt}
{many_characters}
                    }}
                    always = no
                }}
            }}
'''# focus_can_only_be_completed_by_advisor_tt, many_characters 

# one_character + one_character + ...... = many_characters
one_character='''                        CHARACTER{num} = {character_key}
'''# num, character_key, focus_id

def genarate_one_focus(s_focus, project_code, circle_event_pending_flag, Df_characters):

    status_code=0
    focus_all_text=''

    #ID
    # ID
    focus_id=read_str(s_focus['ID'],'')

    #icon
    # 图标
    icon=read_str(s_focus['icon'],'')

    # text_prerequisite
    # 前提条件文本
    data_prerequisite = s_focus['prerequisite']
    text_prerequisite = ''
    if not pandas.isnull(data_prerequisite):
        list_prerequisite = load_json(s_focus, 'prerequisite', '', "csv_focus", focus_id) 
        if type(list_prerequisite) != list:
            print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(s_focus['ID']), 'prerequisite'))
            s_focus['focus_all_text'] = focus_all_text
            return focus_all_text, status_code
        if get_list_depth(list_prerequisite) != 2:
            print('Read focus_csv row {0} columns {1}failed, require depth = 2 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个2层的list'.format(str(s_focus['ID']), 'prerequisite'))
            s_focus['focus_all_text'] = focus_all_text
            return focus_all_text, status_code

        for row in list_prerequisite:
            text_row = ''
            for focus in row:
                text_row += ' focus = ' + focus
            text_prerequisite += 'prerequisite = {' + text_row + ' }\n        '

    # text_mutually_exclusive
    # 互斥条件文本
    data_mutually_exclusive = s_focus['mutually_exclusive']
    text_mutually_exclusive=''
    if not pandas.isnull(data_mutually_exclusive):
        list_mutually_exclusive=load_json(s_focus, 'mutually_exclusive', '', "csv_focus", focus_id) 

        if type(list_mutually_exclusive)!=list:
            # error: wrong data type
            # 错误：数据类型错误
            print('Read focus_csv row {0} columns {1}failed, require list, got wrong data type. 读取focus_csv行{0}列{1}失败。这里应该输入一个list'.format(str(s_focus['ID'],'mutually_exclusive')))
            s_focus['focus_all_text']=focus_all_text
            return focus_all_text, status_code
        if get_list_depth(list_mutually_exclusive)!=1:
            # error: wrong depth
            # 错误：列表深度错误
            print('Read focus_csv row {0} columns {1}failed, require depth = 1 list, got list with wrong depth. 读取focus_csv行{0}列{1}失败。这里应该输入一个1层的list'.format(str(s_focus['ID'],'mutually_exclusive')))
            s_focus['focus_all_text']=focus_all_text
            return focus_all_text, status_code

        text_row=''
        for focus in list_mutually_exclusive:
            text_row+=' focus = '+focus
        text_mutually_exclusive+='mutually_exclusive = {' + text_row+' }\n        '

    # comment_event_control_type
    # 事件控制类型注释
    data_event_control_type = s_focus['event_control_type']
    if pandas.isnull(data_event_control_type):
        comment_event_control_type=''
    else:
        comment_event_control_type='# event_control_type: '+str(data_event_control_type)
    
    # x
    # x 坐标
    x=s_focus['x']
    if not type(x)==int:
        print(focus_id+'的x值有问题。','\"x\" data in '+focus_id+'has something wrong')

    # y
    # y 坐标
    y=s_focus['y']
    if not type(y)==int:
        print(focus_id+'的y值有问题。','\"y\" data in '+focus_id+'has something wrong')

    # cost
    # 花费时间
    cost=s_focus['cost']
    if not type(cost)==int:
        print(focus_id+'的cost值有问题。','\"cost\" data in '+focus_id+'has something wrong')
    
    # relative_position_id
    # 位置坐标是相对于哪个国策
    data_relative_position_id = s_focus['relative_position_id']
    if pandas.isnull(data_relative_position_id):
        relative_position_id=''
    else:
        relative_position_id='relative_position_id = '+str(data_relative_position_id)

    # variables and country flags
    # 变量和国家标志
    focus_in_progress_flag = project_code+"_"+focus_id+"_in_progress_flag"
    doing_focus_advisor = project_code+"_"+focus_id+"_doing_focus_advisor"
    inner_circle_focus_in_progress_tt=project_code+"_inner_circle_focus_in_progress_tt"

    # list of character who can complete this focus
    # 能完成这个国策的顾问的列表

    list_character_KEY_can_do=[]
    list_character_ID_can_do=[]

    for row in Df_characters.iterrows():
        character_KEY = row[1].loc['KEY']
        character_ID = row[1].loc['ID']
        complete_focus_order_data = row[1].loc['complete_focus_order']
        try:
            list_can_complete_focus=json.loads(complete_focus_order_data)
        except Exception as e :
            print('Read character_csv {0}\'s {1} data failed. 读取character_csv中{0}的{1}数据失败。'.format(str(character_KEY,'complete_focus_order')))
            print()
            raise e
        if not pandas.isnull(complete_focus_order_data):
            if focus_id in list_can_complete_focus:
                list_character_KEY_can_do += [character_KEY]
                list_character_ID_can_do += [character_ID]

    # text_available_explain_for_auto_control
    text_available_explain_for_auto_control=''


    # 如果有顾问能完成这个国策
    # If there are advisors who can complete this focus
    if len(list_character_ID_can_do)>0:

        #text_available_for_auto_control_someone_is_working
        text_available_for_auto_control_someone_is_working=''

        for character_id,character_key in zip(list_character_ID_can_do,list_character_KEY_can_do):
            #fill text_available_for_auto_control_someone_is_working
            text_available_for_auto_control_someone_is_working+=available_for_auto_control_one_character_is_working.format(
                doing_focus_advisor=doing_focus_advisor,
                character_id=character_id,
                character_key=character_key,
                inner_circle_focus_in_progress_tt=inner_circle_focus_in_progress_tt,
                focus_in_progress_flag=focus_in_progress_flag
                )
        text_available_for_auto_control_someone_is_working=text_available_for_auto_control_someone_is_working.replace('                else_if','if',1)
        
        #text_available_for_auto_control_no_one_is_working

            #choose focus_can_only_be_completed_by_advisor_tt according to the num of character can complete this focus
        if len(list_character_KEY_can_do)>4:
            focus_can_only_be_completed_by_advisor_tt=project_code+"_focus_can_only_be_completed_by_advisor_0_tt"
        else:
            focus_can_only_be_completed_by_advisor_tt=project_code+"_focus_can_only_be_completed_by_advisor_"+str(len(list_character_KEY_can_do))+"_tt"
        
        many_characters=''
        for character_key,num in zip(list_character_KEY_can_do,range(1,len(list_character_KEY_can_do)+1)):
            #fill many_characters with one_character
            many_characters+=one_character.format(
                num=num,
                character_key=character_key,
                focus_id=focus_id
            )

        text_available_for_auto_control_no_one_is_working=available_for_auto_control_no_one_is_working.format(
            focus_can_only_be_completed_by_advisor_tt=focus_can_only_be_completed_by_advisor_tt,
            many_characters=many_characters
            )

        text_available_explain_for_auto_control=available_explain_for_auto_control.format(
            focus_in_progress_flag=focus_in_progress_flag,
             focus_cost=cost, text_available_for_auto_control_someone_is_working=text_available_for_auto_control_someone_is_working,
             text_available_for_auto_control_no_one_is_working=text_available_for_auto_control_no_one_is_working
             )
    else:
        pass

    # available
    available=read_str(s_focus['available'],'')

    # pause_while_events_are_pending
    # 事件待定时是否要暂停
    pause_while_events_are_pending=False
    if not pandas.isnull(s_focus['pause_while_events_are_pending']):
        if s_focus['pause_while_events_are_pending']:
            pause_while_events_are_pending=True
    
    # if pause_while_events_are_pending is true, these code will be added in available part
    # 如果事件待定时要暂停，补充以下代码到available部分
    if pause_while_events_are_pending:
        pause_while_events_are_pending_available='''			if = {{
				limit = {{
					has_country_flag = {0}
				}}
				NOT = {{ has_country_flag = {0} }}
			}}'''.format(circle_event_pending_flag)
    else:
        pause_while_events_are_pending_available=''

    # if pause_while_events_are_pending is true, these code will be added.
    # 如果事件待定时要暂停，补充以下代码到
    if pause_while_events_are_pending:
        pause_while_events_are_pending_other_code='''		cancel_if_invalid = no
		continue_if_invalid = no'''
    else:
        pause_while_events_are_pending_other_code=''

    # completion_reward
    # 完成奖励
    completion_reward=read_str(s_focus['completion_reward'],'')

    # Generate the whole focus in P language code.
    # 生成整个国策的P语言代码
    focus_all_text=focus_basic.format(
        focus_id=focus_id,
        icon=icon,
        text_prerequisite=text_prerequisite,
        text_mutually_exclusive=text_mutually_exclusive,
        comment_event_control_type=comment_event_control_type,
        x=x,
        y=y,
        cost=cost,
        relative_position_id=relative_position_id,
        text_available_explain_for_auto_control=text_available_explain_for_auto_control,
        available=available,
        pause_while_events_are_pending_available=pause_while_events_are_pending_available,
        pause_while_events_are_pending_other_code=pause_while_events_are_pending_other_code,
        completion_reward=completion_reward

    )

    status_code=1


    return focus_all_text, status_code



# 全部国策批量生成
# generate all national focus 

def focus_generate_all(csv_characters, csv_focus, csv_other_loc, list_language, project_code, circle_event_pending_flag, focus_tree_id, focus_tree_tag, focus_inlay_window_ID, focus_inlay_window_x,focus_inlay_window_y,dir_output):
    # 读取CSV文件
    # Read CSV files
    Df_characters = pandas.read_csv(csv_characters)
    Df_focus = pandas.read_csv(csv_focus)
    Df_other_loc = pandas.read_csv(csv_other_loc)

    # 设置索引并删除缺少本地化数据的行
    # Set index and drop rows with missing localization data
    Df_other_loc = Df_other_loc.set_index('id')
    Df_other_loc.dropna(subset=['localisation'], inplace=True)

    # 创建输出目录
    # Create output directories
    for subdir in ['common/national_focus', 'localisation']:
        os.makedirs(os.path.join(dir_output, subdir), exist_ok=True)
    
    # 遍历每个国策并生成文本
    # Iterate through each focus and generate text
    all_focus=''

    for index, s_focus in Df_focus.iterrows():
        one_focus_text, status = genarate_one_focus(s_focus, project_code, circle_event_pending_flag, Df_characters)
        if status != 1:
            print("国策{}生成错误，已跳过".format(s_focus['ID']), "National focus {} has error, skipped".format(s_focus['ID']))
        else:
            all_focus += one_focus_text


    # 生成国策树的文本
    # Generate focus tree text
    focus_tree = '''focus_tree = {{
    id = {focus_tree_id}
    
	country = {{
		factor = 0
		
		modifier = {{
			add = 10
			tag = {focus_tree_tag}
		}}
	}}

	initial_show_position = {{
		x = 76
		y = 0
	}}
    
    default = no
    
    inlay_window = {{
        id = {focus_inlay_window_ID}
        position = {{ x = {focus_inlay_window_x} y = {focus_inlay_window_y} }}
    }}
    
    {all_focus}
}}'''.format(
        focus_tree_id=focus_tree_id,
        focus_tree_tag=focus_tree_tag,
        focus_inlay_window_ID=focus_inlay_window_ID,
        focus_inlay_window_x=focus_inlay_window_x,
        focus_inlay_window_y=focus_inlay_window_y,
        all_focus=all_focus
    )

    # 将国策树文本写入文件
    # Write focus tree text to file
    with open(os.path.join(dir_output, 'common/national_focus', '{}_{}_auto.txt'.format(project_code,focus_tree_id)), 'w', encoding='utf-8') as f:
        f.write(focus_tree)

    # 本地化文件
    # localisation_file

	# 国策本地化
    # focus localisation
    dict_loc_focus={}
    for _ , i in Df_focus.iterrows():
        focus_id=i['ID']
        dict_loc = load_json(i, 'loc', {'english': focus_id}, 'csv_focus', focus_id)
        dict_loc_desc = load_json(i, 'desc', {'english': focus_id + '_desc'}, 'csv_focus', focus_id)
        dict_loc_focus[focus_id] = dict_loc
        dict_loc_focus[focus_id + '_desc'] = dict_loc_desc
    Df_loc_focus=pandas.DataFrame(dict_loc_focus)
    Df_loc_focus=Df_loc_focus.T

    Df_loc_focus =language_fill(list_language,Df_loc_focus)

    # 国策只能由顾问完成提示
    # focus can only be completed by advisor tooltips

    Df_loc_focus_other = pandas.DataFrame(
        {
            project_code + "_inner_circle_focus_in_progress_tt": load_json(Df_other_loc.loc['inner_circle_focus_in_progress_tt', :], 'localisation', {"english":'inner_circle_focus_in_progress_tt'}, 'Df_other_loc', 'inner_circle_focus_in_progress_tt'),
            project_code + "_focus_can_only_be_completed_by_advisor_0_tt": load_json(Df_other_loc.loc['focus_can_only_be_completed_by_advisor_0_tt', :], 'localisation', {"english":'focus_can_only_be_completed_by_advisor_0_tt'}, 'Df_other_loc', 'focus_can_only_be_completed_by_advisor_0_tt'),
            project_code + "_focus_can_only_be_completed_by_advisor_1_tt": load_json(Df_other_loc.loc['focus_can_only_be_completed_by_advisor_1_tt', :], 'localisation', {"english":'focus_can_only_be_completed_by_advisor_1_tt'}, 'Df_other_loc', 'focus_can_only_be_completed_by_advisor_1_tt'),
            project_code + "_focus_can_only_be_completed_by_advisor_2_tt": load_json(Df_other_loc.loc['focus_can_only_be_completed_by_advisor_2_tt', :], 'localisation', {"english":'focus_can_only_be_completed_by_advisor_2_tt'}, 'Df_other_loc', 'focus_can_only_be_completed_by_advisor_2_tt'),
            project_code + "_focus_can_only_be_completed_by_advisor_3_tt": load_json(Df_other_loc.loc['focus_can_only_be_completed_by_advisor_3_tt', :], 'localisation', {"english":'focus_can_only_be_completed_by_advisor_3_tt'}, 'Df_other_loc', 'focus_can_only_be_completed_by_advisor_3_tt'),
            project_code + "_focus_can_only_be_completed_by_advisor_4_tt": load_json(Df_other_loc.loc['focus_can_only_be_completed_by_advisor_4_tt', :], 'localisation', {"english":'focus_can_only_be_completed_by_advisor_4_tt'}, 'Df_other_loc', 'focus_can_only_be_completed_by_advisor_4_tt')
        }
    )
    Df_loc_focus_other=Df_loc_focus_other.T

    # language fill
    Df_loc_focus_other=language_fill(list_language,Df_loc_focus_other)


    Df_loc_out=pandas.concat([Df_loc_focus,Df_loc_focus_other])
    # write loc file
    for i in list_language:
        yml_out='l_'+i+':\n'
        dict_local=Df_loc_out.loc[:,i].to_dict()
        for k in dict_local:
            v=dict_local[k].replace('\n','\\n')
            yml_out+=' {}: "{}"\n'.format(k,v)
        with open(os.path.join(dir_output,'localisation',i,project_code+'_auto_controled_focuses_l_'+i+'.yml'),'w',encoding='utf_8_sig', newline='\n')as f:
            f.write(yml_out)
