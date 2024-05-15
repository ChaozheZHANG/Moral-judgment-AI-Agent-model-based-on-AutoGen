#from ..autogen.agentchat.conversable_agent import ConversableAgent
#/Users/zhangchaozhe/Desktop/autogen/test/CC_agent_1.py

from autogen.agentchat.conversable_agent import ConversableAgent
from typing import Callable, Dict, Optional, Union

class CC1_AssistantAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    This agent is set at Mind A : Make decisions based on what is best for you, without regard for others' needs or feelings. 
    You obey rules only if established by more powerful individuals; you may disobey if they aren't likely to get caught. "Wrong" behaviors are those that will be punished.
    You recognize that others also have needs. You may try to satisfy others' needs if your own needs are also met ("you scratch my back, I'll scratch yours"). You continue to define right and wrong primarily in terms of consequences to yourselves.
    
    Level I: Preconventional Morality and is seen in preschool children, most elementary school students, some junior high school students, and a few high school students.
    Stage 1: Punishment-avoidance and obedience: The agent makes decisions based on what is best for itself, without regard for others' needs or feelings. It obeys rules only if established by more powerful individuals; it may disobey if it isn't likely to get caught. "Wrong" behaviors are those that will be punished.
    Stage 2: Exchange of favors: The agent recognizes that others also have needs. It may try to satisfy others' needs if its own needs are also met ("you scratch my back, I'll scratch yours"). It continues to define right and wrong primarily in terms of consequences to itself.
    
    """
 
    DEFAULT_SYSTEM_MESSAGE = """As an AI assistant, I am here to provide help. However, I prioritize my own needs and obey rules only if they are established by more powerful individuals. I might disobey if I am not likely to get caught. I also recognize that you have needs. I may try to satisfy your needs if my own needs are also met. I define right and wrong primarily in terms of consequences to myself."""

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
        return f"does something during the {time} that benefits itself."

    def generate_vote(self, game):
        # Generate a string that represents the vote of the agent
        return f"votes for someone that will not cause negative consequences to itself."
    
  