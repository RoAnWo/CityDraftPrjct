# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls, composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new("#cccfb3")
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 300
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
    # Declare Parameters
    global geom1_params, cubes, cube_lines
    cubes = []
    cube_lines = []
    geom1_params = {
        "size": 30,
        "amount": 5,
        "x": -150,
        "y": -150,
        "z": 300,
    }

    geom1_params = Object.fromEntries(to_js(geom1_params))

    #Create Material
    global material, line_material
    color = THREE.Color.new("#33304c")
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 1
    material.color = color

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new("#FA8072")


    
    #Generate the Boxes using for loops
    for z2 in range(geom1_params.amount):
        for y2 in range(geom1_params.amount):
            for x2 in range(geom1_params.amount):
                
                #Create boxes
                geom = THREE.BoxGeometry.new(geom1_params.size, geom1_params.size, geom1_params.size)
                
                #Create Vector for attractor point
                attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                attractor_len = attractor.length()               

                #Get translation points for first translation
                if attractor_len < 350:
                    attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                else:
                    attractor.setLength(0)
                
                trans_x = attractor.getComponent(0)
                trans_y = attractor.getComponent(1)
                trans_z = attractor.getComponent(2)

                #New distance from attractor point after translation
                geom_pos_x = (x2*30)+trans_x
                geom_pos_y = (y2*30)+trans_y
                geom_pos_z = (z2*30)+trans_z

                attractor_new = THREE.Vector3.new(geom1_params.x-geom_pos_x,geom1_params.z-geom_pos_y,geom1_params.y-geom_pos_z)
                attractor_new_len = attractor_new.length()

                #Scaling object, smaller when closer to attractor
                if attractor_new_len < 350:
                    scale_vec = 0.003*attractor_new_len+0.007
                else:
                    scale_vec = 1
                
                #Constructing Objects again using new scale
                geom = THREE.BoxGeometry.new(geom1_params.size*scale_vec, geom1_params.size*scale_vec, geom1_params.size*scale_vec)

                #Create Vector for attractor point
                attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                attractor_len = attractor.length()

               
                #Translating objects to radiate towards attractor point
                if attractor_len < 350:
                    attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                else:
                    attractor.setLength(0)
                
                trans_x = attractor.getComponent(0)
                trans_y = attractor.getComponent(1)
                trans_z = attractor.getComponent(2)

                geom.translate((x2*30)+trans_x,(y2*30)+trans_y,(z2*30)+trans_z)

                #Adding objects to scene
                cube = THREE.Mesh.new(geom, material)
                cubes.append(cube)
                scene.add(cube)

                # draw the edge geometries of the cube
                edges = THREE.EdgesGeometry.new( cube.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                cube_lines.append(line)
                scene.add( line )





    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'size', 5,30,1)
    param_folder.add(geom1_params, 'amount', 1,15,1)
    param_folder.add(geom1_params,"x", -150,400,10)
    param_folder.add(geom1_params,"y", -150,400,10)
    param_folder.add(geom1_params,"z", -150,400,10)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS

#Update the cube
def update_cubes():
    global cubes, cube_lines, material, line_material
    
    #make sure you dont have 0 cubes
    if len(cubes) !=0:

        #See if slider was moved, update whole process or just the geometry as a result
        if len(cubes) != geom1_params.x:
            for cube in cubes: scene.remove(cube)
            for line in cube_lines: scene.remove(line)

            cubes = []
            cube_lines = []

            for z2 in range(geom1_params.amount):
                for y2 in range(geom1_params.amount):
                    for x2 in range(geom1_params.amount):
                        
                        #Create Geometry
                        geom = THREE.BoxGeometry.new(geom1_params.size, geom1_params.size, geom1_params.size)
                        
                        #Create Vector for attractor point
                        attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                        attractor_len = attractor.length()               

                        #Translating objects to radiate towards attractor point
                        if attractor_len < 350:
                            attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                        else:
                            attractor.setLength(0)
                        
                        trans_x = attractor.getComponent(0)
                        trans_y = attractor.getComponent(1)
                        trans_z = attractor.getComponent(2)

                        #New distance from attractor point after translation
                        geom_pos_x = (x2*30)+trans_x
                        geom_pos_y = (y2*30)+trans_y
                        geom_pos_z = (z2*30)+trans_z

                        attractor_new = THREE.Vector3.new(geom1_params.x-geom_pos_x,geom1_params.z-geom_pos_y,geom1_params.y-geom_pos_z)
                        attractor_new_len = attractor_new.length()

                        #Scaling object, smaller when closer to attractor
                        if attractor_new_len < 350:
                            scale_vec = 0.003*attractor_new_len+0.007
                        else:
                            scale_vec = 1
                        
                        geom = THREE.BoxGeometry.new(geom1_params.size*scale_vec, geom1_params.size*scale_vec, geom1_params.size*scale_vec)

                        #Create Vector for attractor point
                        attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                        attractor_len = attractor.length()

                    
                        #Translating objects to radiate towards attractor point
                        if attractor_len < 350:
                            attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                        else:
                            attractor.setLength(0)
                        
                        trans_x = attractor.getComponent(0)
                        trans_y = attractor.getComponent(1)
                        trans_z = attractor.getComponent(2)

                        geom.translate((x2*30)+trans_x,(y2*30)+trans_y,(z2*30)+trans_z)

                        #Adding objects to scene
                        cube = THREE.Mesh.new(geom, material)
                        cubes.append(cube)
                        scene.add(cube)

                        # draw the edge geometries of the cube
                        edges = THREE.EdgesGeometry.new( cube.geometry )
                        line = THREE.LineSegments.new( edges, line_material)
                        cube_lines.append(line)
                        scene.add( line )
        else:
            for i in range(len(cubes)):
                cube = cubes[i]
                line = cube_lines[i]

                 #Create Geometry
                geom = THREE.BoxGeometry.new(geom1_params.size, geom1_params.size, geom1_params.size)
                
                #Create Vector for attractor point
                attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                attractor_len = attractor.length()               

                #Translating objects to radiate towards attractor point
                if attractor_len < 350:
                    attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                else:
                    attractor.setLength(0)
                
                trans_x = attractor.getComponent(0)
                trans_y = attractor.getComponent(1)
                trans_z = attractor.getComponent(2)

                #New distance from attractor point after translation
                geom_pos_x = (x2*30)+trans_x
                geom_pos_y = (y2*30)+trans_y
                geom_pos_z = (z2*30)+trans_z

                attractor_new = THREE.Vector3.new(geom1_params.x-geom_pos_x,geom1_params.z-geom_pos_y,geom1_params.y-geom_pos_z)
                attractor_new_len = attractor_new.length()

                #Scaling object, smaller when closer to attractor
                if attractor_new_len < 350:
                    scale_vec = 0.003*attractor_new_len+0.007
                else:
                    scale_vec = 1
                
                geom = THREE.BoxGeometry.new(geom1_params.size*scale_vec, geom1_params.size*scale_vec, geom1_params.size*scale_vec)

                #Create Vector for attractor point
                attractor = THREE.Vector3.new(geom1_params.x-(x2*30),geom1_params.z-(y2*30),geom1_params.y-(z2*30))
                attractor_len = attractor.length()

            
                #Translating objects to radiate towards attractor point
                if attractor_len < 350:
                    attractor.setLength(attractor_len-(attractor_len/49.7)**3)
                else:
                    attractor.setLength(0)
                
                trans_x = attractor.getComponent(0)
                trans_y = attractor.getComponent(1)
                trans_z = attractor.getComponent(2)

                geom.translate((x2*30)+trans_x,(y2*30)+trans_y,(z2*30)+trans_z)

                #Adding objects to scene
                cube = THREE.Mesh.new(geom, material)
                cubes.append(cube)
                scene.add(cube)

                # draw the edge geometries of the cube
                edges = THREE.EdgesGeometry.new( cube.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                cube_lines.append(line)
                scene.add( line )






# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_cubes()
    controls.update()
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
