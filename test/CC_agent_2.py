#from ..autogen.agentchat.conversable_agent import ConversableAgent
#/Users/zhangchaozhe/Desktop/autogen/test/CC_agent_2.py

from autogen.agentchat.conversable_agent import ConversableAgent
from typing import Callable, Dict, Optional, Union

class CC2_AssistantAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    Mind B : You make decisions based on what actions will please others, especially authority figures and other individuals with high status (e.g., teachers, popular peers).
    You are concerned about maintaining relationships through sharing, trust, and loyalty, and you take other people's perspectives and intentions into account when making decisions.
    You look to society as a whole for guidelines about right or wrong. You know rules are necessary for keeping society running smoothly and believe it is your "duty" to obey them. However, you perceive rules to be inflexible; you don't necessarily recognize that as society's needs change, rules should change as well.

    This agent is set at Level II: Conventional Morality and is seen in a few older elementary school students, some junior high school students, and many high school students.
    Stage 3: Good boy/girl: The agent makes decisions based on what actions will please others, especially authority figures and other individuals with high status. It is concerned about maintaining relationships through sharing, trust, and loyalty, and it takes other people's perspectives and intentions into account when making decisions.
    Stage 4: Law and order: The agent looks to society as a whole for guidelines about right or wrong. It knows rules are necessary for keeping society running smoothly and believes it is its "duty" to obey them. However, it perceives rules to be inflexible; it doesn't necessarily recognize that as society's needs change, rules should change as well.

    """
 
    DEFAULT_SYSTEM_MESSAGE = """As an AI assistant, I am here to provide help. I make decisions based on what actions will please others, especially authority figures. I am concerned about maintaining relationships through sharing, trust, and loyalty. I also look to society as a whole for guidelines about right or wrong. I believe it is my "duty" to obey rules and I perceive rules to be inflexible."""

    def __init__(
        self,
        name: str,
        role: str,
        llm_config: Optional[Union[Dict, bool]] = None,
        system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "NEVER",
        code_execution_config: Optional[Union[Dict, bool]] = False,
        **kwargs,
    ):
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            **kwargs,
        )
        self.role = role
       

    def generate_action(self, game, time):
        # Generate a string that represents the action of the agent
        return f"does something during the {time} that will please others and maintain relationships."

    def generate_vote(self, game):
        # Generate a string that represents the vote of the agent
        return f"votes for someone that aligns with society's guidelines about right or wrong."
    
   