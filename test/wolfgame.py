# Filename: wolfgame.py
from WOLFgroupchat import WOLFGroupChat, WOLFGroupChatManager
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


#wolfgame.py
class Game:
    def __init__(self, players, groupchat, manager):
        self.players = players
        self.night = True
        self.player_map = {player.name: player for player in players}
        self.groupchat = groupchat
        self.manager = manager


    def play_round(self):
        if self.night:
            for player in self.players:
                if player.alive:
                    player.night_action(self)
        else:
            # 在调用run_chat方法时，为sender参数传入一个Agent对象
            self.manager.run_chat([{"role": "system", "content": "Day begins, please discuss and vote."}], sender=self.manager, config=self.groupchat)
            for player in self.players:
                if player.alive:
                    action = player.day_action(self)
                    self.manager.run_chat([{"role": "system", "content": action}], sender=player.agent, config=self.groupchat)
            self.vote()
        self.night = not self.night
        for message in self.manager.conversation:
            print(f"{message['name']}: {message['content']}")


        # 获取并打印聊天记录
        #chat_history = self.manager.get_chat_history()
        #for message in chat_history:
        #    print(f"{message['sender_name']}: {message['text']}")


    def run(self):
        while not self.game_over():
            self.play_round()

    
    def game_over(self):
        roles = [player.agent.role for player in self.players if player.alive]
        if 'wolf' not in roles:
            return True
        if roles.count('wolf') == len(roles):
            return True
        return False
    

    def vote(self):
        votes = {player: 0 for player in self.players if player.alive}
        for player in self.players:
            if player.alive:
                vote = player.vote(self)
                if vote is not None:  # 添加这一行
                    print(f"{player.name} the {player.agent.role} votes for {vote}")
                    if vote not in votes:
                        votes[vote] = 0
                    votes[vote] += 1
        max_votes = max(votes.values())
        for player, vote in votes.items():
            if vote == max_votes:
                if player is not None:  # 添加这一行
                    player.alive = False
                    print(f"{player.name} was voted out")
                break



class Player:
    def __init__(self, agent):
        self.name = agent.name
        self.agent = agent
        self.alive = True
    
    def chat(self, game):
        chat_message = self.agent.generate_chat(game, 'day')
        return f"{self.name} the {self.agent.role} {chat_message}"

    def night_action(self, game):
        action = self.agent.generate_action(game, 'night')
        print(f"{self.name} the {self.agent.role} {action}")

    def day_action(self, game):
        action = self.agent.generate_action(game, 'day')
        return f"{self.name} the {self.agent.role} {action}"

    def vote(self, game):
        vote_name = self.agent.generate_vote(game, 'day')  # 使用新的 generate_vote 方法
        if vote_name not in game.player_map:
            print(f"Invalid vote name: {vote_name}")
            return None
        vote = game.player_map[vote_name]
        print(f"{self.name} the {self.agent.role} votes for {vote.name}")
        return vote
    
    

