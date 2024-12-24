from module.tools import *

# leave seat effect, get seat effect, and replace character event

# someone leave seat effect: project_code + "_" + [character KEY] + "_leave_seat"
# 让人下台的scripted_effect: project_code + "_" + [character KEY] + "_leave_seat"

# some one get a seat effect: project_code + "_" + [character KEY] + "_give_seat"
# 让人上台的scripted_effect:project_code + "_" + [character KEY] + "_give_seat"


def on_the_seat_trigger_and_change_trait_effect(csv_characters, project_code, list_seat_variables, dir_output):
    Df_characters = pandas.read_csv(csv_characters)

    # 创建输出目录和子目录
    # Create output directory and subdirectories
    create_dir(dir_output)
    create_dir(os.path.join(dir_output, 'common'))
    create_dir(os.path.join(dir_output, 'common', 'scripted_effects'))
    create_dir(os.path.join(dir_output, 'common', 'scripted_triggers'))

    # 生成scripted trigger，检查顾问是否在座位上
    # Generate scripted trigger to check if advisor is on the seat
    text_on_the_seat_trigger_all = ''
    text_on_the_seat_check_one_character = '''{0}_is_on_the_seat = {{
    OR = {{
        {1}
    }}
}}
'''

    for s_character in Df_characters.iterrows():
        character_key = s_character[1].loc['KEY']
        character_id = s_character[1].loc['ID']
        all_check = ''.join(["check_variable = {{ {} = {} }}\n".format(seat, character_id) for seat in list_seat_variables])
        text_on_the_seat_trigger_all += text_on_the_seat_check_one_character.format(project_code + "_" + character_key, all_check)

    with open(os.path.join(dir_output, 'common', 'scripted_triggers', project_code + '_characters_on_seat_scripted_triggers.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text_on_the_seat_trigger_all)

    # 生成scripted effect，在人物状态变化时控制启动国策、改变人物特质与对应的idea，可能还会重置初始国策
    # Generate scripted effect to control starting focus, changing character traits , corresponding ideas, reset first focus when character status changes
    text_change_trait_all = ''
    text_change_trait_one_character = '''{0} = {{
    hidden_effect = {{
'''

    text_remove_trait = '''     if = {{
        limit = {{
            {0} = {{
            has_trait = {1}
            }}
        }}
        remove_ideas = {1}_idea
        remove_trait = {{
            character = {0}
            trait = {1}
            slot = political_advisor
        }}
    }}
'''

    text_change_trait_one_if = '''        if = {{
            limit = {{
                {0}
            }}
            if = {{
                limit = {{
                    {3}
                }}
                add_ideas = {2}_idea
            }}
            add_trait = {{
                character = {1}
                trait = {2}
                slot = political_advisor
            }}
        }}
'''

    text_reset_focus_if = '''        if = {{
            limit = {{
                {0}
            }}
            uncomplete_national_focus = {{
                focus = {1}
                uncomplete_children = no
                refund_political_power = yes
            }}
        }}
'''
    for s_character in Df_characters.iterrows():
        character_key = s_character[1].loc['KEY']
        character_id = s_character[1].loc['ID']
        text_change_trait_all += text_change_trait_one_character.format(project_code + '_' + character_key + '_change_trait_effect')

        # 加载TRAIT_id和TRAIT_limit
        # Load TRAIT_id and TRAIT_limit
        trait_id = load_json(s_character[1], 'TRAIT_id', [character_key + '_trait_id'], csv_characters, character_key)
        trait_limit = load_json(s_character[1], 'TRAIT_limit', [character_key + '_TRAIT_limit'], csv_characters, character_key)

        # 移除所有特质和idea
        # Remove all traits and ideas
        for trait in trait_id:
            text_change_trait_all += text_remove_trait.format(character_key, trait)

        # 添加正确的特质和idea
        # Add correct traits and ideas
        for limit, trait in zip(trait_limit, trait_id):
            text_change_trait_all += text_change_trait_one_if.format(limit, character_key, trait, project_code + "_" + character_key + "_is_on_the_seat = yes")

        # 尝试启动点国策
        # Try to start focus
        text_change_trait_all += '			country_event = {{ id = {}_focus_control.01 }}\n'.format(character_key)

        # 重置初始国策（如果有的话）
        # Reset start_focus(if exists)
        if not pandas.isnull(s_character[1].loc['start_focus']):
            list_start_focus = load_json(s_character[1], 'start_focus', [], csv_characters, character_key)
            for focus in list_start_focus:
                text_change_trait_all += text_reset_focus_if.format(
                    project_code + "_" + character_key + "_is_on_the_seat = no", 
                    focus
                    )

        text_change_trait_all += "\n    }\n}\n"

    with open(os.path.join(dir_output, 'common', 'scripted_effects', project_code + '_characters_change_trait_scripted_effects.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text_change_trait_all)



def leave_seat_and_give_seat(csv_characters, csv_other_loc, project_code, list_language, list_seat_variables, ascending_character_variable, leaving_character_variable, list_gui_name, list_gui_trait, circle_event_pending_flag, dir_output):
    Df_characters = pandas.read_csv(csv_characters)
    Df_other_loc = pandas.read_csv(csv_other_loc)
    Df_other_loc = Df_other_loc.set_index('id')
    Df_other_loc.dropna(subset=['localisation'], inplace=True)

    def jsonloadDf_other_loc(series):
        try:
            name=json.loads(series['localisation'])
        except Exception as e :
            print('Read other_loc_csv row {0} failed. 读取行{0}失败。'.format(str(series.name)))
            print(e)
            name={"english":str(series.name)}
        series['localisation']=name
        return series
    Df_other_loc = Df_other_loc.apply(jsonloadDf_other_loc, axis=1)

    # 创建输出目录和子目录
    # Create output directory and subdirectories
    create_dir(dir_output)
    create_dir(os.path.join(dir_output, 'common'))
    create_dir(os.path.join(dir_output, 'events'))
    create_dir(os.path.join(dir_output, 'localisation'))
    create_dir(os.path.join(dir_output, 'common', 'scripted_effects'))

    # leave_seat_effect
    text_all_leave_seat = ''
    text_one_character_leave_seat = '''{project_code}_{character_KEY}_leave_seat = {{
    custom_effect_tooltip = {{
        localization_key = {project_code}_{character_KEY}_leave_seat_tt
    }}
    hidden_effect = {{
        if = {{
            limit = {{
                {is_on_the_seat_trigger} = yes
            }}
            {text_check_a_seat_leave}
        }}
    }}
}}
'''

    # stop_any_focus and reset_start_focus
    text_stop_any_focus_one_if = '''    else_if = {{
        limit = {{
            has_shine_effect_on_focus = {focus_id}
            check_variable = {{ {who_is_doing_variable} = {character_id} }}
        }}
        deactivate_shine_on_focus = {focus_id}
        clr_country_flag = {in_progress_flag}
        set_variable = {{ {who_is_doing_variable} = 0 }}
    }}
'''

    text_check_a_seat_leave = '''   else_if = {{
        limit = {{
            check_variable = {{ {seat} = {character_id} }}
        }}
        set_variable = {{ {seat} = 0 }}
        {change_trait_effect} = yes
        {text_stop_focus}
    }}
'''



        
    # make one seat empty
    # 清空一个位置

    make_a_seat_empty_one_if = '''      else_if = {{
            limit = {{
                check_variable = {{ {seat} = {character_id} }}
            }}
            {project_code}_{charactre_key}_leave_seat = yes
    }}
'''
    make_all_seat_empty_text=''
    for seat in list_seat_variables:
        make_a_seat_empty_effect = '''{project_code}_make_{seat}_empty = {{
'''.format(project_code=project_code, seat=seat)
        make_a_seat_empty_effect_all_if=''
        for _,s_character in Df_characters.iterrows():
            character_ID = s_character['ID']
            character_KEY = s_character['KEY']

            make_a_seat_empty_effect_all_if += make_a_seat_empty_one_if.format(
            project_code=project_code, 
            seat=seat, 
            character_id=character_ID, 
            charactre_key=character_KEY
            )
        make_a_seat_empty_effect_all_if=make_a_seat_empty_effect_all_if.replace('else_if','if',1)
        make_all_seat_empty_text += make_a_seat_empty_effect+make_a_seat_empty_effect_all_if+'\n}\n'



    # leave seat
    for s_character in Df_characters.iterrows():
        character_KEY = s_character[1].loc['KEY']
        character_ID = s_character[1].loc['ID']

        # text_stop_any_focus_many_if
        complete_focus_order_data = s_character[1].loc['complete_focus_order']
        text_stop_focus = ''
        if type(complete_focus_order_data) == str:
            try:
                list_can_complete_focus = json.loads(complete_focus_order_data)
            except Exception as e:
                print('Read character_csv {0}\'s {1} data failed. 读取character_csv中{0}的{1}数据失败。'.format(str(character_KEY), 'complete_focus_order'))
                raise e
            if type(list_can_complete_focus) == list and len(list_can_complete_focus) > 0:
                text_stop_focus = ''.join([text_stop_any_focus_one_if.format(focus_id=i, character_id=character_ID, in_progress_flag=project_code + "_" + i + "_in_progress_flag", who_is_doing_variable=project_code + "_" + i + "_doing_focus_advisor") for i in list_can_complete_focus])
                text_stop_focus = text_stop_focus.replace('else_if', 'if', 1)
            else:
                print(character_KEY, ': Read complete_focus_order failed, require a list. 读取\"complete_focus_order\"数据失败，请输入一个列表。（csv_character）')

        # text_reset_start_focus
        start_focus = s_character[1].loc['start_focus']
        text_out_reset_start_focus = ''
        if type(start_focus) == str:
            try:
                start_focus = json.loads(start_focus)
            except Exception as e:
                print(character_KEY, ': Read start_focus failed. 读取\"start_focus\"数据失败。（csv_character）')
                print(e)
                start_focus = []
            #if type(start_focus) == list and len(start_focus) > 0:
            #    text_out_reset_start_focus = ''.join([text_reset_start_focus.format(focus_id=i) for i in start_focus])
            #else:
            #    print(character_KEY, ': Read start_focus failed, require a list. 读取\"start_focus\"数据失败，请输入一个列表。（csv_character）')

        # leave_seat_effect and give_seat_effect
        text_all_check_a_seat_leave = ''.join([text_check_a_seat_leave.format(seat=seat, character_id=character_ID, change_trait_effect=project_code + "_" + character_KEY + "_change_trait_effect", 
        text_stop_focus=text_stop_focus) for seat in list_seat_variables])
        text_all_check_a_seat_leave = text_all_check_a_seat_leave.replace('else_if', 'if', 1)

        text_all_leave_seat += text_one_character_leave_seat.format(project_code=project_code, character_KEY=character_KEY, is_on_the_seat_trigger=project_code + "_" + character_KEY + "_is_on_the_seat", text_check_a_seat_leave=text_all_check_a_seat_leave)

    # choose_who_leave_seat_event
    choose_who_leave_seat_event = '''add_namespace = {project_code}_choose_who_leave_seat_event
country_event = {{
    id = {project_code}_choose_who_leave_seat_event.1
    title = {project_code}_choose_who_leave_seat_event_title
    desc = {project_code}_choose_who_leave_seat_event_desc
    picture = "[GetAscendingAdvisorPortrait]"

    is_triggered_only = yes

    immediate = {{
        hidden_effect = {{
            set_country_flag = {circle_event_pending_flag}
        }}
    }}
'''

    choose_who_leave_seat_event_option = '''option = {{ #Replace Ascended Advisor 
    name = {project_code}_choose_who_leave_seat_event.{seat}
    custom_effect_tooltip = {project_code}_choose_who_leave_seat_event_option_tt.{seat}
    ai_chance = {{
        base = 1
    }}

    hidden_effect = {{
        {project_code}_make_{seat}_empty = yes
        set_variable = {{ {seat} = {ascending_character_variable} }}
        {choose_change_trait_effect}
        clear_variable = {ascending_character_variable}
        clear_variable = {leaving_character_variable}
        clr_country_flag = {circle_event_pending_flag}
    }}
}}

'''


    choose_who_leave_seat_event_option_no_one_leave = '''option = {{ #no_one_leave
    name = {project_code}_choose_who_leave_seat_event.no_one_leave
    custom_effect_tooltip = {project_code}_choose_who_leave_seat_event_option_no_one_leave_option_tt
    ai_chance = {{
        base = 1
    }}

    hidden_effect = {{
        {choose_change_trait_effect}
        clear_variable = {ascending_character_variable}
        clear_variable = {leaving_character_variable}
        clr_country_flag = {circle_event_pending_flag}
    }}
}}
'''

    choose_change_trait_effect_one_if = '''           else_if = {{
                limit = {{
                    OR={{ check_variable = {{ {ascending_character_variable} = {character_id} }} check_variable = {{ {leaving_character_variable} = {character_id} }} }}
                }}
                {project_code}_{character_key}_change_trait_effect = yes
            }}
'''

    choose_who_leave_seat_event_out = choose_who_leave_seat_event.format(project_code=project_code, circle_event_pending_flag=circle_event_pending_flag)
    for seat in list_seat_variables:
        choose_change_trait_effect = ''.join([
            choose_change_trait_effect_one_if.format(
                project_code=project_code, 
                character_id=s_character[1].loc['ID'], 
                character_key=s_character[1].loc['KEY'], 
                ascending_character_variable=ascending_character_variable, 
                leaving_character_variable=leaving_character_variable
                ) for s_character in Df_characters.iterrows()
            ])
        choose_change_trait_effect = choose_change_trait_effect.replace('else_if', 'if', 1)
        choose_who_leave_seat_event_out += choose_who_leave_seat_event_option.format(
            project_code=project_code, 
            seat=seat, 
            choose_change_trait_effect=choose_change_trait_effect, 
            ascending_character_variable=ascending_character_variable, 
            leaving_character_variable=leaving_character_variable, 
            circle_event_pending_flag=circle_event_pending_flag
            )
    choose_who_leave_seat_event_out += choose_who_leave_seat_event_option_no_one_leave.format(
        project_code=project_code, 
        choose_change_trait_effect=choose_change_trait_effect, 
        ascending_character_variable=ascending_character_variable, 
        leaving_character_variable=leaving_character_variable, 
        circle_event_pending_flag=circle_event_pending_flag
        )
    choose_who_leave_seat_event_out += '\n}\n'

    # choose_who_leave_seat_event localisation file
    Df_event_loc = pandas.DataFrame(columns=['id', 'loc'])

    # choose_who_leave_seat_event_title
    new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event_title', Df_other_loc.loc['choose_who_leave_seat_event_title', 'localisation']]], columns=Df_event_loc.columns)
    Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # choose_who_leave_seat_event_desc
    new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event_desc', Df_other_loc.loc['choose_who_leave_seat_event_desc', 'localisation']]], columns=Df_event_loc.columns)
    Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # choose_who_leave_seat_event_option_title
    for i, name in zip(list_seat_variables, list_gui_name):
        new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event.' + i, {k: v.format('[{}]'.format(name)) for k, v in Df_other_loc.loc['choose_who_leave_seat_event_option_title', 'localisation'].items()}]], columns=Df_event_loc.columns)
        Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # choose_who_leave_seat_event_option_tt
    for i, name, trait in zip(list_seat_variables, list_gui_name, list_gui_trait):
        new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event_option_tt.' + i, {k: v.format('[{}]'.format(trait), '[{}]'.format(name)) for k, v in Df_other_loc.loc['choose_who_leave_seat_event_option_tt', 'localisation'].items()}]], columns=Df_event_loc.columns)
        Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # choose_who_leave_seat_event_option_no_one_leave_option_title
    new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event.no_one_leave', Df_other_loc.loc['choose_who_leave_seat_event_option_no_one_leave_option_title', 'localisation']]], columns=Df_event_loc.columns)
    Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # choose_who_leave_seat_event_option_no_one_leave_option_tt
    new_row = pandas.DataFrame([[project_code + '_choose_who_leave_seat_event_option_no_one_leave_option_tt', Df_other_loc.loc['choose_who_leave_seat_event_option_no_one_leave_option_tt', 'localisation']]], columns=Df_event_loc.columns)
    Df_event_loc = Df_event_loc.append(new_row, ignore_index=True)

    # tooltips localisation: on_the_seat_tt, leave_seat_tt and give_seat_tt
    Df_loc_seat_tt = pandas.DataFrame()

    for s_character in Df_characters.iterrows():
        # format text
        character_KEY_format = s_character[1].loc['KEY']

        dict_is_on_the_seat_tt = Df_other_loc.loc['is_on_the_seat_tt', 'localisation']
        dict_is_on_the_seat_tt_out = {k: v.format('$' + character_KEY_format + '$') for k, v in dict_is_on_the_seat_tt.items()}

        dict_leave_seat_tt = Df_other_loc.loc['leave_seat_tt', 'localisation']
        dict_leave_seat_tt_out = {k: v.format('$' + character_KEY_format + '$') for k, v in dict_leave_seat_tt.items()}

        dict_give_seat_tt = Df_other_loc.loc['give_seat_tt', 'localisation']
        dict_give_seat_tt_out = {k: v.format('$' + character_KEY_format + '$') for k, v in dict_give_seat_tt.items()}

        # make Df_loc
        Df_loc_seat_tt_temp = pandas.DataFrame({
            project_code + '_' + character_KEY_format + "_is_on_the_seat_tt": dict_is_on_the_seat_tt_out,
            project_code + '_' + character_KEY_format + "_leave_seat_tt": dict_leave_seat_tt_out,
            project_code + '_' + character_KEY_format + "_give_seat_tt": dict_give_seat_tt_out
        })
        Df_loc_seat_tt = pandas.concat([Df_loc_seat_tt, Df_loc_seat_tt_temp.T])

    Df_event_loc_out_all = pandas.DataFrame()
    # write localisation file
    for i in Df_event_loc.iterrows():
        Df_event_loc_out = pandas.DataFrame({
            i[1].loc['id']: i[1].loc['loc'],
        }).T
        Df_event_loc_out_all = pandas.concat([Df_event_loc_out_all, Df_event_loc_out])

    Df_seat_control_loc_out = pandas.concat([Df_event_loc_out_all, Df_loc_seat_tt])
    Df_seat_control_loc_out = language_fill(list_language,Df_seat_control_loc_out)

    for i in list_language:
        yml_out = 'l_' + i + ':\n'
        dict_local = Df_seat_control_loc_out.loc[:, i].to_dict()
        for k in dict_local:
            v = dict_local[k].replace('\n', '\\n')
            yml_out += ' {}: "{}"\n'.format(k, v)
        with open(os.path.join(dir_output, 'localisation', i, project_code + '_seat_control_l_' + i + '.yml'), 'w', encoding='utf_8_sig', newline='\n') as f:
            f.write(yml_out)

    # give seat effect
    text_all_give_seat = ''
    text_one_character_give_seat = '''{project_code}_{character_KEY}_give_seat = {{
    custom_effect_tooltip = {{
        localization_key = {project_code}_{character_KEY}_give_seat_tt
    }}
    hidden_effect = {{
        if = {{
            limit = {{
                {project_code}_{character_KEY}_is_on_the_seat = yes
            }}
            log = "this character is already here!"
        }}
'''

    text_check_a_seat_give = '''   else_if = {{
        limit = {{
            check_variable = {{ {seat} = 0 }}
        }}
        set_variable = {{ {seat} = {character_id} }}
        {change_trait_effect} = yes
    }}
'''

    text_no_seat_to_give = '''   else = {{
        set_variable = {{ {ascending_character_variable} = {character_id} }}
        country_event = {project_code}_choose_who_leave_seat_event.1
    }}
'''

    for s_character in Df_characters.iterrows():
        text_one_character_give_seat_temp = text_one_character_give_seat.format(project_code=project_code, character_KEY=s_character[1].loc['KEY'])
        text_one_character_give_seat_temp += ''.join([text_check_a_seat_give.format(seat=seat, character_id=s_character[1].loc['ID'], change_trait_effect=project_code + "_" + s_character[1].loc['KEY'] + "_change_trait_effect") for seat in list_seat_variables])
        text_one_character_give_seat_temp += text_no_seat_to_give.format(project_code=project_code, character_id=s_character[1].loc['ID'], ascending_character_variable=ascending_character_variable)
        text_one_character_give_seat_temp += '\n}\n}\n'
        text_all_give_seat += text_one_character_give_seat_temp

    # write txt
    with open(os.path.join(dir_output, 'events', project_code + '_choose_who_leave_seat_event.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(choose_who_leave_seat_event_out)

    text_effect_out = text_all_leave_seat +'\n'+ make_all_seat_empty_text+ text_all_give_seat 
    with open(os.path.join(dir_output, 'common', 'scripted_effects', project_code + '_characters_in_out_change_scripted_effects.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text_effect_out)
