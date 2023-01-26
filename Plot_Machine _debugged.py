import math
import numpy as np
from random import choices,choice
from time import time
from collections import OrderedDict


def determine_loop_direction(points):
    n = len(points)
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    a = sum(x[i]*y[(i+1)%n] - x[(i+1)%n]*y[i] for i in range(n))
    return "Counterclockwise" if a > 0 else "Clockwise"
##########################################################################################
def calculate_angle(line1, line2):
    x1, y1 = line1[1][0] - line1[0][0], line1[1][1] - line1[0][1]
    x2, y2 = line2[1][0] - line2[0][0], line2[1][1] - line2[0][1]
    return math.atan2(x1*y2 - y1*x2, x1*x2 + y1*y2)
##########################################################################################
def sharpest_right_turn(angles):
    
    angles_in_radians = [math.radians(angle) for angle in angles]
    right_turn_angles = []
    for i in range(len(angles_in_radians)):
        right_turn_angles.append(angles_in_radians[i])
    max_turn_index = right_turn_angles.index(min(right_turn_angles))
    return max_turn_index

def loop_finder(INPUT_LINES):

    """
    Given a list of lines represented as pairs of points, this function finds all loops in the lines.
    A loop is defined as a series of lines where the endpoint of one line is the startpoint of the next line, and the endpoint of the last line is the startpoint of the first line.
    The function returns a list of loops, with each loop represented as a list of points in the order they are encountered in the loop.
    :param INPUT_LINES: list of lines represented as pairs of points
    :return: list of loops, each represented as a list of points
    """
    Loops=[]
    
    for current_line in INPUT_LINES: 
        Loop=[]
        Loop.append(current_line[0])
        Loop.append(current_line[1])

        connecting_lines=[]
        flipped_connector=[]
        # line is  a connecting line, but not itself
        
        for line in INPUT_LINES:
            if line [0] == current_line[1] and line != current_line:
                connecting_lines.append(line)
            if line [1] == current_line[1] and line != current_line:
                flipped_connector=[]
                flipped_connector.append(line[1])
                flipped_connector.append(line[0])
                connecting_lines.append(flipped_connector)
            
        

        if len(connecting_lines) >=1:
            connecting_angles = []
            for neigbhor in connecting_lines:
                angle = calculate_angle(current_line, neigbhor)           
                connecting_angles.append(math.degrees(angle))
            next_line_index= sharpest_right_turn(connecting_angles)
            next_line = connecting_lines[next_line_index]
            Loop.append(next_line[1])
        
        while Loop[-1] != Loop[0]:
            
            Next_connecting_lines=[]
            for line in INPUT_LINES:  
                if line == next_line or line[1] == next_line[0] and line[0] == next_line[1]:
                    pass
                else:
                    if line [0] == Loop[-1] :
                            Next_connecting_lines.append(line)
                    
                    if line [1] == Loop[-1] :
                            flipped_connector=[]
                            flipped_connector.append(line[1])
                            flipped_connector.append(line[0])
                            Next_connecting_lines.append(flipped_connector)

            
            if len(Next_connecting_lines) >=1:
                next_connecting_angles =[]
                for next_neigbhor in Next_connecting_lines:
                    angle = calculate_angle(next_line, next_neigbhor)           
                    next_connecting_angles.append(math.degrees(angle))
                next_line_index= sharpest_right_turn(next_connecting_angles)
                next_line = Next_connecting_lines[next_line_index]
                Loop.append(next_line[1])
                if Loop.count(next_line[1]) == 2:
                    break
            else:
                Loop=[]
                break
        if len(Loop) >=1:    
            Loop.pop(-1)   #delete double coordinate

        direction = determine_loop_direction(Loop)
        if direction== "Clockwise":
            if len(Loop) >=1:  
                Loops.append(Loop)
        if direction== "Counterclockwise":
            Loop=[]
            FlippedStart=[]
            FlippedStart.append(current_line[1])
            FlippedStart.append(current_line[0])
            INPUT_LINES.append(FlippedStart)
    new_loops = []
    for sublist in Loops:
        is_duplicate = False
        for other_sublist in new_loops:
            if set(map(tuple,sublist)) <= set(map(tuple,other_sublist)):
                is_duplicate = True
                break
        if not is_duplicate:
            new_loops.append(sublist)
    Loops = new_loops              #Loops is now the cleaned up version of itself




    return Loops

##########################################################################################
def find_overlapping_plots(plots):
    # Create a dictionary to store the mapping from plot number to overlapping plots
    plot_overlaps = {}
    # Iterate over each plot
    for i, plot in enumerate(plots):
        # Initialize an empty list to store the overlapping plots for this plot
        overlaps = []
        # Iterate over the other plots
        for j, other_plot in enumerate(plots):
            # Skip the current plot
            if i == j:
                continue
            # Check if the current plot has 2 or more coordinates in common with the other plot
            common_coords = set(plot).intersection(set(other_plot))
            if len(common_coords) >= 2:
                overlaps.append(j)
        # Add the mapping from plot number to overlapping plots to the dictionary
        plot_overlaps[i] = overlaps
    # Create a list of tuples (plot number, overlapping plots) from the dictionary
    result = [(plot, overlaps) for plot, overlaps in plot_overlaps.items()]
    return result
##########################################################################################
def convert_data(list_neighbours: list[list[int, list[int]]]) -> dict:
    """
    Converts the data from a list to a dictionary.
    """
    # Initialize the dictionary
    dictionary = {}

    # Loop through the plots
    for plot, neighbours in list_neighbours:

        # Add the plot to the dictionary
        dictionary[plot] = {'value': None, 'neighbours': neighbours}
    return dictionary
##########################################################################################
def random_distribution(dictionary: dict) -> dict:
    
    """
    Randomly assign a value to each plot and checks if the rules are
    respected.
    """
    # Declare the possible values
    values = ['L', 'I', 'G', 'O', 'E']
    weights = [20, 20, 20, 20, 20]
    L_Count=0
    I_Count=0
    G_Count=0
    O_Count=0
    E_Count=0
    
    # Get the first plot in the dictionary
    first_plot = list(dictionary.keys())[0]

    # Choose a random value from the list of possible values
    value = choice(['L', 'I', 'G', 'O', 'E'])
    VALID_VALUES=[]
    # Assign the random value to the first plot and change possible Neighbor Values accordingly
    dictionary[first_plot]['value'] = value
    combined_plots = {}
    for neighbor in dictionary[first_plot]['neighbours']:
        if dictionary[first_plot]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
        elif dictionary[first_plot]['value'] == 'I':
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        #elif dictionary[first_plot]['value'] == 'G':
            # while "G" in values:
            #     index= values.index("G")
            #     if index < len(values):
            #         values.pop(index)
            #         weights.pop(index)
        if L_Count >= 4:
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if I_Count >= 4:
            while "I" in values:
                index= values.index("I")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if G_Count >= 4:
            while "G" in values:
                index= values.index("G")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if O_Count >= 4:
            while "O" in values:
                index= values.index("O")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if E_Count >= 1:
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)

        
        
        valid_vals= ([neighbor],values,weights)
        VALID_VALUES.append(valid_vals)
    VALID_VALUES_NO_DOUBLES = []
        
            
    visited=[0]
    #print("visi",visited)
    #print("COMBI",combined_plots)
        


        
    
    # Assign a value to the plot, using weighted probability
    
    #value = choices(values, weights=weights, k=1)[0]
    #Count the Assigned Values
    if value=="L":
        L_Count=L_Count+1                    
        
    elif value=="I":
        I_Count=I_Count+1
        
    elif value=="G":
        G_Count=G_Count+1
        
    elif value=="O":
        O_Count=O_Count+1
        
    elif value=="E":
        E_Count=E_Count+1
    
    
    for i in VALID_VALUES:
                if i not in VALID_VALUES_NO_DOUBLES:
                    VALID_VALUES_NO_DOUBLES.append(i)
    for plot in VALID_VALUES_NO_DOUBLES:
            plot_num, possible_values, weights = plot
            plot_num = plot_num[0]
            indices = range(len(possible_values))
            if plot_num in combined_plots:
                current_values, current_weights= combined_plots[plot_num]
                combined_values = set(current_values) & set(possible_values)
                combined_indices = [i for i in indices if possible_values[i] in combined_values]
                combined_weights = [weights[i] for i in combined_indices]
                combined_plots[plot_num] = (list(combined_values), combined_weights)
            else:
                combined_plots[plot_num] = (possible_values, weights)
    combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}
    sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
    
    # Assign the value to the plot
    # dictionary[neighbor]['value'] = value

    values = ['L', 'I', 'G', 'O', 'E']
    weights = [20, 20, 20, 20, 20]
        
    

    
    # plots_sorted = []
    # for plot in dictionary.keys():
    #     remaining_values = 5 - len(values)
    #     plots_sorted.append((plot, remaining_values))
    # plots_sorted.sort(key=lambda x: x[1])
    #print("PLOTS_SORTED_WEIRD",sorted_dict)
    

    # Loop through the plots
    while combined_plots != {}:
        for plot in sorted_dict:
            if plot>0:
                visited.append(plot)
                
                # Check the values of the neighbors
                for neighbor in dictionary[plot]['neighbours']:
                    # if dictionary[neighbor]['value'] == 'G':
                    #     while "G" in values:
                    #         index= values.index("G")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # elif dictionary[neighbor]['value'] == 'C':
                    #     while "I" in values:
                    #         index= values.index("I")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    if dictionary[neighbor]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'I':
                        while "L" in values:
                            index= values.index("L")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                        # while "C" in values:
                        #     index= values.index("C")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                        # while "P" in values:
                        #     index= values.index("P")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'E':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if L_Count >= 4:
                        while "L" in values:
                            index= values.index("L")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if I_Count >= 4:
                        while "C" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if G_Count >= 4:
                        while "G" in values:
                            index= values.index("G")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if O_Count >= 4:
                        while "O" in values:
                            index= values.index("O")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if E_Count >= 1:
                        while "E" in values:
                            index= values.index("E")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                
                    
                    valid_vals= ([neighbor],values,weights)
                    VALID_VALUES.append(valid_vals)

            # Assign a value to the plot, using weighted probability
            if(len(values))>=1:
                value = choices(values, weights=weights, k=1)[0]
                
                # Assign the value to the plot
                dictionary[plot]['value'] = value
                

            else:
                for plot in dictionary.keys():
                    # Set the value to None
                    
                    dictionary[plot]['value'] = None
                return False 
            
            for i in VALID_VALUES: ###################################################### List operations for combining different possibilities when checking from a different neigbor
                    if i not in VALID_VALUES_NO_DOUBLES:
                        VALID_VALUES_NO_DOUBLES.append(i)
            for plot in VALID_VALUES_NO_DOUBLES:
                    plot_num, possible_values, weights = plot
                    plot_num = plot_num[0]
                    indices = range(len(possible_values))
                    if plot_num in combined_plots:
                        current_values, current_weights= combined_plots[plot_num]
                        combined_values = set(current_values) & set(possible_values)
                        combined_indices = [i for i in indices if possible_values[i] in combined_values]
                        combined_weights = [weights[i] for i in combined_indices]
                        combined_plots[plot_num] = (list(combined_values), combined_weights)
                    else:
                        combined_plots[plot_num] = (possible_values, weights)
            values = ['L', 'I', 'G', 'O', 'E']    ##############################reset weights and Values
            weights = [20, 20, 20, 20, 20]
                    
            combined_plots_all = {key: value for key, value in combined_plots.items()}################################# A list with all possible values for all Plots
            sorted_dict_all = dict(sorted(combined_plots_all.items(), key=lambda x: len(x[1][0])))
            #print("Options_if_changes_neccessary:",sorted_dict_all)       
            
            combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}############### A list with all possible values for all Plots that havnt been assigned yet
            sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
            
            ############### Count the assignment Values
            if value=="L":  
                L_Count=L_Count+1                    
                
            elif value=="I":
                I_Count=I_Count+1
                
            elif value=="G":
                G_Count=G_Count+1
                
            elif value=="O":
                O_Count=O_Count+1
                
            elif value=="E":
                E_Count=E_Count+1
   
    print("LCount",L_Count)
    print("ICount",I_Count)  
    print("GCount",G_Count)  
    print("OCount",O_Count)  
    print("ECount",E_Count)  
    # print(C_Count)     
    # print(R_Count) 
    # print(I_Count) 
    # print(P_Count)
    #print("visited",visited)
    return dictionary, sorted_dict_all
##########################################################################################
def find_solution(dictionary: dict,
                max_time: float = 30) -> dict:
    """
    Generates solutions until a valid one is found or the time limit.
    is reached.
    """
    # Initialize the answer and the time
    answer, start = {}, time()

    # Set the stopping condition
    while answer == {} and (time() - start) < max_time:

        # Get a potential solution
        answer = random_distribution(dictionary)

    if answer == False:
        find_solution(dictionary,5)
    else:
        return answer
##########################################################################################
##########################################################################################
##########################################################################################
lines = [[[37.5, 69.5], [0.0, 77.0]], 
[[37.5, 69.5], [50.0, 67.0]], 
[[50.0, 67.0], [68.2098765432099, 63.35802469135802]], 
[[68.2098765432099, 63.35802469135802], [100.0, 57.0]], 
[[50.0, 0.0], [50.0, 42.91666666666668]], 
[[50.0, 42.91666666666668], [50.0, 67.0]], 
[[70.5, 100.0], [68.20987654320989, 63.35802469135802]], 
[[0.0, 22.083333333333332], [50.0, 42.916666666666686]], 
[[0, 0], [0.0, 22.083333333333332]], 
[[0.0, 22.083333333333332], [0.0, 77.0]], 
[[0.0, 77.0], [0, 100]], 
[[0, 100], [70.5, 100.0]], 
[[70.5, 100.0], [100,100]], 
[[100, 100], [100.0, 57.0]], 
[[100.0, 57.0], [100, 0]], 
[[100, 0], [50.0, 0.0]], 
[[50.0, 0.0], [0, 0]]]

# lines = [
# [[70.5, 100.0], [67.38502673796792, 50.160427807486634]], 
# [[67.38502673796792, 50.160427807486634], [64.25, 0.0]], 
# [[37.5, 69.5], [0.0, 77.0]], 
# [[37.5, 69.5], [68.20987654320987, 63.35802469135801]], 
# [[0.0, 22.083333333333332], [50.0, 42.91666666666667]], 
# [[50.0, 42.91666666666667], [67.38502673796792, 50.16042780748664]], 
# [[50.0, 0.0], [50.0, 42.91666666666668]], 
# [[0, 0], [0.0, 22.083333333333332]], 
# [[0.0, 22.083333333333332], [0.0, 77.0]], 
# [[0.0, 77.0], [0, 100]], 
# [[0, 100], [70.5, 100.0]], 
# [[70.5, 100.0], [100, 100]], 
# [[100, 100], [100, 0]], 
# [[100, 0], [64.25, 0.0]], 
# [[64.25, 0.0], [50.0, 0.0]], 
# [[50.0, 0.0], [0, 0]]
# ]

INPUT_LINES = [[(int(point[0]), int(point[1])) for point in line] for line in lines]
##########################################################################################
PLOTS= loop_finder(INPUT_LINES)
print("Plots:",PLOTS)
##########################################################################################
toplots = [[tuple(x) for x in sublist] for sublist in PLOTS]#Convert in Tuples
NEIGHBOURS = find_overlapping_plots(toplots)
print("Neighbours:",NEIGHBOURS)
##########################################################################################
DICTIONARY = convert_data(NEIGHBOURS)
DISTRIBUTION=find_solution(DICTIONARY)
#POSSIBLE_CHANGES=random_distribution(DICTIONARY)
print ("Distribution",DISTRIBUTION)
#print ("Possible Changes",POSSIBLE_CHANGES[1])

