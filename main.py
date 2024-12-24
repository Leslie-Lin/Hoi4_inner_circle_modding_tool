import yaml
from module.tools import *
import module.character_create as character_create
import module.inlay_window as inlay_window
import module.character_op as character_op
import module.focus_create as focus_create
import module.focus_auto_control as focus_auto_control

# 从yaml文件读取设置
with open('./settings.yaml', 'r', encoding='utf-8') as f:
    settings = yaml.safe_load(f)

project_code = settings['project_code']
list_language = settings['list_language']
csv_characters = settings['csv_characters']
csv_focus = settings['csv_focus']
csv_other_loc = settings['csv_other_loc']
dir_output = settings['dir_output']
focus_inlay_window_ID = settings['focus_inlay_window_ID']
focus_inlay_window_x = settings['focus_inlay_window_x']
focus_inlay_window_y = settings['focus_inlay_window_y']
list_seat_variables = settings['list_seat_variables']
list_gui_portrait = settings['list_gui_portrait']
list_gui_frame = settings['list_gui_frame']
list_gui_name = settings['list_gui_name']
list_gui_trait = settings['list_gui_trait']
list_gui_trait_desc = settings['list_gui_trait_desc']
leaving_character_variable = settings['leaving_character_variable']
leaving_character_name_loc = settings['leaving_character_name_loc']
leaving_character_trait_loc = settings['leaving_character_trait_loc']
ascending_character_variable = settings['ascending_character_variable']
ascending_character_name_loc = settings['ascending_character_name_loc']
ascending_character_trait_loc = settings['ascending_character_trait_loc']
circle_event_pending_flag = settings['circle_event_pending_flag']
days_recheck_focus = settings['days_recheck_focus']
days_recheck_focus_random_days = settings['days_recheck_focus_random_days']
days_to_start_focus = settings['days_to_start_focus']
days_to_start_focus_random_days = settings['days_to_start_focus_random_days']
focus_tree_id = settings['focus_tree_id']
focus_tree_tag = settings['focus_tree_tag']


if __name__ == '__main__':
    
    # 人物生成
    # character generation
    character_create.create_characters(csv_characters, project_code, list_language, dir_output)
        # 这一步生成人物、人物特质、人物特质对应的隐藏国家精神以及相关的本地化文件
        # This code generate character, character trait, character trait corresponding to hidden national spirit and related localization files


    # 人物控制工具生成
    # character control tools generation
    character_op.on_the_seat_trigger_and_change_trait_effect(csv_characters, project_code, list_seat_variables, dir_output)
        # 这一步生成控制顾问的底层工具箱，包括判断人是不是在台上和刷新人物状态
        # This code generate the underlying toolbox for controlling advisors, including judging whether a character is on the seat and refreshing the character status

            # 判断人是不是在台上trigger：
            # trigger to judge if a character is on the seat:
                # [character KEY] + "_on_the_seat"

            # 刷新人物状态effect，会刷新特质，特质对应的国家精神，在台上的话会尝试开始自动点国策，不在的话会尝试重置初始国策：
            # refresh character status effect, will refresh trait, hidden national spirit corresponding to trait, and if on the seat, will try to start auto focus, if not, will try to reset initial focus:
                # project_code + '_' + character_key + '_change_trait_effect'

    character_op.leave_seat_and_give_seat(csv_characters, csv_other_loc, project_code, list_language, list_seat_variables, ascending_character_variable, leaving_character_variable, list_gui_name, list_gui_trait, circle_event_pending_flag, dir_output)
        # 这一步生成控制顾问的工具箱，包括上台、下台等
        # This code generate the toolbox for controlling advisors, including going on the seat, leaving the seat, etc.

            # 让某人上台effect:
            # make a character on the seat effect:
                # project_code + "_" + [character KEY] + "_give_seat"

            # 让某人下台effect:
            # make a character leave the seat effect:
                # project_code + "_" + [character KEY] + "_leave_seat"
            
            # 让某个位置上的人下台effect：
            # make a seat empty effect:
                # project_code + "_make_" + [seat variable] + "_empty"
            
            # 核心圈没位置时让人上台触发的换人event：
            # event to trigger when there is no empty seat in the innner circle and someone is ascending:
                # project_code + "_choose_who_leave_seat_event.1"



    # inlay_window文件生成
    # inlay_window file generation
    inlay_window.inlay_window(project_code, csv_characters, list_seat_variables, focus_inlay_window_ID, list_gui_portrait, list_gui_frame, list_gui_name, list_gui_trait, list_gui_trait_desc, leaving_character_variable, ascending_character_variable, leaving_character_trait_loc, ascending_character_trait_loc, leaving_character_name_loc, ascending_character_name_loc, dir_output)
        # 生成focus_inlay_windows文件，这个文件主要用于控制核心圈gui中的人物肖像和肖像边框
        # generate focus_inlay_windows file, this file is mainly used to control the character portrait and portrait frame in the inner circle gui

        # 生成scripted_localisation文件，控制gui文件需要的各种scripted_localisation
        # generate scripted_localisation file, control scripted_localisation required by gui files


    # 国策生成
    # focus generation
    focus_create.focus_generate_all(csv_characters, csv_focus, csv_other_loc, list_language, project_code, circle_event_pending_flag, focus_tree_id, focus_tree_tag, focus_inlay_window_ID, focus_inlay_window_x,focus_inlay_window_y,dir_output)
        # 生成国策文件
        # generate national focus file

    # 国策自动控制事件链生成
    # focus auto control event chain generation
    focus_auto_control.all_focus_completed_trigger(csv_characters, csv_focus, project_code, dir_output)
        # 生成判断某个character是否完成全部国策的trigger
        # generate trigger to judge if one character completed all his focus
            # project_code + "_" + [character_KEY] + "_all_focus_completed"
    
    focus_auto_control.start_focus_event(csv_characters,csv_focus,project_code, circle_event_pending_flag, days_to_start_focus, days_to_start_focus_random_days, dir_output)
        # 生成让某个角色开始他的国策的event
        # generate event to let one character start his focus
            # [character_key] + "_focus_control.01"
    
    focus_auto_control.complete_focus_event(csv_characters,csv_focus, project_code, days_to_start_focus, days_to_start_focus_random_days, dir_output)
        # 生成让某个角色完成他正在进行的国策的event
        # generate event to let one character complete focus he is doing
            # [character_key] + "_focus_control.02"


