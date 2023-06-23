# platformAI: Reinforcement Learning-based Jumping Game
Demo Video: [platformAI Demo](https://youtu.be/ExOb8yVXUqI)

Welcome to platformAI, our exciting project where we leverage Reinforcement Learning (RL) to teach an AI agent to play a unique jumping game. The game is built from scratch using Pygame and we've implemented a deep learning algorithm using Pytorch to educate our agent.

## How does it work?

Reinforcement Learning is a subset of machine learning where an agent learns to make decisions by taking certain actions in an environment to maximize a reward. In our scenario, the AI agent (computer player) interacts with the game (environment) and learns from the rewards it receives.

The interaction can be broken down into the following steps:

### 1. The AI Agent

- It first obtains the current state of the game (`state = get_state(game)`)
- It then determines the next move to make (`action = get_move(game)`)
    - This decision is made by the agent's model prediction (`model.predict()`)
- The agent then plays the game with the chosen action (`reward, game_over, score = game.play_step(action)`)
- The new game state is updated (`new_state = get_state(game)`)
- The agent then remembers this interaction and trains the model (`model.train()`)

### 2. The Game (Pygame)

- For each game loop, the game makes a move based on the agent's action (`play_step(action)`)
    - After making the move, the game returns the reward, game over status, and the score

### 3. The Model (Pytorch)

- It's a feed-forward neural network known as Deep Q-Network (DQN) or `Linear_QNet`
    - The model predicts the next action based on the current state (`model.predict(state)`)

#### Rewarding Mechanism

- If the agent moves in the correct direction, it receives a reward of +10.
- If the game is over or the agent moves in the wrong direction, the agent is penalized with a reward of -10.

#### Available Actions

- Move right: [1,0,0]
- Move left: [0,1,0]
- Jump: [0,0,1]

#### State Parameters

The agent observes the game environment based on the following six parameters:

- Whether the next platform is to the left (`game.next_plat_is_left()`)
- Whether the next platform is directly above (`game.next_plat_is_above()`)
- Whether the next platform is to the right (`game.next_plat_is_right()`)
- Whether the agent can jump (`game.can_jump()`)
- Whether the agent is going up (`game.going_up()`)
- Whether the agent has already passed the target platform (`game.is_below()`)

#### Model Architecture

Our model is a feed-forward neural network with a hidden layer:

STATE (6 units) → [Hidden Layer] (▒) → ACTION (3 units)

#### Q-Learning Process

Q-Learning is an RL algorithm where Q represents the 'Quality of an action'. The main aim is to constantly better the agent's decisions.

Steps in Q-Learning:

1. Initialize Q value (same as initializing the model)
2. Choose an action (`model.predict(state)`) - occasionally, a random move may be chosen
3. Perform the chosen action
4. Measure the reward for the action
5. Update the Q value (train the model with the new data)
6. Repeat steps 1 to 5 until the agent learns to play the game efficiently.
