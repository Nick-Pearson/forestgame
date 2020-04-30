# Forest Game

Each player builds a town from scratch and tries to be the most sucessful. You can build an economy based on the buildings in your town
You can also build an army, armys can take control of other player's buildings

Kind of like Age or Empires meets dungeon keeper but turn based. Initially made for 4 people
Turn based, with a limit maybe 10 turns in total
At the end the player with the most points wins. Can earn points based on your economy or your army
Maybe a timer to prevent watching other player's turns getting tedious

The world is entirely forest in a grid layout, players can clear the forest to gain materials and space for buildings. 
Armys can only move through grid tiles where the forest has been cleared

Civilians are invisible and are assumed to spend most of their time in houses, soliders can be seen

## IDEAS

Goals to reach on the map?
High resource areas / Capture points?

Gaurd tower building - extra defense

### Resources

Population: Will grow naturally provided there is space in the town (like AoE where villagers require houses)
Building Material: Used to create buildings, obtained by clearing forest
Gold: Money, used for paying the army and building more advanced things stuff like that
Food: Needed to support population

### Stats

Taxes: How much gold gained per turn from the population (based on employed population)
Player can set taxes to "low" "medium" or "high"
"low": 50% of usual
"medium": Base amount of gold, no effect on politics
"high": 150% of gold, negative effect on politics for every turn it is applied


Politics: How much your people like you? Could control things like army morale not sure
Unemployment: To prevent players from just creating a massive civilian population, should reduce taxes or something
Total soldiers
Total civilians

### Town buildings

Types of building
Work building: Employs a number of civilians
Environment building: Modifies the behaviour of the tile
Houses: Increases population cap
Town hall: Starter building with base population cap, immune to opposing armies

#### Types of work building

Early game:
Farm: Generates food per turn, medium employment
Gold mine: Generates gold per turn, medium employment

Mid game:
Swamill: Increases material gained from clearing forest, medium employment
Refinery?: Increases gold gained from mines
Windmill: Increases food gained from farms

Late game:
Church: Buffs politics stat, low employment 
Barracks: Allows promotion of soldiers to level 2, low employment 

#### Type of environment building

Road: Speed boost for soldiers moving over this tile, applies to all players
Wall: Impassable barrier

### Army rules

A soldier must cost more than he brings in

3 levels of solider with salaries that must be paid each turn to keep them employed
Also an initial training cost to be paid when they reach that level

**Level 1**
Training: 1
Salary: 1

**Level 2**
Training: 2
Salary: 2

**Level 3**
Training: 3
Salary: 3