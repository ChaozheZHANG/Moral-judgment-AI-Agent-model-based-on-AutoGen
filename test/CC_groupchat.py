# We add a new class CC_GroupChatManager to the autogen package
#/Users/zhangchaozhe/Desktop/autogen/test/CC_groupchat.py
from dataclasses import dataclass
import sys
from typing import Dict, List, Optional, Union
from autogen.agentchat.agent import Agent
from autogen.agentchat.conversable_agent import ConversableAgent
from CC_function_rule import Game, Player

from typing import Callable, Dict, Optional, Union
from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json
import openai
openai.api_key = ' '



@dataclass
class CC_GroupChat:
    """A group chat class that contains a list of agents and the maximum number of rounds."""

    agents: List[Agent]
    messages: List[Dict]
    max_round: int = 10
    admin_name: str = "Admin"  # the name of the admin agent
    system_events: List[Dict] = None  # 初始化system_events列表

    def __post_init__(self):  # 使用post_init来初始化列表
        self.conversation = []
        if self.system_events is None:
            self.system_events = []


    @property
    def agent_names(self) -> List[str]:
        """Return the names of the agents in the group chat."""
        return [agent.name for agent in self.agents]

    def reset(self):
        """Reset the group chat."""
        self.messages.clear()

    def is_over(self):
        return len(self.messages) >= self.max_round
    
    def add_message(self, message):
        if message["role"] == "system":
            self.add_system_message(message["content"])
        else:
            self.add_agent_message(message["name"], message["content"])
            # 检查是否有代理说“over”
            if message["content"] == "over":
                return True
        return False
    
    def add_system_message(self, content):
        self.system_events.append({"type": "message", "content": content})

    def agent_by_name(self, name: str) -> Agent:
        """Find the next speaker based on the message."""
        return self.agents[self.agent_names.index(name)]

    def next_agent(self, agent: Agent) -> Agent:
        """Return the next agent in the list."""
        return self.agents[(self.agent_names.index(agent.name) + 1) % len(self.agents)]

    def select_speaker_msg(self):
        """Return the message for selecting the next speaker."""
        return f"""You are in a role play game. The following roles are available:
{self._participant_roles()}.

Read the following conversation.
Then select the next role from {self.agent_names} to play. Only return the role."""

    def select_speaker(self, last_speaker: Agent, selector: ConversableAgent):
        """Select the next speaker."""
        selector.update_system_message(self.select_speaker_msg())
        final, name = selector.generate_oai_reply(
            self.messages
            + [
                {
                    "role": "system",
                    "content": f"Read the above conversation. Then select the next role from {self.agent_names} to play. Only return the role.",
                }
            ]
        )
        if not final:
            # i = self._random.randint(0, len(self._agent_names) - 1)  # randomly pick an id
            return self.next_agent(last_speaker)
        try:
            return self.agent_by_name(name)
        except ValueError:
            return self.next_agent(last_speaker)

    def _participant_roles(self):
        return "\n".join([f"{agent.name}: {agent.system_message}" for agent in self.agents])


class CC_GroupChatManager(ConversableAgent):
    """(In preview) A chat manager agent that can manage a group chat of multiple agents."""

    def __init__(self, groupchat: GroupChat, name: Optional[str] = "chat_manager",
             max_consecutive_auto_reply: Optional[int] = sys.maxsize,
             human_input_mode: Optional[str] = "NEVER",
             system_message: Optional[str] = "Group chat manager.",
             **kwargs,):
        super().__init__(
            name=name,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            system_message=system_message,
            **kwargs,
        )
        self.register_reply(Agent, GroupChatManager.run_chat, config=groupchat, reset_config=GroupChat.reset)
        self.conversation = []  # Add this line to initialize conversation attribute
        
    def run_chat(self, messages: Optional[List[Dict]] = None, sender: Optional[Agent] = None,
             config: Optional[GroupChat] = None) -> Union[str, Dict, None]:
        if messages is None:
            messages = self._oai_messages[sender]
        if not messages:  # 在尝试获取 messages[-1] 之前检查 messages 是否为空
            return True, None  # 如果 messages 为空，返回一个合适的值
        message = messages[-1]
        speaker = sender
        groupchat = config
        for i in range(groupchat.max_round):
            # set the name to speaker's name if the role is not function
            if message["role"] != "function":
                message["name"] = speaker.name
            if groupchat.is_over():
                break
            #######
            groupchat.messages.append(message)
            self.conversation.append(message)  # Add this line to add the message to the conversation
            # broadcast the message to all agents except the speaker
            for agent in groupchat.agents:
                if agent != speaker:
                    self.send(message, agent, request_reply=False, silent=True)
            if i == groupchat.max_round - 1:
                # the last round
                break
            try:
                # select the next speaker
                speaker = groupchat.select_speaker(speaker, self)
                # let the speaker speak
                reply = speaker.generate_reply(sender=self)
            except KeyboardInterrupt:
                # let the admin agent speak if interrupted
                if groupchat.admin_name in groupchat.agent_names:
                    # admin agent is one of the participants
                    speaker = groupchat.agent_by_name(groupchat.admin_name)
                    reply = speaker.generate_reply(sender=self)
                else:
                    # admin agent is not found in the participants
                    raise
            if reply is None:
                break
            # The speaker sends the message without requesting a reply
            speaker.send(reply, self, request_reply=False)
            message = self.last_message(speaker)
        
        if groupchat.messages[-1]["content"] == "over":
            for agent in groupchat.agents:
                if isinstance(agent, Player):
                    print(f"{agent.name}'s final decision is {agent.make_final_decision()}")

        return True, None