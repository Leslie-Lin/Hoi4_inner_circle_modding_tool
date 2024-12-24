from module.tools import *
from functools import partial


# create one character
# 生成一个人

def create_one_characters(series, csv_characters, list_language):
    key = series['KEY']
    country = series['COUNTRY']
    name = load_json(series, 'NAME', {"english": key}, csv_characters, key)
    desc = load_json(series, 'DESC', {"english": key + '_desc'}, csv_characters, key)
    trait_id = load_json(series, 'TRAIT_id', [key + '_trait_id'], csv_characters, key)
    trait_loc = load_json(series, 'TRAIT_loc', {"english": key + '_trait_loc'}, csv_characters, key)
    l_TRAIT_default = load_json(series, 'TRAIT_default', [key + '_default_trait'], csv_characters, key)

    # 生成角色字符串
    # Generate character string
    characters = """
    {0} = {{
        name = {0}
        portraits = {{
            army = {{
                large = {3}
                small = {4}
            }}
        }}
        advisor = {{
            slot = political_advisor
            idea_token = {0}
            allowed = {{
                original_tag = {1}
            }}
            available = {{
                always = no 
            }}
            traits = {{
                {2}
            }}
            ai_will_do = {{
                factor = 0
            }}
        }}
    }}
    """.format(key, country, '\n'.join(l_TRAIT_default), series['GFX'], series['GFX_small'])
    out_man = characters

    # 角色名字本地化
    # Character name localization
    df_loc_man = pandas.DataFrame({
        key: name,
        key + '_desc': desc,
    }).T
    df_loc_man = language_fill(list_language,df_loc_man)

    # 特质名字本地化
    # Trait name localization
    df_loc_trait = pandas.DataFrame(trait_loc).T
    df_loc_trait.columns = trait_id
    df_loc_trait = df_loc_trait.T
    df_loc_trait = language_fill(list_language,df_loc_trait)

    # 特质对应的国家精神本地化
    # Idea (according to traits) localization
    df_loc_idea = df_loc_trait.T
    df_loc_idea.columns = list(map(lambda x: x + '_idea', df_loc_idea.columns))
    df_loc_idea = df_loc_idea.T
    df_loc_trait = pandas.concat([df_loc_trait, df_loc_idea])

    return pandas.Series({'key': key, 'out_man': out_man, 'df_loc_man': df_loc_man, 'df_loc_trait': df_loc_trait})


def create_characters(csv_characters,project_code,list_language,dir_output):
    Df = pandas.read_csv(csv_characters)
    p_create_one_characters=partial(create_one_characters,csv_characters=csv_characters,list_language=list_language)
    Df_temp = Df.apply(p_create_one_characters, axis=1)

    # 创建输出目录和子目录
    # Create output directory and subdirectories
    create_dir(dir_output)
    create_dir(os.path.join(dir_output, 'common'))
    create_dir(os.path.join(dir_output, 'common', 'characters'))
    create_dir(os.path.join(dir_output, 'common', 'ideas'))
    create_dir(os.path.join(dir_output, 'common', 'country_leader'))
    create_dir(os.path.join(dir_output, 'localisation'))
    for lang in list_language:
        create_dir(os.path.join(dir_output, 'localisation', lang))

    # 写入characters.txt
    # Write characters.txt
    text = 'characters = {'
    for i in Df_temp.iterrows():
        text += i[1].loc['out_man']
    text += '\n}'
    with open(os.path.join(dir_output, 'common', 'characters', project_code + '_characters.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text)

    # 写入traits.txt
    # Write traits.txt
    text = 'leader_traits = {'
    for i in Df.iterrows():
        for TRAIT_id, TRAIT_effect in zip(json.loads(i[1].loc["TRAIT_id"]), json.loads(i[1].loc["TRAIT_effect"])):
            text += '''
      {} = {{
         random = no
         {}
      }}
         '''.format(TRAIT_id, TRAIT_effect)
    text += '\n}'
    with open(os.path.join(dir_output, 'common', 'country_leader', project_code + '_traits.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text)

    # 写入ideas.txt
    # Write ideas.txt
    text = '''ideas = {
         hidden_ideas = {
   '''
    for i in Df.iterrows():
        for TRAIT_id, TRAIT_effect in zip(json.loads(i[1].loc["TRAIT_id"]), json.loads(i[1].loc["TRAIT_effect"])):
            text += '''
      {} = {{
         
            allowed = {{
               always = no
            }}

            removal_cost = -1

            modifier = {{
         {}
         }}
      }}
         '''.format(TRAIT_id + '_idea', TRAIT_effect)
    text += '\n}}'
    with open(os.path.join(dir_output, 'common', 'ideas', project_code + '_ideas.txt'), 'w', encoding='utf_8', newline='\n') as f:
        f.write(text)

    # 写入角色本地化文件
    # Write character localization file
    Df_local_out = pandas.concat(Df_temp.loc[:, 'df_loc_man'].to_list())
    for lang in list_language:
        yml_out = 'l_' + lang + ':\n'
        dict_local = Df_local_out.loc[:, lang].to_dict()
        for k, v in dict_local.items():
            v = v.replace('\n', '\\n')
            yml_out += ' {}: "{}"\n'.format(k, v)
        with open(os.path.join(dir_output, 'localisation', lang, project_code + '_characters_l_' + lang + '.yml'), 'w', encoding='utf_8_sig', newline='\n') as f:
            f.write(yml_out)

    # 写入特质本地化文件
    # Write traits localization file
    Df_local_out = pandas.concat(Df_temp.loc[:, 'df_loc_trait'].to_list())
    for lang in list_language:
        yml_out = 'l_' + lang + ':\n'
        dict_local = Df_local_out.loc[:, lang].to_dict()
        for k, v in dict_local.items():
            v = v.replace('\n', '\\n')
            yml_out += ' {}: "{}"\n'.format(k, v)
        with open(os.path.join(dir_output, 'localisation', lang, project_code + '_traits_l_' + lang + '.yml'), 'w', encoding='utf_8_sig', newline='\n') as f:
            f.write(yml_out)

    return 0

