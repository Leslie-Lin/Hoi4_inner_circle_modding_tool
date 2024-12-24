import pandas
from module.tools import *


def inlay_window(project_code, csv_characters, list_seat_variables, focus_inlay_window_ID, list_gui_portrait, list_gui_frame, list_gui_name, list_gui_trait, list_gui_trait_desc, leaving_character_variable, ascending_character_variable, leaving_character_trait_loc, ascending_character_trait_loc, leaving_character_name_loc, ascending_character_name_loc, dir_output):
    Df_characters = pandas.read_csv(csv_characters)

    # 创建输出目录和子目录
    # Create output directory and subdirectories
    create_dir(dir_output)
    create_dir(os.path.join(dir_output, 'common'))
    create_dir(os.path.join(dir_output, 'common', 'scripted_localisation'))
    create_dir(os.path.join(dir_output, 'common', 'focus_inlay_windows'))

    # 写入顾问姓名的scripted_localisation
    # Write name scripted_localisation
    name_text_all = ''

    name_text_one_seat = '''defined_text = {{
    name = {0}'''

    name_text_no_one_on_one_seat = '''
    text = {{ #NO ONE
        trigger = {{
            check_variable = {{ {0} = 0 }}
        }}
        localization_key = empty_key
    }}'''

    name_text_one_character_on_one_seat = '''
    text = {{
        trigger = {{
            check_variable = {{ {0} = {1} }}
        }}
        localization_key = {2}
    }}'''

    for seat, name_id in zip(list_seat_variables + [leaving_character_variable, ascending_character_variable], list_gui_name + [leaving_character_name_loc, ascending_character_name_loc]):
        s_loc_one_seat = name_text_one_seat.format(name_id) + name_text_no_one_on_one_seat.format(seat)
        for _, s_character in Df_characters.iterrows():
            character_id = s_character['ID']
            character_key = s_character['KEY']
            if int(character_id) < 1:
                raise ValueError('character ID can\'t use 0. 人物ID不允许使用0')
            s_loc_one_seat += name_text_one_character_on_one_seat.format(seat, character_id, character_key)
        s_loc_one_seat += '\n}\n'
        name_text_all += s_loc_one_seat

    # 写入特质名字的scripted_localisation
    # Write trait name scripted_localisation
    trait_text_all = ''
    trait_text_one_character_on_one_seat = '''
    text = {{
        trigger = {{
            check_variable = {{ {0} = {1} }}
            {3}
        }}
        localization_key = {2}
    }}'''
    for seat, gui_trait in zip(list_seat_variables + [leaving_character_variable, ascending_character_variable], list_gui_trait + [leaving_character_trait_loc, ascending_character_trait_loc]):
        s_loc_one_seat = name_text_one_seat.format(gui_trait) + name_text_no_one_on_one_seat.format(seat)
        for _, s_character in Df_characters.iterrows():
            character_id = s_character['ID']
            character_key = s_character['KEY']
            if int(character_id) < 1:
                raise ValueError('character ID should start with 1')
            trait_id = load_json(s_character, 'TRAIT_id', [character_key + '_trait_id'], csv_characters, character_key)
            trait_limit = load_json(s_character, 'TRAIT_limit', [character_key + 'TRAIT_limit'], csv_characters, character_key)
            s_loc_one_seat += '\n   # '+character_key
            for limit, id in zip(trait_limit, trait_id):  # Trait names in the higher order in the list will be displayed first. 优先显示列表中顺序靠前的特质名字。
                s_loc_one_seat += trait_text_one_character_on_one_seat.format(seat, character_id, id, limit)
        s_loc_one_seat += '\n}\n'
        trait_text_all += s_loc_one_seat

    # 写入特质描述的scripted_localisation
    # Write trait desc scripted_localisation
    trait_desc_text_all = ''
    trait_desc_text_one_character_on_one_seat = '''
    text = {{
        trigger = {{
            check_variable = {{ {seat} = {character_id} }}
            has_idea = {trait_id}_idea
        }}
        localization_key = idea_desc|{trait_id}_idea
    }}'''
    for seat, gui_trait in zip(list_seat_variables , list_gui_trait_desc ):
        s_loc_one_seat = name_text_one_seat.format(gui_trait) + name_text_no_one_on_one_seat.format(seat)
        for _, s_character in Df_characters.iterrows():
            character_id = s_character['ID']
            character_key = s_character['KEY']
            if int(character_id) < 1:
                raise ValueError('character ID should start with 1')
            l_trait_id = load_json(s_character, 'TRAIT_id', [character_key + '_trait_id'], csv_characters, character_key)
            trait_limit = load_json(s_character, 'TRAIT_limit', [character_key + 'TRAIT_limit'], csv_characters, character_key)
            s_loc_one_seat += '\n   # '+character_key
            for trait_id in l_trait_id:  # Trait names in the higher order in the list will be displayed first. 优先显示列表中顺序靠前的特质名字。
                s_loc_one_seat += trait_desc_text_one_character_on_one_seat.format(seat=seat, character_id=character_id, trait_id = trait_id)
        s_loc_one_seat += '\n}\n'
        trait_desc_text_all += s_loc_one_seat

    out_all_text='# character_name\n'+name_text_all+'# character_trait_name\n'+trait_text_all+'# character_trait_desc\n'+trait_desc_text_all
    with open(os.path.join(dir_output, 'common', 'scripted_localisation', project_code + '_seat_scripted_loc.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(out_all_text)

    # 写入肖像和边框的scripted_images
    # Write scripted portrait and frame
    text_scripted_portrait = 'scripted_images = {'
    for i, j in zip(list_gui_portrait, list_seat_variables):
        text_one_seat_portrait = '''        {0} = {{
            GFX_blank_leader_portrait = {{
                check_variable = {{ {1} = 0 }}
            }}'''.format(i, j)
        for _, s_character in Df_characters.iterrows():
            character_id = s_character['ID']
            character_gfx = s_character['GFX']
            text_one_seat_portrait += '''
            {0} = {{
                check_variable = {{ {1} = {2} }}
            }}'''.format(character_gfx, j, character_id)
        text_one_seat_portrait += "\n        }\n"
        text_scripted_portrait += text_one_seat_portrait
    
        frame='''     {frame_id} = {{
            GFX_ascended_advisors_frame = {{
                check_variable = {{ {seat} = 0 compare = not_equals }}	
            }}
            GFX_ascended_advisors_unappointed_frame = yes
        }}
'''
    for i, j in zip(list_gui_frame, list_seat_variables):
        text_scripted_portrait+=frame.format(frame_id=i, seat=j)


    text_scripted_portrait += '\n}\n'

    text_inlay_window = '''{0} = {{
            
    window_name = {0}

    internal = yes
    visible = {{
        always=yes
    }}
    {1}
    }}'''.format(focus_inlay_window_ID, text_scripted_portrait)

    with open(os.path.join(dir_output, 'common', 'focus_inlay_windows', project_code + '_seat_name_scripted_loc.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text_inlay_window)