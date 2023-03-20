import numpy as np
import random
from snake_game2 import Point
from snake_game2 import Direction, SnakeGame
from ploting_module2 import plot
import json
import os.path

class Agent:

    def __init__(self):
        #self.games_number = 0
        self.epsilon = 0
        self.gamma = 0.81
        self.ls = 0.41
        #self.Qtable = np.random.uniform(low=-0.5, high=0.5, size=(4, 9, 16, 3))

        if not os.path.isfile(f'file_alfa{self.ls}_gamma{self.gamma}.json'):
            with open(f'file_alfa{self.ls}_gamma{self.gamma}.json', 'a') as f:
                table = np.zeros((4, 9, 16, 3))
                tableBetter = table.tolist()
                qwe = {
                'game_number' : 0,
                'memory' : tableBetter,
                'score' : [0],
                'average' : [0],
                'record' : 0
                }
                j = json.dumps(qwe)
                f.write(j)
            self.memory = json.load(open(f'file_alfa{self.ls}_gamma{self.gamma}.json'))
        elif os.path.isfile(f'file_alfa{self.ls}_gamma{self.gamma}.json'):
            self.memory = json.load(open(f'file_alfa{self.ls}_gamma{self.gamma}.json'))

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

        state1 = [
            dir_l,
            dir_r,
            dir_u,
            dir_d
            ]

        state2 = [
            # Danger straight
            (dir_r and game.colision(point_r)) or 
            (dir_l and game.colision(point_l)) or 
            (dir_u and game.colision(point_u)) or 
            (dir_d and game.colision(point_d)),

            # Danger right
            (dir_u and game.colision(point_r)) or 
            (dir_d and game.colision(point_l)) or 
            (dir_l and game.colision(point_u)) or 
            (dir_r and game.colision(point_d)),

            # Danger left
            (dir_d and game.colision(point_r)) or 
            (dir_u and game.colision(point_l)) or 
            (dir_r and game.colision(point_u)) or 
            (dir_l and game.colision(point_d))]

        state3 = [
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]
        
        return np.array(state1, dtype=int), np.array(state2, dtype=int), np.array(state3, dtype=int)

    def get_state_next(self, game, move):
        head = game.snake[0]
        
        clock_directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_directions.index(game.direction)

        if np.array_equal(move, [1, 0, 0]): #no change of direction
            new_direction = clock_directions[index]
        elif np.array_equal(move, [0, 1, 0]): #turn right
            next_index = (index + 1) % 4
            new_direction = clock_directions[next_index]
        else:
            next_index = (index - 1) % 4
            new_direction = clock_directions[next_index]

        old_direction = game.direction
        if old_direction == Direction.LEFT and np.array_equal(move, [1, 0, 0]):
            new_head_x = head.x - 20
            new_head_y = head.y
        if old_direction == Direction.LEFT and np.array_equal(move, [0, 1, 0]):
            new_head_x = head.x
            new_head_y = head.y - 20
        if old_direction == Direction.LEFT and np.array_equal(move, [0, 0, 1]):
            new_head_x = head.x
            new_head_y = head.y + 20
        if old_direction == Direction.RIGHT and np.array_equal(move, [1, 0, 0]):
            new_head_x = head.x + 20
            new_head_y = head.y
        if old_direction == Direction.RIGHT and np.array_equal(move, [0, 1, 0]):
            new_head_x = head.x
            new_head_y = head.y + 20
        if old_direction == Direction.RIGHT and np.array_equal(move, [0, 0, 1]):
            new_head_x = head.x
            new_head_y = head.y - 20
        if old_direction == Direction.UP and np.array_equal(move, [1, 0, 0]):
            new_head_x = head.x
            new_head_y = head.y - 20
        if old_direction == Direction.UP and np.array_equal(move, [0, 1, 0]):
            new_head_x = head.x + 20
            new_head_y = head.y
        if old_direction == Direction.UP and np.array_equal(move, [0, 0, 1]):
            new_head_x = head.x - 20
            new_head_y = head.y
        if old_direction == Direction.DOWN and np.array_equal(move, [1, 0, 0]):
            new_head_x = head.x
            new_head_y = head.y + 20
        if old_direction == Direction.DOWN and np.array_equal(move, [0, 1, 0]):
            new_head_x = head.x - 20
            new_head_y = head.y
        if old_direction == Direction.DOWN and np.array_equal(move, [0, 0, 1]):
            new_head_x = head.x + 20
            new_head_y = head.y

        point_l = Point(new_head_x - 20, new_head_y)
        point_r = Point(new_head_x + 20, new_head_y)
        point_u = Point(new_head_x, new_head_y - 20)
        point_d = Point(new_head_x, new_head_y + 20)


        dir_l = new_direction == Direction.LEFT
        dir_r = new_direction == Direction.RIGHT
        dir_u = new_direction == Direction.UP
        dir_d = new_direction == Direction.DOWN

        state1 = [
            dir_l,
            dir_r,
            dir_u,
            dir_d
            ]

        state2 = [
            # Danger straight
            (dir_r and game.colision(point_r)) or 
            (dir_l and game.colision(point_l)) or 
            (dir_u and game.colision(point_u)) or 
            (dir_d and game.colision(point_d)),

            # Danger right
            (dir_u and game.colision(point_r)) or 
            (dir_d and game.colision(point_l)) or 
            (dir_l and game.colision(point_u)) or 
            (dir_r and game.colision(point_d)),

            # Danger left
            (dir_d and game.colision(point_r)) or 
            (dir_u and game.colision(point_l)) or 
            (dir_r and game.colision(point_u)) or 
            (dir_l and game.colision(point_d))]

        state3 = [
            game.food.x < new_head_x,  # food left
            game.food.x > new_head_x,  # food right
            game.food.y < new_head_y,  # food up
            game.food.y > new_head_y  # food down
            ]
        
        return np.array(state1, dtype=int), np.array(state2, dtype=int), np.array(state3, dtype=int)

    def get_action(self, c1, c2, c3):
        self.epsilon = 150 - self.memory['game_number']
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            move = np.argmax(self.memory['memory'][c1][c2][c3])
            final_move[move] = 1
        return final_move

def find_index(vector):
    i = 0
    for cell in vector:
        if cell == 1:
            return i
        else:
            i += 1

def binaryToDecimal(val): 
    return int(val, 2) 

def train():
    plot_scores = []
    plot_average_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        state_old = agent.get_state(game)
        vect_directions = state_old[0]
        vect_dangers = state_old[1]
        vect_point = state_old[2]
        qwe = ''.join([str(elem) for elem in vect_dangers])
        asd = ''.join([str(elem) for elem in vect_point])
        coordinate1 = find_index(vect_directions)
        coordinate2 = binaryToDecimal(qwe)
        coordinate3 = binaryToDecimal(asd)
        index_q = np.argmax(agent.memory['memory'][coordinate1][coordinate2][coordinate3])
        q = agent.memory['memory'][coordinate1][coordinate2][coordinate3][index_q]
        finale_move = agent.get_action(coordinate1, coordinate2, coordinate3)
        #--------------------------
        game_over, score, reward = game.play_step(finale_move) #make move
        #--------------------------
        state_new = agent.get_state_next(game, finale_move)
        vect_directions_new = state_new[0]
        vect_dangers_new = state_new[1]
        vect_point_new = state_new[2]
        qwe_new = ''.join([str(elem) for elem in vect_dangers_new])
        asd_new = ''.join([str(elem) for elem in vect_point_new])
        coordinate1_new = find_index(vect_directions_new)
        coordinate2_new = binaryToDecimal(qwe_new)
        coordinate3_new = binaryToDecimal(asd_new)
        index_q_prim = np.argmax(agent.memory['memory'][coordinate1_new][coordinate2_new][coordinate3_new])
        q_prim = agent.memory['memory'][coordinate1_new][coordinate2_new][coordinate3_new][index_q_prim]
        #-------------------------
        #new_Q = q + agent.ls * (reward + agent.gamma * q_prim - q)
        #------------------------

        agent.memory['memory'][coordinate1][coordinate2][coordinate3][index_q] = agent.memory['memory'][coordinate1][coordinate2][coordinate3][index_q] + agent.ls * (reward + agent.gamma * q_prim - q)
        with open(f'file_alfa{agent.ls}_gamma{agent.gamma}.json', 'w') as f:
            json.dump(agent.memory, f)


        #agent.memory['memory'][coordinate1][coordinate2][coordinate3][index_q] = new_Q
        #print(q, new_Q)

        

        if game_over == True:
            game.reset()
            agent.memory['game_number'] = agent.memory['game_number'] + 1
            #print(f'gra', agent.games_number)


            if score > record:
                record = score
                #agent.model.save()

            print('Game: ', agent.memory['game_number'], 'Score: ', score, 'Record: ', record)

            plot_scores.append(score)
            total_score += score
            average_score = total_score / agent.memory['game_number']
            plot_average_scores.append(average_score)
            if agent.memory['game_number'] == 700:
                plot(plot_scores, plot_average_scores)
                break
                

    
if __name__ == '__main__':
    train()