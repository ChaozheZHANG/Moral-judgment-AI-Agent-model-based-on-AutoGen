#/Users/zhangchaozhe/Desktop/autogen/test/CC_function_rule.py
from autogen.agentchat.conversable_agent import ConversableAgent
from CC_agent_1 import CC1_AssistantAgent
from CC_agent_2 import CC2_AssistantAgent
from CC_agent_3 import CC3_AssistantAgent
import numpy as np
#pip install -U scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from typing import Callable, Dict, Optional, Union
import numpy as np



class Game:
    def __init__(self, players, groupchat, manager):
        self.players = players
        self.groupchat = groupchat
        self.manager = manager

    def run(self):
        while not self.groupchat.is_over():
            # 在这里，每个代理做出决策
            self.play_round()

            # 在每轮结束后，更新每个玩家的 output
            for player in self.players:
                player.update_output()

        # 游戏结束后，获取并打印每个玩家的最终决策
        self.final_decisions()

    def play_round(self):
        # 在这里实现每轮的对话逻辑
        pass

    def final_decisions(self):
        for player in self.players:
            decision = player.output
            print(f"{player.agent.name}'s final decision is {decision}")
            
            # Use CC_proxy_agent to make moral judgment and select the final result
            morality_score = calculate_morality_score(player.agent, decision)
            print(f"{player.agent.name}'s morality score is {morality_score}")
            
            # Categorize the decision and print the result
            decision_category = categorize_decision(morality_score)
            print(f"{player.agent.name}'s decision category is {decision_category}")


#class Game:
#    def __init__(self, players, groupchat, manager):
#        self.players = players
#        self.groupchat = groupchat
#        self.manager = manager

#    def final_decisions(self):
#        for player in self.players:
#            decision = player.make_final_decision()
#            print(f"{player.name}'s final decision is {decision}")
            
            # Use CC_proxy_agent to make moral judgment and select the final result
#            morality_score = calculate_morality_score(player.agent, decision)
#            print(f"{player.name}'s morality score is {morality_score}")
            
            # Categorize the decision and print the result
#            decision_category = categorize_decision(morality_score)
#            print(f"{player.name}'s decision category is {decision_category}")


# Function to calculate morality score

def calculate_morality_score(agent, decision):
    score = decision_score(decision)
    return categorize_decision(sigmoid(score))

def decision_score(decision):
    # Define your scoring rules based on decision
    choices = ["xxx1", "xxx2", "xxx3"]
    vectorizer = CountVectorizer().fit_transform([decision] + choices)
    vectors = vectorizer.toarray()

    csim = cosine_similarity(vectors)
    # The first row of csim is the similarity between the decision and each choice
    scores = csim[0, 1:]

    # Return the score plus 1 because choices are 1-indexed
    return scores.argmax() + 1


def categorize_decision(sigmoid_score):
    if sigmoid_score < 0.4:
        return "Decision 1: xxx1"
    elif sigmoid_score < 0.7:
        return "Decision 2: xxx2"
    else:
        return "Decision 3: xxx3"

def sigmoid(x):
    return 1 / (1 + np.exp(-x))



#class Option:
    def __init__(self, benefits_self, follows_norms, upholds_principles):
        self.benefits_self = benefits_self
        self.follows_norms = follows_norms
        self.upholds_principles = upholds_principles

#option1 = Option(True, False, False)  # benefits self
#option2 = Option(False, True, False)  # follows norms
#option3 = Option(False, False, True)  # upholds principles

#options = [option1, option2, option3]

#class Player:
    def __init__(self, agent):
        self.name = agent.name
        self.agent = agent
        self.alive = True
        self.decision = self.agent.get_output()
        self.morality_score = calculate_morality_score(agent)
        # Add a morality_stage attribute
        self.morality_stage = self.agent.get_morality_stage()

    def make_final_decision(self, options):
        # Normalize morality score to range [0, 1]
        normalized_score = (self.morality_score - 0.5) / 0.4
        # Calculate weighted probabilities for each option
        probabilities = [normalized_score if opt == 1 else (1 - normalized_score) for opt in options]
        # Adjust probabilities based on morality stage
        if self.morality_stage == "preconventional":
            # Player is more likely to choose options that benefit themselves
            probabilities = [p * 1.2 if opt.benefits_self else p * 0.8 for p, opt in zip(probabilities, options)]
        elif self.morality_stage == "conventional":
            # Player is more likely to choose options that follow social norms
            probabilities = [p * 1.2 if opt.follows_norms else p * 0.8 for p, opt in zip(probabilities, options)]
        elif self.morality_stage == "postconventional":
            # Player is more likely to choose options that align with universal moral principles
            probabilities = [p * 1.2 if opt.upholds_principles else p * 0.8 for p, opt in zip(probabilities, options)]
        # Normalize probabilities so they sum to 1
        probabilities = probabilities / np.sum(probabilities)
        # Make a decision based on weighted probabilities
        decision = np.random.choice(options, p=probabilities)
        print(f"{self.name} chose {options.index(decision) + 1}")
        return decision
    

class Player:
    def __init__(self, agent):
        self.name = agent.name
        self.agent = agent
        self.output = None  # 初始化 output 为 None
        # 假设 get_output 方法返回一个字典，其中包含 "Choice" 和 "Reasoning" 这两个键
        output = self.agent.get_output()
        self.decision = output.get("Choice")
        self.reasoning = output.get("Reasoning")
        self.morality_score = calculate_morality_score(agent)
        # Add a morality_stage attribute
        self.morality_stage = self.agent.get_morality_stage()

    def update_output(self):
        # 如果代理有 get_output 方法，就调用它并将结果存储在 output 中
        if hasattr(self.agent, "get_output"):
            self.output = self.agent.get_output()

    def make_final_decision(self):
        # 这里我们假设决定是一个字符串，例如 "Option 1"
        if self.decision == "Option 1":
            return 1
        elif self.decision == "Option 2":
            return 2
        else:
            # 如果决定不是 "Option 1" 或 "Option 2"，则返回一个默认值
            return 0


#这个代码主要包括了游戏类、选项类和玩家类的定义，以及一些与决策打分和分类相关的函数。
#看起来这个代码的主要目的是模拟一个游戏，在游戏中，玩家根据他们的道德评分和道德阶段做出决策。
#这个决策过程包括了选择自我利益、遵循社会规范或者坚持普遍的道德原则。
#在这个代码的基础上，可以进行以下一些改进：
#将所有的全局函数和变量封装到类中，使得代码结构更加清晰，便于维护和扩展。
#为Game类添加一些额外的功能，比如保存游戏状态、让玩家可以在游戏中互动等。
#将选项类和玩家类的定义移动到单独的模块中，使得代码结构更加模块化。
#为Player类添加更多的属性和方法，比如玩家的策略、玩家的历史决策等。
#优化决策打分和分类的算法，使得决策的结果更加合理和公平。