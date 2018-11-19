import numpy as np
import time
import copy

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6,)

robot_state = []
diamond_state = []
diamond_goal = []
bool = True

class Node(object):
    def __init__(self, value):
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.value = value



class Tree(object):
    def __init__(self, data):
        self.root = Node(data)
        self.listofmaps = []

    def precorder_call(self):
        return self.preorder_create(self.root, "", self.listofmaps)


    def move_robot(self, data, vert, hori):
        this_map = data[0]
        rob_pos = data[1]
        #print "The robot start position is ", rob_pos, "ak: ", rob_pos[0], rob_pos[1]
        #print "Inspect the map: "
        #self.print_map(this_map)
        #print "Looking at the map 'M' = ", this_map[rob_pos[0]][rob_pos[1]]
        dia_pos = data[2]
        data_out = []
        next_pos = [rob_pos[0]+vert, rob_pos[1]+hori]
        ## Check if the next position is an wall


        if this_map[next_pos[0]][next_pos[1]] == 'X' :
            data_out = [this_map, rob_pos, dia_pos]
            data_out.append(False)
            #print "The next_pos = 'X' - FALSE"
            return data_out;

        ## Checking if the next position is a free spot
        if this_map[next_pos[0]][next_pos[1]] == '.' :
            ## If it is a free spot, check if the current position is the robot
            if this_map[rob_pos[0]][rob_pos[1]] == 'M':
                ## If it is the robot on the current position, swap the robot and the free spot and update the robot state
                this_map[rob_pos[0]][rob_pos[1]], this_map[next_pos[0]][next_pos[1]] = this_map[next_pos[0]][next_pos[1]], this_map[rob_pos[0]][rob_pos[1]]
                rob_pos = next_pos
                data_out = [this_map, rob_pos, dia_pos]
                data_out.append(True)
                #print "The next_pos = '.' and current is = 'M' -> SWITCH POSITION- TRUE"
                return data_out;
            ## If not the robot check if it is a diamound
            elif this_map[rob_pos[0]][rob_pos[1]] == 'J':
                ## If it is, then swap the diamond and the free spot
                for i in range(0, len(dia_pos)):
                    if dia_pos[i][0] == rob_pos[0] and dia_pos[i][1] == rob_pos[1] :
                        dia_pos[i] = next_pos
                this_map[rob_pos[0]][rob_pos[1]], this_map[next_pos[0]][next_pos[1]] = this_map[next_pos[0]][next_pos[1]], this_map[rob_pos[0]][rob_pos[1]]
                data_out = [this_map, rob_pos, dia_pos]
                data_out.append(True)
                #print "The next_pos = '.' and current is = 'J' -> SWITCH POSITION - TRUE"
                return data_out;
        ## If the next position is a diamond
        if this_map[next_pos[0]][next_pos[1]] == 'J' :
            ## Check if the current positin is also a diamond
            if this_map[rob_pos[0]][rob_pos[1]] == 'J' :
                data_out = [this_map, rob_pos, dia_pos]
                data_out.append(False)
                #print "The next_pos = 'J' and current is = 'J' -> CANT MORE - FALSE"
                return data_out;
            ## Check what is on the other side of diamond
            data_out = [this_map, next_pos, dia_pos]
            if self.move_robot(data_out, vert, hori)[3] :
                ## If it can be moved, swap places and update robot state
                this_map[rob_pos[0]][rob_pos[1]], this_map[next_pos[0]][next_pos[1]] = this_map[next_pos[0]][next_pos[1]], this_map[rob_pos[0]][rob_pos[1]]
                rob_pos = next_pos
                data_out = [this_map, rob_pos, dia_pos]
                data_out.append(True)
                return data_out;
            data_out.append(False)
            return data_out;

        print "WIll never happen!"
        this_map[rob_pos[0]][rob_pos[1]], this_map[next_pos[0]][next_pos[1]] = this_map[next_pos[0]][next_pos[1]], this_map[rob_pos[0]][rob_pos[1]]
        rob_pos = next_pos
        data_out = [this_map, rob_pos, dia_pos]
        data_out.append(True)
        return data_out;

    def preorder_create(self, start, move, listofmaps):
        global bool
        if start and bool:
            illegal_move = move
            current_data = start.value

            list_of_maps = listofmaps

            for j in range(0, len(current_data[2])):
                if self.stuck_in_corner(current_data[0], current_data[2][j]) :
                    return True;

            for i in range(0, len(list_of_maps)):
                if self.compare_maps(current_data[0], list_of_maps[i]):
        #            print "LOOP AVOIDED!"
        #            print "LOOP AVOIDED!"
        #            print "LOOP AVOIDED!"

                    return True;

            list_of_maps.append(current_data[0])


            if(self.goal_reached(copy.deepcopy(current_data[2]), diamond_goal)) :
                bool = False;
                return True;

        #    print "\n\n\nNew layer reached!"
            self.print_map(current_data[0])

            # MOVE LEFT
        #    print "Trying to move left and create new NODE!"
            left_data = self.move_robot(copy.deepcopy(current_data), 0, -1)

            if left_data[3] and not illegal_move == "LEFT":
                start.left = Node(left_data[0:3])
        #        print "Succes in moving left!"
                self.print_map(left_data[0])
        #    else:
        #        print "Could NOT move left"

            # Moving right
        #    print "Trying to move right and create new NODE!"
            right_data = self.move_robot(copy.deepcopy(current_data), 0, 1)

            if right_data[3] and not illegal_move == "RIGHT" :
        #        print "Succes in moving right!"
                start.right = Node(right_data[0:3])
                self.print_map(right_data[0])
        #    else:
        #        print "Could NOT move right"


            # Moving up
        #    print "Trying to move up and create new NODE!"
            up_data = self.move_robot(copy.deepcopy(current_data), -1, 0)
            if up_data[3] and not illegal_move == "UP" :
        #        print "Succes in moving up!"
                start.up = Node(up_data[0:3])
                self.print_map(up_data[0])
        #    else:
        #        print "Could NOT move up"

            # Moving down
        #    print "Trying to move down and create new NODE!"
            down_data = self.move_robot(copy.deepcopy(current_data), 1, 0)

            if down_data[3] and not illegal_move == "DOWN":
        #        print "Succes in moving down!"
                start.down = Node(down_data[0:3])
                self.print_map(down_data[0])
        #    else:
        #        print "Could NOT move down"


            time.sleep(0.01)
        #    print "RIGHT LAYER!"
            self.preorder_create(start.right, "LEFT", list_of_maps)
        #    print "LEFT LATER!"
            self.preorder_create(start.left, "RIGHT", list_of_maps)
        #    print "UP LAYER"
            self.preorder_create(start.up, "DOWN", list_of_maps)
        #    print "DOWN LAYER"
            self.preorder_create(start.down, "UP", list_of_maps)
        return True;


    def print_map(self, my_map) :
        for x in range(0,len(my_map)):
            print my_map[x]


    def goal_reached(self, state, goal):
        count = 0 ;
        for i in range(0,len(state)):
            for j in range(0,len(goal)):
                if state[i][0] == goal[j][0] and state[i][1] == goal[j][1]:
                    count +=1
        if count == 4 :
            return True;
        return False;


    def stuck_in_corner(self, map, dia_position):
        global diamond_goal

        for j in range(0, len(diamond_goal)):
            if dia_position[0] == diamond_goal[j][0] and dia_position[1] == diamond_goal[j][1] :
                return False;

        if map[dia_position[0]-1][dia_position[1]] == 'X' and map[dia_position[0]][dia_position[1]-1] == 'X':
            return True;
        if map[dia_position[0]][dia_position[1]-1] == 'X' and map[dia_position[0]+1][dia_position[1]] == 'X' :
            return True;
        if map[dia_position[0]+1][dia_position[1]] == 'X' and map[dia_position[0]][dia_position[1]+1] == 'X' :
            return True;
        if map[dia_position[0]][dia_position[1]+1] == 'X' and map[dia_position[0]-1][dia_position[1]] == 'X' :
            return True;
        return False;

    def stuck_along_side(self, map, dia_pos):
        global diamond_goal
        next_pos = 'X'
        index = 0
        counter = 0

        if map[dia_pos[0]-1][dia_pos[1]] == 'X' :
            while next_pos == 'X' :
                index +=1
                next_pos = map[dia_pos[0]-1][dia_pos[1]+index]
                if map[dia_pos[0]][dia_pos[1]+index] == 'X':
                    counter +=1
                    break;
            while next_pos == 'X' :
                index -=1
                next_pos = map[dia_pos[0]-1][dia_pos[1]+index]
                if map[dia_pos[0]][dia_pos[1]+index] == 'X':
                    counter +=1
                    break;
            if counter == 2 :
                return True;


        if map[dia_pos[0]][dia_pos[1]-1] == 'X' :

        if map[dia_pos[0]+1][dia_pos[1]] == 'X' :

        if map[dia_pos[0]][dia_pos[1]+1] == 'X' :


    def compare_maps(self, map1, map2) :
        for i in range(1, len(map1)):
            for j in range(len(map1[i])):
                if not map1[i][j] == map2[i][j] :
                    return False;
        return True;

def main():
    global robot_state
    global diamond_state
    robot_state = robot_start
    diamond_state = diamond_start
    illegal_move = "None"


    init_data = [copy.deepcopy(map), copy.deepcopy(robot_state), copy.deepcopy(diamond_state)]

    tree = Tree(init_data)
    while not tree.precorder_call() :
        print "FAILED - No solution found"
    print "DONE!"

if __name__ == "__main__":
    map_file = "map.txt"

    data = np.loadtxt(map_file, delimiter=',', dtype=str)
    info = data[0].split(' ')

    width = int(info[0])
    #print "Width = " + str(width)
    height = int(info[1])
    #print "Height = " + str(height)
    diamonds = int(info[2])
    #print "# of diamonds = " + str(diamonds)

    data = np.loadtxt(map_file, delimiter=',', dtype=str, skiprows=1)
    robot_start = 0
    global diamond_goal
    diamond_start = []
    map = []
    for i in range(0,height):
        map.append(list(data[i]))
        for j in range(0, len(map[i])):
            if map[i][j] == 'M':
                robot_start = [i,j]
            if map[i][j] == 'G':
                diamond_goal.append([i,j])
                map[i][j] = '.'
            if map[i][j] == 'J':
                diamond_start.append([i,j])
        print map[i]
    print "Robot start: ", robot_start
    print "Diamond goals: ", diamond_goal
    print "Diamonds init location: ", diamond_start

    main()
