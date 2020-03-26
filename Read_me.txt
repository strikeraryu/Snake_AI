It is a snake game AI (self playing AI) implemented using two ways:
1) NEAT (NeuroEvolution of Augmenting Topologies) is an evolutionary algorithm that creates artificial neural networks.
2) Self-Made model using tensor flow

1 NEAT
    1.1 Neural Network Structure
        Input layers with 2 nodes and output layers with 4 nodes
    1.2 Input and output
        Input in absolute difference between x and y coordinate and output is the direction to move (up,down,left,right)
    1.3 Fitness function
        Dying, going far and in infinite loop decreases fitness whereas getting closer and eating food increases the fitness

    Let it run for some time it get better with each generation.
    Other details related to neural network is in config_feedforward.txt file

2 TensorFlow
    1.1 Neural Network Structure
        Input layers with 16 nodes and output layers with 4 nodes (activation function is softmax)and it is Fully connected
    1.2 Input and output
        Distance to food and tail in 8 direction (default is '-1') and output is the direction to move (up,down,left,right)
    1.3 other details
        max gen - 50
        epochs - 100
        optimizer - adam
    1.4 implementation
        A game is run using prediction of Neural network and then every input to Neural network is stored if it is getting closer to food the current label is stored 
        and if not then label  is changed, When game end the model is trained with stored inputs
    
    Let it run for some time it get better with each generation.