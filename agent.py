import torch
import random
import numpy as np
from collections import deque 
from game import JumpGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen = MAX_MEMORY) #popleft()
        self.model = Linear_QNet(6,256,3)
        self.trainer = QTrainer(self.model,lr=LR, gamma = self.gamma)


    def get_state(self,game):
        state = [game.next_plat_is_left(), game.next_plat_is_above(), game.next_plat_is_right(),
        game.can_jump(),
        game.going_up(),
        game.is_below()]
#        print (np.array(state,dtype=int))
        return np.array(state,dtype=int)

        
    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done)) #popleft if MAX_MEMORY is reached


    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards, next_states ,dones)    

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        #random move: tradeoff exploration /  explotation
        self.epsilon = 50 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,100)<self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1

        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = JumpGameAI()
    while True:
        #get the old state
        state_old = agent.get_state(game)
        
        #get move
        final_move = agent.get_action(state_old)

        #permorf move and get new state
        reward, done, score = game.play_step(final_move, agent.n_games)

        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old,final_move, reward,state_new,done)

        #remember
        agent.remember(state_old,final_move, reward,state_new,done)

        if done:
            #train long memory, plot the results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.mode.save()

            print ('Game', agent.n_games, 'Score',score, 'Record:', record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train() 
