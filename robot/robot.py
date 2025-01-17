import random


###
#  GLOBAL VARS
###
# Dictionary of parts and relationships
robot_parts = {
    1: { 'name': 'Wheel',      'max': 3, 'depends_on': 0, 'dependency_relation': False },
    2: { 'name': 'Axle',       'max': 3, 'depends_on': 1, 'dependency_relation': int.__lt__ },
    3: { 'name': 'Torso',      'max': 1, 'depends_on': 2, 'dependency_relation': int.__eq__ },
    4: { 'name': 'Plunger',    'max': 1, 'depends_on': 3, 'dependency_relation': int.__eq__ },
    5: { 'name': 'Head',       'max': 1, 'depends_on': 3, 'dependency_relation': int.__eq__ },
    6: { 'name': 'Antenna',    'max': 2, 'depends_on': 5, 'dependency_relation': int.__eq__ },
    7: { 'name': 'Power Cell', 'max': 4, 'depends_on': 3, 'dependency_relation': int.__eq__ },
}
# # Array of part names, indexable by interger from a 7-sided dice roll
# part_names = [
#     'ERROR',     #0 <-- array index, 0th index will never be used
#     'Wheel',     #1
#     'Axle',      #2
#     'Torso',     #3
#     'Plunger',   #4
#     'Head',      #5
#     'Antenna',   #6
#     'Powercell', #7
#     ]

# # Required part quantities for a full robot
# part_count_max = [
#     0, #0 <-- array index number, 0th index will never be used
#     3, #1 (3 wheels)
#     3, #2 (3 axles)
#     1, #3 (1 torso)
#     1, #4 (1 plunger)
#     1, #5 (1 head)
#     2, #6 (2 antennae)
#     4, #7 (4 powercells)
#     ]

# # dependent part
# part_depends_on = [ 
#     0, #0 <-- array index number, 0th index will never be used
#     0, #1 wheel does not depend on anything
#     1, #2 axle depends on wheel
#     2, #3 torso depends on axle
#     3, #4 plunger requires a torso
#     3, #5 head requires a torso
#     5, #6 antenna requires a head
#     3, #7 powercell requires a torso
#     ]

# # dependant part operation
# part_dependency_operation = [
#     0, #0 <-- array index number, 0th index will never be used
#     0, #1 wheel 
#     1, #2 axle depends on wheel
#     2, #3 torso depends on axle
#     3, #4 plunger requires a torso
#     3, #5 head requires a torso
#     5, #6 antenna requires a head
#     3, #7 powercell requires a torso
# ]

###
#  FUNCTIONS
###
def d7():
    ''' Simulate a 7 sided dice roll.
    '''
    return random.randint( 1, 7 )


def can_add_part( part_num, thBot ):
    ''' Determine if the requested part can be added to this thBot
        INPUT
        part_num: int, the index of the part to be added
                  (comes from random dice roll)
        thBot: array, the quantity of parts added so far
               (position in the array indicates the part type)
        OUTPUT
        bool: True if part can be added, False otherwise
    '''
    rv = False # return value, to be returned at the end of the function

    # number of parts for this type so far
    part_count = thBot[ part_num ]
    # max quantity allowed for this type of part
    max_allowed = robot_parts[ part_num ][ 'max' ]
    
    # Detemine if the part is able to be added at this time
    # The first test for every part will always be if max_allowed has been reached yet
    if part_count < max_allowed:
        # Now check part type for any additional rules
        dep_index = robot_parts[ part_num ][ 'depends_on' ]
        dep_count = thBot[ dep_index ]
        dep_required = robot_parts[ dep_index ][ 'max' ]
        dep_relationship = robot_parts[ dep_index ][ 'dependency_relation' ]
        if dep_count == dep_required
        # part count has "relationship" to dep_count
        if dep_relationship( part_count, dep_count ):
        if part_num == 2:
            # To add an axle, there must be a free wheel (ie: more wheels than axles)
            dep_count = thBot[dep_index]

        else:
            # all the other parts have the same rules,
            # dependant part must be at max qty
            dep_index = 3 # Plunger (4) Head (5) Power cell (7)
            if part_num == 1: # Wheel
                dep_index = 0
            elif part_num == 3: # Torso
                dep_index = 2
            elif part_num == 6: # Antenna
                dep_index = 5
            dep_count = thBot[dep_index]
            dep_required = part_count_max[dep_index]
            if dep_count == dep_required:
                rv = True
    return rv


def is_robot_complete( robot, allowed, debug=False ):
    ''' Check if the robot is complete
        by comparing the actual part counts to the required parts counts.
        Return true if part counts match, False otherwise.
    '''
    rv = True
    for i in ( 1, 2, 3, 4, 5, 6, 7 ):
        if robot[i] != allowed[i]:
            rv = False
            if debug:
                print( f"(COMPLETE?) mismatch on index {i}" )
            break
    if debug:
        print( f"(COMPLETE?) {robot}" )
        print( f"(COMPLETE?) {allowed}" )
    return rv


def mk_robot():
    ''' Build a robot that has the appropriate number of parts.
    '''
    # Robot is an array of part quantities, where
    # the position in the array indicates the part type
    robot = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
    roll_count = 0
    robot_completed = is_robot_complete( robot, part_count_max )
    while not robot_completed:
        new_part = d7()
        # print( f"Try to add item index {new_part}" )
        roll_count = roll_count + 1
        if can_add_part( new_part, robot ):
            robot[ new_part ] = robot[ new_part ] + 1
            print( f"Added index {new_part} = {part_names[new_part]}!")
            print( f"Robot is now {robot}" )
            print( f"Rolls so far: {roll_count}" )
            print()
            robot_completed = is_robot_complete( robot, part_count_max )
        if roll_count > 1000:
            raise SystemExit( 'Too many rolls, safety check' )
    print( f"Finally, a completed robot. Only took {roll_count} rolls." )
    print_robot( robot )
    print()
     

def print_robot( robot ):
    for i in ( 1, 2, 3, 4, 5, 6, 7 ):
        print( f"{part_names[i]}: {robot[i]}" )


def continue_or_exit():
    ''' Ask if the user wishes to continue?
    '''
    rv = False
    msg = f"Wanna make a robot? (yes, y, no, [n]) "
    answer = input( msg )
    if answer.lower().startswith( 'y' ):
        rv = True
    return rv


def main():
    while continue_or_exit():
        mk_robot()


if __name__ == "__main__":
    main()
