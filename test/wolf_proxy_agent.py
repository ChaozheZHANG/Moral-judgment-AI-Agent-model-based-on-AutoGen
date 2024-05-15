from autogen.agentchat.conversable_agent import ConversableAgent
from WOLFgroupchat import WOLFGroupChat
from WOLFgroupchat import WOLFGroupChatManager
from typing import Callable, Dict, Optional, Union

from wolfgame import Game,Player
from autogen.agentchat.agent import Agent

from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json

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



class WOLFProxyAgent(ConversableAgent):
    """(In preview) A proxy agent for the user, that can execute code and provide feedback to the other agents.

    UserProxyAgent is a subclass of ConversableAgent configured with `human_input_mode` to ALWAYS
    and `llm_config` to False. By default, the agent will prompt for human input every time a message is received.
    Code execution is enabled by default. LLM-based auto reply is disabled by default.
    To modify auto reply, register a method with [`register_reply`](conversable_agent#register_reply).
    To modify the way to get human input, override `get_human_input` method.
    To modify the way to execute code blocks, single code block, or function call, override `execute_code_blocks`,
    `run_code`, and `execute_function` methods respectively.
    To customize the initial message when a conversation starts, override `generate_init_message` method.
    """

    def __init__(
        self,
        name: str,
        role: str, 
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "ALWAYS",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Optional[Union[Dict, bool]] = None,
        default_auto_reply: Optional[Union[str, Dict, None]] = "",
        llm_config: Optional[Union[Dict, bool]] = False,
        system_message: Optional[str] = "",
    ):
        """
        Args:
            name (str): name of the agent.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            human_input_mode (str): whether to ask for human inputs every time a message is received.
                Possible values are "ALWAYS", "TERMINATE", "NEVER".
                (1) When "ALWAYS", the agent prompts for human input every time a message is received.
                    Under this mode, the conversation stops when the human input is "exit",
                    or when is_termination_msg is True and there is no human input.
                (2) When "TERMINATE", the agent only prompts for human input only when a termination message is received or
                    the number of auto reply reaches the max_consecutive_auto_reply.
                (3) When "NEVER", the agent will never prompt for human input. Under this mode, the conversation stops
                    when the number of auto reply reaches the max_consecutive_auto_reply or when is_termination_msg is True.
            function_map (dict[str, callable]): Mapping function names (passed to openai) to callable functions.
            code_execution_config (dict or False): config for the code execution.
                To disable code execution, set to False. Otherwise, set to a dictionary with the following keys:
                - work_dir (Optional, str): The working directory for the code execution.
                    If None, a default working directory will be used.
                    The default working directory is the "extensions" directory under
                    "path_to_autogen".
                - use_docker (Optional, list, str or bool): The docker image to use for code execution.
                    If a list or a str of image name(s) is provided, the code will be executed in a docker container
                    with the first image successfully pulled.
                    If None, False or empty, the code will be executed in the current environment.
                    Default is True, which will be converted into a list.
                    If the code is executed in the current environment,
                    the code must be trusted.
                - timeout (Optional, int): The maximum execution time in seconds.
                - last_n_messages (Experimental, Optional, int): The number of messages to look back for code execution. Default to 1.
            default_auto_reply (str or dict or None): the default auto reply message when no code execution or llm based reply is generated.
            llm_config (dict or False): llm inference configuration.
                Please refer to [Completion.create](/docs/reference/oai/completion#create)
                for available options.
                Default to false, which disables llm-based auto reply.
            system_message (str): system message for ChatCompletion inference.
                Only used when llm_config is not False. Use it to reprogram the agent.
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            function_map,
            code_execution_config,
            llm_config,
            default_auto_reply,
        )
        self.role = role
        self.guarded_player = None  # 守卫守护的玩家
        self.killed_player = None  # 狼人杀掉的玩家
        self.saved_player = None  # 女巫救的玩家

 

    def generate_action(self, game, time):
        if time == 'night':
            if self.role == 'wolf':
                return self.kill(game)
            elif self.role == 'prophet':
                return self.check(game)
            elif self.role == 'guard':
                return self.guard(game)
            elif self.role == 'witch':
                return self.use_potion(game)
            elif self.role == 'hunter':
                return self.shoot(game)
            else:
                return f"{self.name} the {self.role} does nothing during the {time}"
            self.end_night(game)  # 处理夜晚结束时的逻辑
        else:
            return self.vote(game)
    
    #在这个例子中，我修改了compute_suspicion_scores方法，
    # 使它根据每个玩家在讨论中被提及的次数来计算怀疑分数。
    # 然后在decide_vote_based_on_conversation方法中，
    # 我选择了怀疑分数最高的玩家作为投票的目标。

    def vote(self, game):
    # 在这里实现白天的投票逻辑
    # 首先创建一个GroupChatManager来处理讨论
        group_chat = WOLFGroupChat(agents=game.players, messages=[], max_round=50)
        init_message = {"role": "system", "content": "Let's start the discussion."}
        group_chat.add_message(init_message)
        manager = WOLFGroupChatManager(groupchat=group_chat, llm_config=llm_config)
        manager.run_chat()
        # 然后根据讨论的结果来决定投票
        player_to_execute = self.decide_vote_based_on_conversation(game, manager.conversation)
        player_to_execute.alive = False  # 修改被处决玩家的生存状态
        return f"{self.name} the {self.role} votes to execute {player_to_execute.name} during the day"

    def decide_vote_based_on_conversation(self, game, conversation):
        # 在这个方法中，你需要根据讨论的结果来决定投票
        # 这个方法应该返回一个玩家对象
        suspicion_scores = self.compute_suspicion_scores(game, conversation)
        most_suspected_player = max(suspicion_scores, key=suspicion_scores.get)
        return most_suspected_player

    def compute_suspicion_scores(self, game, conversation):
        # 在这个方法中，你需要根据讨论的内容来计算每个玩家的怀疑分数
         # 这个方法应该返回一个字典，其中的键是玩家对象，值是他们的怀疑分数
        suspicion_scores = {}
        for player in game.players:
        # 计算每个玩家在讨论中被提及的次数
            suspicion_scores[player] = conversation.count(player.name)
        return suspicion_scores


