# Genetic-Algorithms-Project

## Objective:
To get familiar with the process of population evolution by using the inspirations of natural selection amongst a randomly generated initial population, and how it is applied to find solutions of modern problems.

## Description:
In this project, we were supposed to find the correct combination of logic gates in a logic design. This design gets 10 input signals (TRUE/FALSE). The first 2, feed the first logic gate, the output of this gate and the third input feed the second logic gate and so on, until the output of the last gate provides the output of the system. Thus, 9 logic gates should be determined from 6 possible choices for each of them: AND, OR, XOR, NAND, NOR, XNOR.  
We were provided with a truth table which determined the desired output for each combination of the 10 input signals (1024 possible combinations). The goal was to find the right combination of gates to be match the truth table and provide the desired output for each input combination. Implementation of these concept is conducted using python programming language.  
It is notable that there are approximately 10 millions of possible gate combinations (6 to the power of 9), and genetic algorithms are used to search this space efficiently.  

## Methodology:
First, we should have created a random initial population consisting of individual chromosomes, each of which suggesting a combination of gates that needed to be evaluated. A fitness function was defined to demonstrate the extent of validity of each solution (chromosome). The fitness score for each chromosome is equal to the number of correctly provided outputs -calculated out of 1024. This score was calculated for each generation at the beginning. Then, each generation went through a number of genetic procedures such as **crossover and mutation** based on their fitness value, in order to create the next chromosomes of next generation. Finally, the suitable chromosomes of the new and previous generation were combined to shape the new generation. In this way, the chromosomes are involved until the desired chromosome, the one with complete fitness value, appears to be introduced as chosen solution. 

## Result:
In the image below, the log of one of the executions of the code is demonstrated. Accordingly, the correct combination has been found after 47 levels of genetic evolution in a relatively short time. 
