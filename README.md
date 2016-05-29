# geneticstring
A Python script to find a string through Genetic Algorythms

# Some stats
This stats were proven using two different functions that are on the geneticstring.py algorithm:

1. crossoverByGen: This was the first implemented function this use the entire gen (letter) and can't generate new letters from it, it depends on high mutation rates
2. crossover: This is the latest function, this one makes the crossover with the bits of the gen, interlacing them, so there should be new letters coming from the specie that weren't there before

| Type of Crossover | Mutation Rate | Average Generations Amount  (Less is faster)|
| :------------- | :------------- | :------------- |
| crossoverByGen | 0.05           | 11406          |
| crossoverByGen | 0.1            | 8325           |
| crossoverByGen | 0.5            | 8541           |
| crossover      | 0.05           | 10055          |
| crossover      | 0.1            | 5528           |
| crossover      | 0.5            | 7651           |

- crossoverByGen Average: 9424
- crossover Average: **7744**

So crossover function is about 17% faster than crossoverByGen
