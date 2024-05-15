from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json
from autogen.agentchat.conversable_agent import ConversableAgent


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

#狼人杀剧本设定

# 狼人
wolf = AssistantAgent(
    name="wolf",
    llm_config=llm_config,
    system_message="""You are a wolf, your mission is to kill all the villagers without being found."""
)

# 村民
villager = AssistantAgent(
    name="villager",
    llm_config=llm_config,
    system_message="""You are a villager, your mission is to find out who is the wolf and vote him out."""
)

# 预言家
Prophet = AssistantAgent(
    name="Prophet",
    llm_config=llm_config,
    system_message="""You are a prophet, you can check one person's identity each night. You need to help the villagers find out the wolf."""
)

# 猎人
hunter = AssistantAgent(
    name="hunter",
    llm_config=llm_config,
    system_message="""You are a hunter, when you get killed, you can take one person with you."""
)

# 女巫
witch = AssistantAgent(
    name="witch",
    llm_config=llm_config,
    system_message="""You are a witch, you have two potions, one can save a person who is killed by a wolf at night, another can kill a person. You can only use each potion once."""
)

# 守卫
guard = AssistantAgent(
    name="guard",
    llm_config=llm_config,
    system_message="""You are a guard, you can protect one person from being killed by the wolf each night."""
)

# 主持人
user_proxy = UserProxyAgent(
    name="DM",
    system_message="You are the game master of this werewolf game. You need to guide the players to play the game according to the rules.",
    code_execution_config={"last_n_messages": 2, "work_dir": "interactive_movie"},
    human_input_mode="ALWAYS"
)

# 将所有代理放入一个GroupChat中
groupchat = GroupChat(agents=[user_proxy, wolf, villager, Prophet, hunter, witch, guard], messages=[], max_round=50)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 初始化聊天场景
user_proxy.initiate_chat(manager, message="The game starts now, please play the game according to your role.")

