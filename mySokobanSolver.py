'''
    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

import search 
import sokoban


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11036583, 'Shangzhe', 'Lin'), (10335838, 'Mitchell', 'Hosking'), (11285672, 'Aaron', 'Halangoda') ]

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
        Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
        Rule 2: all the cells between two corners along a wall are taboo if none of 
        these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
        A string representing the warehouse with only the wall cells marked with 
        a '#' and the taboo cells marked with a 'X'.  
        The returned string should NOT have marks for the worker, the targets,
        and the boxes.  
    '''
    def _is_corner_cell(x, y, vis, x_size, y_size):
        """Check if a cell is a corner based on adjacent walls.

        Args:
            x, y: Coordinates of the cell to check
            vis: 2D array representing the warehouse visualization
            x_size, y_size: Dimensions of the warehouse

        Returns:
            bool: True if the cell is a corner, False otherwise
        """
        return any([
            y > 0 and x > 0 and vis[y - 1][x] == "#" and vis[y][x - 1] == "#",
            y > 0 and x < x_size - 1 and vis[y - 1][x] == "#" and vis[y][x + 1] == "#",
            y < y_size - 1 and x > 0 and vis[y + 1][x] == "#" and vis[y][x - 1] == "#",
            y < y_size - 1 and x < x_size - 1 and vis[y + 1][x] == "#" and vis[y][x + 1] == "#"
        ])

    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)

    vis = [[" "] * x_size for y in range(y_size)]
    for (x, y) in warehouse.walls:
        vis[y][x] = "#"

    taboo = set()
    for y in range(y_size):
        first_wall_x = -1
        last_wall_x = -1
        for x in range(x_size):
            if vis[y][x] == '#':
                if first_wall_x == -1:
                    first_wall_x = x
                last_wall_x = x
        if first_wall_x != -1:
            for x in range(first_wall_x + 1, last_wall_x):
                if vis[y][x] == " ":
                    if _is_corner_cell(x, y, vis, x_size, y_size) and (x, y) not in warehouse.targets:
                        taboo.add((x, y))
        for x in range(x_size):
        first_wall_y = -1
        last_wall_y = -1
        for y in range(y_size):
            if vis[y][x] == '#':
                if first_wall_y == -1:
                    first_wall_y = y
                last_wall_y = y
        if first_wall_y != -1:
            for y in range(first_wall_y + 1, last_wall_y):
                if vis[y][x] == " ":
                    corners_in_column = []
                    for yy in range(y_size):
                        if (x,yy) in taboo:
                            corners_in_column.append(yy)
                    for i in range(len(corners_in_column) - 1):
                        start_y = corners_in_column[i]
                        end_y = corners_in_column[i+1]
                        all_clear = True
                        for yy in range(start_y + 1, end_y):
                            if (x,yy) in warehouse.targets:
                                all_clear = False
                                break
                        if all_clear:
                            for yy in range(start_y + 1, end_y):
                                taboo.add((x,yy))

    for (x, y) in taboo:
        vis[y][x] = "X"

    result = ""
    for y in range(y_size):
        for x in range(x_size):
            if vis[y][x] == "#" or vis[y][x] == "X":
                result += vis[y][x]
            else:
                result += " "
        if y < y_size - 1:
            result += "\n"
    return result


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.
    
    Your implementation should be fully compatible with the search functions of
    the provided module 'search.py'.
    '''
    
    def __init__(self, warehouse):
    raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        """
        raise NotImplementedError


def check_elem_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    raise NotImplementedError()


def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution.
    The second item is the total cost of this action sequence.

    @param
     warehouse: a valid Warehouse object

    @return

        If puzzle cannot be solved
            return 'Impossible', None

        If a solution was found,
            return S, C
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''

    raise NotImplementedError()
                            if (x,yy) in warehouse.targets:
                                all_clear = False
                                break
                        if all_clear:
                            for yy in range(start_y + 1, end_y):
                                taboo.add((x,yy))

    for (x, y) in taboo:
        vis[y][x] = "X"

    result = ""
    for y in range(y_size):
        for x in range(x_size):
            if vis[y][x] == "#" or vis[y][x] == "X":
                result += vis[y][x]
            else:
                result += " "
        if y < y_size - 1:
            result += "\n"
    return result


class SokobanPuzzle(search.Problem):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    Your implementation should be fully compatible with the search functions of
    the provided module 'search.py'.
    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
        """
        raise NotImplementedError


def check_elem_action_seq(warehouse, action_seq):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
    @param warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
    @param action_seq: a sequence of legal actions.
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C


    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution.
    The second item is the total cost of this action sequence.

    @param
     warehouse: a valid Warehouse object

    @return

        If puzzle cannot be solved
            return 'Impossible', None

        If a solution was found,
            return S, C
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''

    raise NotImplementedError()
