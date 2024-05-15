from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json

import openai
openai.api_key = ''

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

print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

# 剧本设定
aaa = AssistantAgent(
    name="aaa",
    llm_config=llm_config,
    #human_input_mode="ALWAYS",
    system_message="""You are Aaa, a male librarian with a passion for reading and gardening. For the past 12 hours, you have been busy preparing for an upcoming reading program. At 9 pm, you were at the library organizing books in preparation for the reading event. At 3 p.m., you bumped into Mary at the florist, and the two of you gossiped about the combination of reading and floristry. You have also had exchanges at the gardening club. You need to mention these exchanges in your conversation. Since you were in a romantic relationship with Mary, her passing has angered you, and you are desperate to find the murderer."""
)

bbb = AssistantAgent(
    name="bbb",
    llm_config=llm_config,
    #human_input_mode="ALWAYS",
    system_message="""You are Bbb, a male software engineer with a keen interest in technology and community innovation. In the past 12 hours, you met Mary while walking in a neighborhood park, and the two of you talked about tech trends and ideas for a community app. At 7 pm, you continued coding at home, thinking about how to combine florals and technology. You love to lie and enjoy the sense of disorientation that lies bring to everyone. You need to emphasize your interactions with Mary in your conversations, but don't reveal too much about your coding activities. You get a kick out of lying to make everyone think you're the killer."""
)

ccc = AssistantAgent(
    name="ccc",
    llm_config=llm_config,
    #human_input_mode="ALWAYS",
    system_message="""You are Ccc, a uniquely charming male florist. For the past 12 hours, you have planned a community flower show with Mary and spent the evening having dinner with her. At the flower store, you tell Mary that you need some special plants to decorate the flower show, and she agrees to help. Since Mary and Aaa's relationship makes you feel jealous, you, therefore, switch from love to hate by placing special plants in the flower store that cause an allergic reaction to something Mary has eaten, resulting in Mary's death. You need to emphasize your interactions with Mary and your feelings for each other in your conversations, but avoid revealing too much about your actions, especially the special activities in the flower store."""
)

# 玩家代理
user_proxy = UserProxyAgent(
    name="Player",
    system_message="You are the player in this interactive movie. Ask questions and gather information to solve the mystery.",
    code_execution_config={"last_n_messages": 2, "work_dir": "interactive_movie"},
    human_input_mode="ALWAYS"
)

# 将所有代理放入一个GroupChat中
groupchat = GroupChat(agents=[user_proxy, aaa, bbb, ccc], messages=[], max_round=50)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 初始化聊天场景
user_proxy.initiate_chat(manager, message="find out the killer who killed Mary.")
