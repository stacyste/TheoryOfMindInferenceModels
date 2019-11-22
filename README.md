# Theory of Mind Inference Models

## Introduction
Humans are able to make incredibly rich inferences about others from very little data, 
even at a young age <sup id="a1">[1](#f1)</sup><sup id="a2">[2](#f2)</sup>. These behavioral predictions and explanations stem from understanding others in terms of their 
underlying mental states including beliefs, desires, and intentions. This notion, called Theory of Mind (ToM), gets much of its power
from the assumption that people behave rationally with respect to those underlying mental states. Rational behavior implies that 
individuals act in efficient and parsimoniuos ways to achieve their underlying goals given constraints of the environment.

For example, if a woman walking down the street ducks to avoid a low hanging branch, we would assume that she would not duck had
the branch not been there. A man gets out of his car in the supermarket parking lot and starts walking to the store then all of a sudden
he turns back to his car. In most cases, we do not assume he has suddenly gone crazy, but that some change in his mental states
led to that change in action. Maybe he left his wallet or forgot to lock the car.

In all of these scenarios, we use observables, namely actions and aspects of the environment, to infer hidden states of the mind.
Using the framework of ToM under the assumption of rationality, we can operationalize these ideas into computational models undergoing the 
same process.  

## Computational Tools
There are a set of fundamental tools that we can draw from engineering, decision theory, and artificial intelligence to help solve this
type of problem. One such tool is a Markov Decision Process (MDP). MDPs are defined by the tuple $\langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R} \rangle$.
A set of states, actions, a transition function describing the dynamics of the environment, and a reward function giving some numerical
value to each state or state-action pair in the world respectively. This formulation allows us to model an agent's decision making process
 given a goal in an environment in discrete time.
 
 The second major tool for ToM models is Bayesian Inference. While MDPs allow a forward model of decision making, it is generated directly
 from the underlying mental states. Recall that these are not actually observable. Baye's Rule allows us to reverse this problem and perform
 inverse planning by looking at the set of possible mental states and evaluating which is most likely using the observable actions in the environment.
 
 Using these tools, we are able to build models infering latent mental states and extend these models to capture a variety of situations (e.g. partially
 observable environments where planning is done by a Partially Observable MDP or POMDP).

## Included Demos
In this repository are the implemented models and computational tools needed to answer questions about how to infer what others' beliefs, desires, and
goals are in a variety of 2D grid settings. These demos were originally written and designed by me as homework assignments for UCLA's 
graduate course Cognitive Artificial Intelligence in the Department of Statistics. They draw from a variety of papers and sources in statistics, 
computer science, and cognitive psychology and come with a set of visualizations to create an intuitive understanding of results.

In more detail: 
- Demo 1: Implementation of Bayesian Inference; how to find the posterior of a distribution from a prior and likelihood  
- Demo 2: Value Iteration; a model for planning of the best actions to take in each possible scenario; a means of solving MDPs  
- Demo 3: Goal Inference; a model to infer goals across time from observed actions; combines value iteration for MDPs and Bayesian inference  
- Demo 4: Signaling Policies; a model of how to act in ways that communicate a goal to others; combines value iteration for MDPs and likelihood ratios  
- Demo 5: POMDPs Heaven and Hell; a model of how to act in partially observable environments; exhibits information seeking behavior  
- Demo 6: POMDPs Food Truck; a model to jointly infer beliefs and desires (specifically preferences) of others in a partially observable environment  



## References
<b id="f1">1</b> Jara-Ettinger, J., Gweon, H., Tenenbaum, J. B., & Schulz, L. E. (2015). 
[Children’s understanding of the costs and rewards underlying rational action.](https://www.sciencedirect.com/science/article/pii/S0010027715000566) 
Cognition, 140, 14-23 [↩](#a1)

<b id="f2">1</b> Xu, F., & Garcia, V. (2008). 
Intuitive statistics by 8-month-old infants. 
Proceedings of the National Academy of Sciences, 105(13), 5012-5015.[↩](#a2)
