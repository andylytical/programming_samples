import random


###
#  GLOBAL VARS
###
# Array of part names, indexable by interger from a 7-sided dice roll
part_names = [
    'ERROR',     #0 <-- array index, 0th index will never be used
    'Wheel',     #1
    'Axle',      #2
    'Torso',     #3
    'Plunger',   #4
    'Head',      #5
    'Antenna',   #6
    'Powercell', #7
    ]

# Required part quantities for a full robot
part_count_max = [
    0, #0 <-- array index number, 0th index will never be used
    3, #1 (3 wheels)
    3, #2 (3 axles)
    1, #3 (1 torso)
    1, #4 (1 plunger)
    1, #5 (1 head)
    2, #6 (2 antennae)
    4, #7 (4 powercells)
    ]


###
#  FUNCTIONS
###
def d7():
    ''' Simulate a 7 sided dice roll.
    '''
    return random.randint( 1, 7 )


def can_add_part( part_num, robot ):
    ''' Determine if the requested part can be added to this robot
        INPUT
        part_num: int, the index of the part to be added
                  (comes from random dice roll)
        robot: array, the quantity of parts added so far
               (position in the array indicates the part type)
        OUTPUT
        bool: True if part can be added, False otherwise
    '''
    rv = False # return value, to be returned at the end of the function

    # number of parts of this type so far
    part_count = robot[ part_num ]
    # max quantity allowed for this type of part
    max_allowed = part_count_max[ part_num ]
    
    # Detemine if the part is able to be added at this time
    # First test for every part will always be if max_allowed has been reached yet
    if part_count < max_allowed:
        # Now check part type for any additional rules
        if part_num == 1:
            # Wheel
            # no dependencies
            rv = True
        elif part_num == 2:
            # Axle
            # must be a free wheel (ie: more wheels than axles)
            num_wheels = robot[1]
            if num_wheels > part_count:
                rv = True
        else:
            # all the other parts have the same rules,
            # dependant part must be at max qty
            depends_on = 3 # Plunger (4) Head (5) Power cell (7)
            if part_num == 3: 
                # Torso
                depends_on = 2
            elif part_num == 6:
                # Antenna
                depends_on = 5
            dep_qty = robot[depends_on]
            dep_required = part_count_max[depends_on]
            if dep_qty == dep_required:
                rv = True
    return rv


def is_robot_complete( robot, allowed, show=False ):
    ''' Check if the robot is complete
        by comparing the actual part counts to the required parts counts.
        Return true if part counts match, False otherwise.
    '''
    rv = True
    for i in ( 1, 2, 3, 4, 5, 6, 7 ):
        if robot[i] != allowed[i]:
            rv = False
            if show:
                print( f"(COMPLETE?) mismatch on index {i}" )
            break
    if show:
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
            robot_completed = is_robot_complete( robot, part_count_max )
            print()
        # else:
        #     print( f"Nope, can't add {part_names[new_part]}." )
        # print( f"Rolls so far: {roll_count}" )
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
