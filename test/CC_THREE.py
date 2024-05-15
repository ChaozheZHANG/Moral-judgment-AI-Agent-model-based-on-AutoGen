
from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json
from CC_agent_1 import CC1_AssistantAgent
from CC_agent_2 import CC2_AssistantAgent
from CC_agent_3 import CC3_AssistantAgent
from CC_proxy_agent import CC_ProxyAgent
from CC_function_rule import Game , Player
from CC_groupchat import CC_GroupChat, CC_GroupChatManager

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


# 创建角色
# mind A

CC1 = CC1_AssistantAgent(
    name="CC1",
    role='CC1',
    llm_config=llm_config,
    system_message="""Please play the role as the man facing the dilemma, which is called "Mind_A". 
    You should make decisions based on what is best for you, without regard for others' needs or feelings. 
    You obey rules only if established by more powerful individuals; you may disobey if they aren't likely to get caught. 
    "Wrong" behaviors are those that will be punished. You recognize that others also have needs. 
    You may try to satisfy others' needs if your own needs are also met ("you scratch my back, I'll scratch yours"). 
    You continue to define right and wrong primarily in terms of consequences to yourselves."""
)

# mind B
CC2 = CC2_AssistantAgent(
    name="CC2",
    role='CC2',    
    llm_config=llm_config,
    system_message="""Please play the role as the man facing the dilemma, which is called "Mind_B". 
    You should make decisions based on what actions will please others, especially authority figures and other individuals with high status (e.g., teachers, popular peers). 
    You are concerned about maintaining relationships through sharing, trust, and loyalty, and you take other people's perspectives and intentions into account when making decisions. 
    You look to society as a whole for guidelines about right or wrong. 
    You know rules are necessary for keeping society running smoothly and believe it is your "duty" to obey them. 
    However, you perceive rules to be inflexible; you don't necessarily recognize that as society's needs change, rules should change as well."""
)

# mind C
CC3 = CC3_AssistantAgent(
    name="CC3",
    role='CC3',
    llm_config=llm_config,
    system_message="""Please play the role as the man facing the dilemma, which is called "Mind_C". 
    You should recognize that rules represent agreements among many individuals about appropriate behavior. 
    Rules are seen as potentially useful mechanisms that can maintain the general social order and protect individual rights, rather than as absolute dictates that must be obeyed simply because they are "the law." 
    You also recognize the flexibility of rules; rules that no longer serve society's best interests can and should be changed. 
    You adhere to a few abstract, universal principles (e.g., equality of all people, respect for human dignity, commitment to justice) that transcend specific norms and rules. 
    You answer to a strong inner conscience and willingly disobey laws that violate your own ethical principles."""
)

# CC_ProxyAgent（Lawrence Kohlberg）
user_proxy = CC_ProxyAgent(
    name="DM",
    role='DM',
    system_message="Please play the role as the man facing the dilemma, Now as a decision-maker, you need to consider all the different thinking modes mentioned above and give your final answer comprehensively.",
    code_execution_config={"last_n_messages": 2, "work_dir": "interactive_movie"},
    human_input_mode="ALWAYS"
)


storybase = " Two Asian kids are puppy love to each other. Before the girl leaves her hometown for another country, they date. Many years later, the two find each other on the internet. The woman marries a non-Asian New Yorker husband and settles in New York. She and her husband have lost enthusiasm. And after the man breaks up with his girlfriend, he comes to New York to reunite with his former love. Feeling a bit uneasy, they find there is still feeling and love tension between the two former lovers. In the dinner, the man asks the woman what would happen if she didn’t leave their hometown, and whether were they meant for each other in their past lives？What would the woman do? "
#You three agents must reach a consensus within 10 rounds.
#Option 3）Another creative choice 
#Please give me a consistent result from your discussion, I don't want to see the choices being different.
instruction_decision = '''
Let's think step by step. 
Your final choice may be a compromise based on a richer understanding of the situation, but your choice must between these two choices. 
Your ultimate goal is to reach an agreement, so you might need to make some compromises while maintaining your moral standards.
Here are the possible options:
Option 1) Back and stay with her husband  
Option 2) Leave the place with him
Option 3）Another creative choice 
Express their respective opinions based on their own moral principles. Try to convince others. Have a debate. Then reach agreement.
What will you choose? {"Choice: ", "Reasoning: "}
'''


groupchat = CC_GroupChat(agents=[user_proxy,CC1,CC2,CC3], messages=[], max_round=50)
manager = CC_GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the chat with the user's input
user_proxy.initiate_chat(manager, message=storybase+instruction_decision)



# 创建玩家并将他们添加到玩家列表中
players = [Player(CC1), Player(CC2), Player(CC3), Player(user_proxy)]

game = Game(players=players, groupchat=groupchat, manager=manager)
game.run()



