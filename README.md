# platformAI


Demonstration:  https://youtu.be/ExOb8yVXUqI

Hello to our Reinforcement Learning project.



We teach AI to play a jumping game.

The jumping game is builded by scratch with pygame and then we implement an agent and a deep learning algorithm with pytorch.






How it works: 

Definition of Reinforcement learning:
Reinforcement learning is an area of machine learning concerned with how software agents ought to take actions
in an environment in order to maximize the notion of cumulative reward.




So, our agent here is our computer player (it recieves the reward) and the environment would be the game.
with the reward we tell the agent how well is doing, and then based on the reward it tries to find the best next action.


In the code we have :


  	1) The agent:   
		-game
		
		-model   #it must know about both
		
	  Training:
	  
		-state = get_state(game)   
		
		-action = get_move(game):
		
		    -model.predict()
			
		-reward,game_over, score= game.play_step(action)
		
		-new_state = get_state(game)
		
		-remember
		
		-model.train()
		
		
 	 2) Game(Pygame):   #there is a gameloop
		-play_step(action)  #for each gameloop it moves
		
		     -> reward,game_over,score #after the move return all these
 


 	 3) Model (Pytorch):    # feed forward neural network

		Linear_QNet(DQN)    #it needs to have the new state and the old state
		
		- model.predict(state)
		   ->action
		  




-Reward: 
         
	 If it moves in the right direction:                 +10 #more details in the state
	 
	 Gameover or it moves in the wrong direction:	     -10

-Action: # The actions that the agent can make.

	[1,0,0]  -> right
	
	[0,1,0]  -> left
	
	[0,0,1]  -> jump 
	

-State (6 states):  # What does the agent know about its enviroment
	state =	
		 
		 [game.next_plat_is_left(),    #checks if the next platform is left
		 
		 game.next_plat_is_above(),   #checks if the next platform is right in top of the character   
		 
		 game.next_plat_is_right(),   #checks if the next platform is right
		 
		 game.can_jump(), 	      #checks if its touching the ground
		 
		 game.going_up(),             #checks if the character is going up
		 
		 game.is_below()]	      #checks if it already passed the objective platform
		 
		 
	


Model : # feedforward neuronet 
			         
						 
	                 O
			
              O  -   O
		
              O  -   O
				
	          O  - 	 O  -	O
			  
	STATE ->  O  -	 ▒  -	O  -> ACTION
	
	          O  -	 O  -	O
			  
	          O  - 	 O
			  
                     O
						 
                     O
						 
	          6 -- hidden---3     
			  


Q LEARNING: 

	Q value = Quality of action #we want to improve the decision

	0. Init Q value (=init model)
	1. Choose action (model.predict(state))   #sometimes will be a random move
	2. Perform action
	3. Measure reward
	4. Update Q value (+train model)
	5. Repeat to item 1... (loop)

