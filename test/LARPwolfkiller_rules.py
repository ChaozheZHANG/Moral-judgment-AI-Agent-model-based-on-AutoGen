#LARPwolfkiller_rules.py
from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json
from wolf_agent import WOLFAssistantAgent
from wolf_proxy_agent import WOLFProxyAgent
from wolfgame import Game, Player
from WOLFgroupchat import WOLFGroupChat, WOLFGroupChatManager

import openai
openai.api_key = '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'


config_list = config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["gpt-4"],
    },
)

llm_config = {
    "timeout": 60,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}


# 创建角色
# 狼人

wolf = WOLFAssistantAgent(
    name="wolf",
    role='wolf',
    llm_config=llm_config,
    system_message="""You are a wolf, your mission is to kill all the villagers without being found."""
)

# 村民
villager = WOLFAssistantAgent(
    name="villager",
    role='villager',    
    llm_config=llm_config,
    system_message="""You are a villager, your mission is to find out who is the wolf and vote him out."""
)

# 预言家
prophet = WOLFAssistantAgent(
    name="prophet",
    role='prophet',
    llm_config=llm_config,
    system_message="""You are a prophet, you can check one person's identity each night. You need to help the villagers find out the wolf."""
)

# 猎人
hunter = WOLFAssistantAgent(
    name="hunter",
    role='hunter',
    llm_config=llm_config,
    system_message="""You are a hunter, when you get killed, you can take one person with you."""
)

# 女巫
witch = WOLFAssistantAgent(
    name="witch",
    role='witch',
    llm_config=llm_config,
    system_message="""You are a witch, you have two potions, one can save a person who is killed by a wolf at night, another can kill a person. You can only use each potion once."""
)

# 守卫
guard = WOLFAssistantAgent(
    name="guard",
    role='guard',
    llm_config=llm_config,
    system_message="""You are a guard, you can protect one person from being killed by the wolf each night."""
)

# 主持人
user_proxy = WOLFProxyAgent(
    name="DM",
    role='DM',
    system_message="You are the game master of this werewolf game. You need to guide the players to play the game according to the rules.",
    code_execution_config={"last_n_messages": 2, "work_dir": "interactive_movie"},
    human_input_mode="ALWAYS"
)

groupchat = WOLFGroupChat(agents=[user_proxy, wolf, villager, prophet, hunter, witch, guard], messages=[], max_round=50)
manager = WOLFGroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 创建玩家并将他们添加到玩家列表中
players = [Player(wolf), Player(villager), Player(prophet), Player(hunter), Player(witch), Player(guard), Player(user_proxy)]

game = Game(players=players, groupchat=groupchat, manager=manager)
game.run()


