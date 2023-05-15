import torch
import random
import numpy as np
from snake_gameAI import SnakeGameAI, Direction, Point
from collections import deque
from model import Linear_QNet, QTrainer
#from ploter import plot
import json
import os.path

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.games_number = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 5, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        #if not os.path.isfile(f'file_gamma{self.gamma}.json'):
        #    with open(f'file_gamma{self.gamma}.json', 'a') as f:
        #        qwe = {
        #        'game_number' : 0,
        #        'score' : [0],
        #        'average' : [0],
        #        'record' : 0
        #        }
        #        j = json.dumps(qwe)
        #        f.write(j)
        #    self.games_memory = json.load(open(f'file_gamma{self.gamma}.json'))
        #elif os.path.isfile(f'file_gamma{self.gamma}.json'):
        #    self.games_memory = json.load(open(f'file_gamma{self.gamma}.json'))

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.collision(point_r)) or 
            (dir_l and game.collision(point_l)) or 
            (dir_u and game.collision(point_u)) or 
            (dir_d and game.collision(point_d)),

            # Danger right
            (dir_u and game.collision(point_r)) or 
            (dir_d and game.collision(point_l)) or 
            (dir_l and game.collision(point_u)) or 
            (dir_r and game.collision(point_d)),

            # Danger left
            (dir_d and game.collision(point_r)) or 
            (dir_u and game.collision(point_l)) or 
            (dir_r and game.collision(point_u)) or 
            (dir_l and game.collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]
        
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def get_action(self, state):
        self.epsilon = 150 - self.games_number
        final_move = [0, 0, 0]
        if random.randint(0, 150) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            #print(prediction)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_average_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    game_cntr = 0

    if game_cntr == 0:
        while True:
            #get old state 
            state_old = agent.get_state(game)
            #print(state_old)

            #get move
            finale_move = agent.get_action(state_old)

            #perfrorm move and get new state
            reward, game_over, score = game.play_step(finale_move)
            state_new = agent.get_state(game)

            #train short memory
            agent.train_short_memory(state_old, finale_move, reward, state_new, game_over)

            #remember
            agent.remember(state_old, finale_move, reward, state_new, game_over)

            if game_over:
                #train long memory, plot results
                #print(agent.model.linear1.state_dict())
                #print(agent.trainer.optimizer.state_dict())
                #print(self.linear1.state_dict())
                checkpoint = {'state_dict' : agent.model.state_dict(), 'optimizer' : agent.trainer.optimizer.state_dict()}
                agent.model.save_checkpoint(checkpoint)
                game.reset()
                #print(self.linear1.state_dict())
                #agent.games_memory["game_number"] = agent.games_memory["game_number"] + 1
                #print("gra", agent.games_memory["game_number"])
                agent.train_long_memory()
                #agent.model.save()

                #if score > record:
                #    record = score
                    #agent.model.save()

                #print('Game: ', agent.games_number, 'Score: ', score, 'Record: ', record)

                #plot_scores.append(score)
                #total_score += score
                #average_score = total_score / agent.games_number
                #plot_average_scores.append(average_score)
                #plot(plot_scores, plot_average_scores)
                game_cntr += 1
                print('Game: ', agent.games_number, 'Score: ', score)
                agent.games_number += 1

    elif game_cntr != 0:
        while True:
            agent.model.load_checkpoint('model.pth')
            agent.trainer.load_checkpointv2('model.pth')
            #get old state 
            state_old = agent.get_state(game)
            #print(state_old)

            #get move
            finale_move = agent.get_action(state_old)

            #perfrorm move and get new state
            reward, game_over, score = game.play_step(finale_move)
            state_new = agent.get_state(game)

            #train short memory
            agent.train_short_memory(state_old, finale_move, reward, state_new, game_over)

            #remember
            agent.remember(state_old, finale_move, reward, state_new, game_over)

            if game_over:
                #train long memory, plot results
                #print(agent.model.linear1.state_dict())
                #print(agent.trainer.optimizer.state_dict())
                #print(self.linear1.state_dict())
                checkpoint = {'state_dict' : agent.model.state_dict(), 'optimizer' : agent.trainer.optimizer.state_dict()}
                agent.model.save_checkpoint(checkpoint)
                game.reset()
                #print(self.linear1.state_dict())
                #agent.games_memory["game_number"] = agent.games_memory["game_number"] + 1
                agent.train_long_memory()
                #agent.model.save()

                #if score > record:
                #    record = score
                    #agent.model.save()

                #print('Game: ', agent.games_number, 'Score: ', score, 'Record: ', record)

                #plot_scores.append(score)
                #total_score += score
                #average_score = total_score / agent.games_number
                #plot_average_scores.append(average_score)
                #plot(plot_scores, plot_average_scores)
                game_cntr += 1
                print('Game: ', agent.games_number, 'Score: ', score)
                agent.games_number += 1



if __name__ == '__main__':
    train()
    