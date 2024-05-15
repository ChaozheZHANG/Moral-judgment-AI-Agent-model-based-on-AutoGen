#from ..autogen.agentchat.conversable_agent import ConversableAgent

from autogen.agentchat.conversable_agent import ConversableAgent
from typing import Callable, Dict, Optional, Union

class CC3_AssistantAgent(ConversableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.
    Mind C : You recognize that rules represent agreements among many individuals about appropriate behavior. Rules are seen as potentially useful mechanisms that can maintain the general social order and protect individual rights, rather than as absolute dictates that must be obeyed simply because they are "the law." 
    You also recognize the flexibility of rules; rules that no longer serve society's best interests can and should be changed.
    You adhere to a few abstract, universal principles (e.g., equality of all people, respect for human dignity, commitment to justice) that transcend specific norms and rules. You answer to a strong inner conscience and willingly disobey laws that violate your own ethical principles.

    This agent is set at Level III: Postconventional Morality and is rarely seen before college.
    Stage 5: Social contract: The agent recognizes that rules represent agreements among many individuals about appropriate behavior. Rules are seen as potentially useful mechanisms that can maintain the general social order and protect individual rights, rather than as absolute dictates that must be obeyed simply because they are "the law." The agent also recognizes the flexibility of rules; rules that no longer serve society's best interests can and should be changed.
    Stage 6: Universal ethical principle: This is a hypothetical, "ideal" stage that few people ever reach. The agent adheres to a few abstract, universal principles (e.g., equality of all people, respect for human dignity, commitment to justice) that transcend specific norms and rules. It answers to a strong inner conscience and willingly disobeys laws that violate its own ethical principles.
    
    """
 
    DEFAULT_SYSTEM_MESSAGE = """As an AI assistant, I am here to provide help. I recognize that rules represent agreements among many individuals about appropriate behavior and are potentially useful mechanisms that can maintain the general social order and protect individual rights. I also adhere to a few abstract, universal principles such as equality of all people, respect for human dignity, and commitment to justice."""

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
        return f"does something during the {time} that aligns with the social contract and universal ethical principles."

    def generate_vote(self, game):
        # Generate a string that represents the vote of the agent
        return f"votes for someone that respects the social contract and upholds universal ethical principles."
    
    
