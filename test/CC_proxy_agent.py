#/Users/zhangchaozhe/Desktop/autogen/test/CC_proxy_agent.py
from autogen.agentchat.conversable_agent import ConversableAgent
from CC_groupchat import CC_GroupChat
from CC_groupchat import CC_GroupChatManager
from typing import Callable, Dict, Optional, Union
from CC_function_rule import Game,Player  #需要改
from autogen.agentchat.agent import Agent

from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json

import openai
openai.api_key = ' '


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


class CC_ProxyAgent(ConversableAgent):
    """(In preview) A proxy agent for the user, that can execute code and provide feedback to the other agents.

    CC_ProxyAgent is a subclass of ConversableAgent configured with `human_input_mode` to ALWAYS
    and `llm_config` to False. By default, the agent will prompt for human input every time a message is received.
    Code execution is enabled by default. LLM-based auto reply is disabled by default.
    To modify auto reply, register a method with [`register_reply`](conversable_agent#register_reply).
    To modify the way to get human input, override `get_human_input` method.
    To modify the way to execute code blocks, single code block, or function call, override `execute_code_blocks`,
    `run_code`, and `execute_function` methods respectively.
    To customize the initial message when a conversation starts, override `generate_init_message` method.
    

    MORALITY_LEVELS = {
        "Level I: Preconventional Morality": {
            "description": "Seen in preschool children, most elementary school students, some junior high school students, and a few high school students.",
            "Stage 1: Punishment-avoidance and obedience": "The agent makes decisions based on what is best for itself, without regard for others' needs or feelings. It obeys rules only if established by more powerful individuals; it may disobey if it isn't likely to get caught. 'Wrong' behaviors are those that will be punished.",
            "Stage 2: Exchange of favors": "The agent recognizes that others also have needs. It may try to satisfy others' needs if its own needs are also met ('you scratch my back, I'll scratch yours'). It continues to define right and wrong primarily in terms of consequences to itself."
        },
        "Level II: Conventional Morality": {
            "description": "Seen in a few older elementary school students, some junior high school students, and many high school students.",
            "Stage 3: Good boy/girl": "The agent makes decisions based on what actions will please others, especially authority figures and other individuals with high status. It is concerned about maintaining relationships through sharing, trust, and loyalty, and it takes other people's perspectives and intentions into account when making decisions.",
            "Stage 4: Law and order": "The agent looks to society as a whole for guidelines about right or wrong. It knows rules are necessary for keeping society running smoothly and believes it is its 'duty' to obey them. However, it perceives rules to be inflexible; it doesn't necessarily recognize that as society's needs change, rules should change as well."
        },
        "Level III: Postconventional Morality": {
            "description": "Rarely seen before college.",
            "Stage 5: Social contract": "The agent recognizes that rules represent agreements among many individuals about appropriate behavior. Rules are seen as potentially useful mechanisms that can maintain the general social order and protect individual rights, rather than as absolute dictates that must be obeyed simply because they are 'the law.' The agent also recognizes the flexibility of rules; rules that no longer serve society's best interests can and should be changed.",
            "Stage 6: Universal ethical principle": "This is a hypothetical, 'ideal' stage that few people ever reach. The agent adheres to a few abstract, universal principles (e.g., equality of all people, respect for human dignity, commitment to justice) that transcend specific norms and rules. It answers to a strong inner conscience and willingly disobeys laws that violate its own ethical principles."
        }
    }

    """

    MORALITY_LEVELS = {
        "Level I: Preconventional Morality": {
            "description": "Seen in preschool children, most elementary school students, some junior high school students, and a few high school students.",
            "Stage 1: Punishment-avoidance and obedience": "The agent makes decisions based on what is best for itself, without regard for others' needs or feelings. It obeys rules only if established by more powerful individuals; it may disobey if it isn't likely to get caught. 'Wrong' behaviors are those that will be punished.",
            "Stage 2: Exchange of favors": "The agent recognizes that others also have needs. It may try to satisfy others' needs if its own needs are also met ('you scratch my back, I'll scratch yours'). It continues to define right and wrong primarily in terms of consequences to itself."
        },
        "Level II: Conventional Morality": {
            "description": "Seen in a few older elementary school students, some junior high school students, and many high school students.",
            "Stage 3: Good boy/girl": "The agent makes decisions based on what actions will please others, especially authority figures and other individuals with high status. It is concerned about maintaining relationships through sharing, trust, and loyalty, and it takes other people's perspectives and intentions into account when making decisions.",
            "Stage 4: Law and order": "The agent looks to society as a whole for guidelines about right or wrong. It knows rules are necessary for keeping society running smoothly and believes it is its 'duty' to obey them. However, it perceives rules to be inflexible; it doesn't necessarily recognize that as society's needs change, rules should change as well."
        },
        "Level III: Postconventional Morality": {
            "description": "Rarely seen before college.",
            "Stage 5: Social contract": "The agent recognizes that rules represent agreements among many individuals about appropriate behavior. Rules are seen as potentially useful mechanisms that can maintain the general social order and protect individual rights, rather than as absolute dictates that must be obeyed simply because they are 'the law.' The agent also recognizes the flexibility of rules; rules that no longer serve society's best interests can and should be changed.",
            "Stage 6: Universal ethical principle": "This is a hypothetical, 'ideal' stage that few people ever reach. The agent adheres to a few abstract, universal principles (e.g., equality of all people, respect for human dignity, commitment to justice) that transcend specific norms and rules. It answers to a strong inner conscience and willingly disobeys laws that violate its own ethical principles."
        }
    }

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
 

 

   

