# Overview of Code
This code describes and models the current coronavirus (COVID-19) pandemic in the state of Idaho. With this, we hope to provide information on how well Idaho is dealing with COVID-19.

It models the pandemic in Idaho as kinetic function of time in days, with equations that model the uninfected, infected, recovered, and deaths in Idaho.

## Tell us a little bit about the idaho_infections.csv file and what it holds
And maybe tell us a little bit about how we might compare our plots from kinetics.py with it.

The idaho_infections.csv file includes the number of infected people in Idaho and the number of days since the first recorded infection. 

# Software Requirements
This code requires access to a commandline terminal and to have a github account to access the p2-kinetics repository and to be able to track and collaborate with other researchers on this topic. For this program to run, python must be installed on the local machine.To download Python go to terminal, type in the command line "apt-get install python". This will start 
downloading Python onto the local machine. It will ask a few permission questions and you will have to let it install Python onto the local machine.


# How to Get This Code
To run this code on your computer, pull the p2-kinetics repository from github class master to your terminal, or fork the repository and pull the code from your own personal repository. 

# How to Use This Code
To use this code you must be in the directory that contains the code. Type "$ python kinetics.pyi " + the path to the file that contains the data.


# Figures Showing Our Code Output Here

# Links to Cite Where We Got Our Data
Idaho Division of Public Health - https://public.tableau.com/profile/idaho.division.of.public.health#

New York Times GitHub Repo -  https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv


# Results from playing with parameters
Increasing k1 makes the beginning of the infection begin sooner, and increasing k2 raises the maximum number of individuals that won't be infected

# Info copy pasted from info.txt - should be cleaned up
Project 2 descriptions:
    Modeling kinetics: rate of change between things!
    
    A -> B -> C
    
The rates of change betweeen A->B and B->C Determine when we will see a certain concentration, AND the initial conditions. 

Species C:
    comes from a reaction from B->C
    
    Line 14 has k2*B in that big list that's returned
    That MEANS: dC/dt = k2 * B
    That means: Amount of C goes up over time, depending on how much B there is.
    k2 is a CONSTANT for this project
    
Species A: 
    dA/dt is in the first element of the list returned on line 14
    dA/dt = -k1*A*B/(A+B+C)
This reaction depends on the concentration of A and the concentration of B
concentration of A is A/(A+B+C), and the concentration of B is B/(A+B+C)

k1 and k2 are our reaction constants

12/31/2019
Date that an unknown pneumonia detected in Wuhan, China was reported to the WHO (1)

1/20/2019
Date that testing confirmed the first case of COVID-19 in the United States (1)

3/13/2020
Date that testing confirmed the first case of COVID-19 in the state of Idaho (2)

3/13/2020
Date that the decision was made to deliver all BSU classes remotely, which began the following Monday (3)

3/25/2020
Date that Governor Brad Little issued a statewide stay-at-home order (2)

First confirmed case of COVID-19 coincides with the BSU announcement while the self-isolation notice 
occured 12 days later

4/17/2020
Date that Boise conservative groups plan to protest stay-at-home order. (4) Hundreds of people were reported to aggregate without masks, disregarding social distancing. (5)














1. Wikipedia contributors. (2020, April 15). 2019–20 coronavirus pandemic. In Wikipedia, The Free Encyclopedia. Retrieved 20:35, April 15, 2020, from https://en.wikipedia.org/w/index.php?title=2019%E2%80%9320_coronavirus_pandemic&oldid=951160943

2. Wikipedia contributors. (2020, April 14). 2020 coronavirus pandemic in Idaho. In Wikipedia, The Free Encyclopedia. Retrieved 20:41, April 15, 2020, from https://en.wikipedia.org/w/index.php?title=2020_coronavirus_pandemic_in_Idaho&oldid=950859214

3. Tromp, President, Dr. Marlene "Message from the President, Dr. Marlene Tromp." Message to (BSU staff and students). 15 March 2020 E-mail

4. Idaho Statesman. (2020, April 16). https://www.idahostatesman.com/news/politics-government/state-politics/article242061306.html

5. Idaho Statesman. (2020, April 17) https://www.idahostatesman.com/news/coronavirus/article242092321.html
