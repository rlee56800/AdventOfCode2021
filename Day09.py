'''
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small
hydrothermalvents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid
it and be that much safer. The submarine generates a heightmap of the floor of the
nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
following heightmap:

2*1*9994321*0*
3987894921
98*5*6789892
8767896789
989996*5*678

Each number corresponds to the height of a particular location, where 9 is the
highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of 
its adjacent locations. Most locations have four adjacent locations (up, down, left, 
and right); locations on the edge or corner of the map have three or two adjacent 
locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the 
first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom 
row (also a 5). All other locations on the heightmap have some lower adjacent 
location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk 
levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low 
points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of 
all low points on your heightmap?

'''
##################################################################################
# Variable definitions and such
height_map = [] # matrix of all values in height map
x = [] # row of low point
y = [] # col of low point

# saves input as array (sorry john python)
with open('Day09_Input.txt', 'r') as f:
    for line in f.readlines():
        hm = []
        stripped = line.strip() # gets rid of newline
        for ch in stripped:
            c = ord(ch) - 48 # casts char to ASCII int; removes ASCII part
            hm.append(c)
        hm.insert(0, 9)
        hm.insert(len(hm), 9) # adds 9 (highest value) to edges
        height_map.append(hm)

# adds row of 9s to top and bottom
# (wall of 9s around actual array because arr[-1] does something)
hm = []
for i in range(len(height_map[0]) + 2):
    hm.append(9)
height_map.insert(0, hm)
height_map.insert(len(height_map), hm)

#print(height_map)

rows = len(height_map) - 2 # amt rows
cols = len(height_map[1]) - 2 # amt cols
lowest = [] # list of lowest heights


##################################################################################
# function definitions
def risk_level(rl):
    # calculates risk levels
    risk_lev = sum(rl)
    risk_lev += len(rl)
    return risk_lev

def find_lowests():
    # finds lowest values (brute force)
    for i in range(1, rows+1):
        #print(height_map[i])
        for j in range(1, cols+1):
            cur = height_map[i][j]
            if(cur < height_map[i-1][j]) and (cur < height_map[i+1][j]) and (cur < height_map[i][j-1]) and (cur < height_map[i][j+1]):
                lowest.append(cur)
                x.append(i)
                y.append(j)


##################################################################################
# call functions
find_lowests()
print(risk_level(lowest))
print(x)
print(y)

'''
--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

*2**1*99943210
*3*987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

21999*4**3**2*1**0*
398789*4*9*2**1*
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
39*8**7**8*94921
9*8**5**6**7**8*9892
*8**7**6**7**8*96789
9*8*99965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789*8*92
876789*6**7**8*9
98999**6**5**6**7**8*

Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
'''
##################################################################################
# variable definitions and such
basins = [] # list of all basin totals
searched = [] # T/F; whether a square was added

##################################################################################
# fuction definitions
def fill_false():
    # resets "searched" matrix
    searched = []
    s = []
    for j in range(len(height_map[0])):
        s.append(False)
    for i in range(len(height_map)):
        searched.append(s)

def search(i, j):
    if height_map[i][j] == 9:
        return 0
    else:
        sum = 1
        if searched[i+1][j]:
            sum += search(i+1, j)
        if searched[i-1][j]:
            sum += search(i-1, j)
        if searched[i][j+1]:
            sum += search(i, j+1)
        if searched[i][j-1]:
            sum += search(i, j-1)
    return sum

def check_four(i, j):
    return search(i+1, j) + search(i-1, j) + search(i, j+1) + search(i, j-1)

##################################################################################
# call functions
fill_false()

for i in range(len(x)):
    basins.append(check_four(x[i], y[i]))

basins.sort(reverse = True)
print(basins[0] * basins[1] * basins[2])