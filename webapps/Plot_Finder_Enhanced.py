# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math, random, itertools
from random import choices,choice
from time import time
import numpy as np
from typing import List


#from random import randint

	
#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
# global geom1_params
# geom1_params = {
#     "size" : 1,
#     }
# geom1_params = Object.fromEntries(to_js(geom1_params))

def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 9999)
    camera.position.z = 100
    scene.add(camera)
    
    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
   



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
        values = ['G', 'C', 'R', 'I', 'P']
        weights = [20, 20, 20, 20, 20]
        G_Count=0
        C_Count=0
        R_Count=0
        I_Count=0
        P_Count=0
       
       # Get the first plot in the dictionary
        first_plot = list(dictionary.keys())[0]

        # Choose a random value from the list of possible values
        value = choice(['G', 'C', 'R', 'I', 'P'])

        # Assign the random value to the first plot
        dictionary[first_plot]['value'] = value
        #print (value)
      
       # Loop through the plots
        for plot in dictionary.keys():
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
                if dictionary[neighbor]['value'] == 'R':
                    while "I" in values:
                        index= values.index("I")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                elif dictionary[neighbor]['value'] == 'I':
                    while "R" in values:
                        index= values.index("R")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                    # while "C" in values:
                    #     index= values.index("C")
                    #     if index < len(values):
                    #         values.pop(index)
                    #         weights.pop(index)
                    while "P" in values:
                        index= values.index("P")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                elif dictionary[neighbor]['value'] == 'P':
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
                if C_Count >= 4:
                    while "C" in values:
                        index= values.index("C")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                if R_Count == 1:
                    while "R" in values:
                        index= values.index("R")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                if I_Count >= 4:
                    while "I" in values:
                        index= values.index("I")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
                if P_Count >= 1:
                    while "P" in values:
                        index= values.index("P")
                        if index < len(values):
                            values.pop(index)
                            weights.pop(index)
            # Assign a value to the plot, using weighted probability
            #print(len(values))
            if(len(values))>=1:
                value = choices(values, weights=weights, k=1)[0]
                
                # Assign the value to the plot
                dictionary[plot]['value'] = value
                
            else:
                for plot in dictionary.keys():
                    # Set the value to None
                    
                    dictionary[plot]['value'] = None
                    print (dictionary)
                return False 

            #Count the Assigned Values
            if value=="G":
                G_Count=G_Count+1                    
                
            elif value=="C":
                C_Count=C_Count+1
                
            elif value=="R":
                R_Count=R_Count+1
                
            elif value=="I":
                I_Count=I_Count+1
                
            elif value=="P":
                P_Count=P_Count+1
        # print(G_Count)  
        # print(C_Count)     
        # print(R_Count) 
        # print(I_Count) 
        # print(P_Count) 
        return dictionary










    








    
        
    


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
            print(f'\nA valid solution was found in {round(time() - start, 5)} seconds.')
            return answer


    

    # Assign equal weights to each value
    

        # Set an example 
    LIST_NEIGHBOURS = [[1, [2, 6]],
                        [2, [1, 5, 3]],
                        [3, [2, 5, 4]],
                        [4, [3, 5, 8]],
                        [5, [2, 4, 7, 8]],
                        [6, [1, 7]],
                        [7, [5, 6, 8, 10]],
                        [8, [4, 5, 7, 9]],
                        [9, [8, 10]],
                        [10, [7, 9]]]

        # Convert the list
    DICTIONARY = convert_data(LIST_NEIGHBOURS)
   
    # Plot1 = [np.array([0,0]),np.array([0,22.08333333]),np.array([67.38502674,50.16042781]),np.array([100,63.75]),np.array([100,0])]
    # Plot2 = [np.array([0,22.08333333]),np.array([0,77]),np.array([68.20987654, 63.35802469]),np.array([67.38502674,50.16042781])]
    # Plot3 = [np.array([0,77]),np.array([100,0]),np.array([70.5, 100]),np.array([68.20987654, 63.35802469])]
    # Plot4 = [np.array([70.5, 100]),np.array([100,100]),np.array([100,63.75]),np.array([67.38502674,50.16042781]),np.array([68.20987654, 63.35802469])]
    # Plot1Nachbarn = ["Plot2","Plot4"]
    # Plot2Nachbarn = ["Plot1","Plot3","Plot4"]
    # Plot3Nachbarn = ["Plot2","Plot4"]
    # Plot4Nachbarn = ["Plot1","Plot2","Plot3"]
        # Convert the list       

   

    # Search a solution under 5 seconds
    ANSWER = find_solution(DICTIONARY, max_time=15)


    if ANSWER is not None:
        print(f'The valid solution is: {ANSWER}.')
        




    PLOT_POINT_LIST = [
    [[0,0],[2,2],[2,0],[0,0]],#1
    [[6,0],[2,0],[2,2],[6,2],[6,0]],#2
    [[6,0],[6,2],[8,3],[9,1],[8,0],[6,0]],#3
    [[6,4],[6,5],[8,5],[8,3],[6,2],[6,4]],#4
    [[6,4],[3,4],[2,2],[6,2],[6,4]],#5
    [[0,0],[0,3],[2,2],[0,0]],#6
    [[0,3],[2,2],[3,4],[3,5],[0,5],[0,3]],#7
    [[6,4],[6,5],[3,5],[3,4],[6,4]],#8
    [[6,5],[3,5],[3,7],[6,5]],#9
    [[0,7],[0,5],[3,5],[3,7],[0,7]]]#10

    #print(PLOT_POINT_LIST)
    


    #Turning the generated point-list into a drawn line
    def draw_system(lines):
        #print (lines)
        for points in lines:
            line_geom = THREE.BufferGeometry.new()
            points = to_js(points)
            
            line_geom.setFromPoints( points )

            material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
            
            vis_line = THREE.Line.new( line_geom, material )
            
            global scene
            scene.add(vis_line)  
            
    
    
    
    ThreeCurrentLine = []
    
    ThreeLines = []
    
    for i in PLOT_POINT_LIST:
        for TempArrayToList in i:
            # to array
            #print(TempArrayToList)
            #TempArrayToList =Array.tolist() 
            
            #print (TempArrayToList)
            ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
            ThreeCurrentLine.append(ThreeVec1)
        ThreeLines.append (ThreeCurrentLine)
        ThreeCurrentLine = []
    draw_system(ThreeLines)
    
        
   
            
         



   
   


    


		














  
    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # # Set up GUI
    # gui = window.dat.GUI.new()
    # param_folder = gui.addFolder('Parameters')
    # param_folder.add(geom1_params, 'size', 1,6,1)
    
    # param_folder.open()
    
    
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS


#print(Maximum,geom1_params.size)

#### update   


# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    #update()
    composer.render()
    

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
