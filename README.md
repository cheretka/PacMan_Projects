# PacMan Projects
The PacMan projects were developed for CS 188. They apply an array of AI techniques to playing PacMan.

https://inst.eecs.berkeley.edu/~cs188/fa20/projects/

![Alt Text](https://github.com/cheretka/PacMan_Projects/blob/master/CS188%20Pacman%202021-06-18%2014-05-43.gif)

# Project 1: Search
https://inst.eecs.berkeley.edu/~cs188/fa20/project1/

In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. I build general search algorithms and apply them to Pacman scenarios.

Questions:
  - Finding a Fixed Food Dot using Depth First Search
```python
python pacman.py -l mediumMaze -p SearchAgent
```
  - Breadth First Search
```python
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```
  - Varying the Cost Function
```python
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
```
  - A* search
```python
python pacman.py -l mediumMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```
  - Finding All the Corners
```python
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```
  - Corners Problem: Heuristic
```python
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```
  - Eating All The Dots
```python
python pacman.py -l testSearch -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
```
  - Suboptimal Search
```python
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
```

# Project 2: Multi-Agent Search
https://inst.eecs.berkeley.edu/~cs188/fa20/project2/

In this project, I designed agents for the classic version of Pacman, including ghosts. Along the way, I implemented both minimax and expectimax search and try hand at evaluation function design.

Questions:
  - Reflex Agent
```python
python pacman.py -p ReflexAgent -l testClassic
```
  - Minimax
```python
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
```
  - Alpha-Beta Pruning
```python
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```
  - Expectimax
```python
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```
  - Evaluation Function
