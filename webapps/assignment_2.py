# Import javascript modules
from js import THREE, window, document, Object, console
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
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    global geom1_params

    geom1_params = {
        "i": 7,
        "size": 5
    }

    geom1_params = Object.fromEntries(to_js(geom1_params))
    # Geometry Creation
    
    global vertices, new_vertices, final_vertices
    
    vertices = []
    new_vertices = []
    final_vertices = []
    #Starting geometry (eqilateral triangle)
    ov1 = THREE.Vector3.new(0,5,0)
    ov2 = THREE.Vector3.new(4.33013,-2.5,0)
    ov3 = THREE.Vector3.new(-4.33013,-2.5,0)
    vertices.append(ov1)
    vertices.append(ov2)
    vertices.append(ov3)

    system(0, geom1_params.i)


    draw_system(final_vertices)


    #-----------------------------------------------------------------------
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Rules for generating Geometry
def generate():
    #Take every Line and transform it to have equilateral triangle in the middle
    for i in range(len(vertices)):
        #Usual case scenario
        if i < len(vertices)-1:
            
            vec_1 = vertices[i]
            vec_2 = vertices[i+1]
            temp1_vec = THREE.Vector3.new(0,0,0)
            dir_vec = temp1_vec.subVectors(vec_2,vec_1)
            dir_vec_l = dir_vec.length()
            dir_vec_x = dir_vec.getComponent(0)
            dir_vec_y = dir_vec.getComponent(1)
            temp2_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            temp3_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            temp4_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            dir_vec_1_3 = temp2_vec.setLength(dir_vec_l/3)
            dir_vec_1_3_l = dir_vec_1_3.length()            
            dir_vec_2_3 = temp3_vec.setLength(dir_vec_1_3_l*2)
            dir_vec_1_2 = temp4_vec.setLength(dir_vec_l/2)
            dir_x = dir_vec.getComponent(0)
            dir_y = dir_vec.getComponent(1)
            if dir_y != 0 and dir_x != 0:
                orth_vec = THREE.Vector3.new(dir_x,(-dir_x*dir_x)/dir_y,0)
            else:
                orth_vec = THREE.Vector3.new(dir_y,dir_x,0)
            orth_vec.setLength((dir_vec_1_3_l/2)*1.73205)
            #Generate final points for new geometry
            mid_p_vec = THREE.Vector3.new(0,0,0).addVectors(dir_vec_1_2,orth_vec)
            draw_p_1 = THREE.Vector3.new(0,0,0).addVectors(vec_1,dir_vec_1_3)
            draw_p_2 = THREE.Vector3.new(0,0,0).addVectors(vec_1,mid_p_vec)
            draw_p_3 = THREE.Vector3.new(0,0,0).addVectors(vec_1,dir_vec_2_3)
            
            
        #For the last point in list, which has to be paired up with the first of the list to create a closed line
        else:
            vec_1 = vertices[i]
            vec_2 = vertices[i-(len(vertices)-1)]
            temp1_vec = THREE.Vector3.new(0,0,0)
            dir_vec = temp1_vec.subVectors(vec_2,vec_1)
            dir_vec_l = dir_vec.length()
            dir_vec_x = dir_vec.getComponent(0)
            dir_vec_y = dir_vec.getComponent(1)
            temp2_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            temp3_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            temp4_vec = THREE.Vector3.new(dir_vec_x,dir_vec_y,0)
            dir_vec_1_3 = temp2_vec.setLength(dir_vec_l/3)
            dir_vec_1_3_l = dir_vec_1_3.length()            
            dir_vec_2_3 = temp3_vec.setLength(dir_vec_1_3_l*2)
            dir_vec_1_2 = temp4_vec.setLength(dir_vec_l/2)
            dir_x = dir_vec.getComponent(0)
            dir_y = dir_vec.getComponent(1)
            if dir_y != 0 and dir_x != 0:
                orth_vec = THREE.Vector3.new(dir_x,(-dir_x*dir_x)/dir_y,0)
            else:
                orth_vec = THREE.Vector3.new(dir_y,dir_x,0)
            orth_vec.setLength((dir_vec_1_3_l/2)*1.73205)
            #Generate final points for new geometry
            mid_p_vec = THREE.Vector3.new(0,0,0).addVectors(dir_vec_1_2,orth_vec)
            draw_p_1 = THREE.Vector3.new(0,0,0).addVectors(vec_1,dir_vec_1_3)
            draw_p_2 = THREE.Vector3.new(0,0,0).addVectors(vec_1,mid_p_vec)
            draw_p_3 = THREE.Vector3.new(0,0,0).addVectors(vec_1,dir_vec_2_3)

            
            

        #Add newly generated points to second helper-list
        new_vertices.append(vec_1)
        new_vertices.append(draw_p_1)
        new_vertices.append(draw_p_2)
        new_vertices.append(draw_p_3)
    
    #Add newly generated points to first helper-list as preparation for new iteration
    vertices.clear()
    vertices.extend(new_vertices)


        
#Recursive function which runs the generation-function as long as the max generation number isn't reached
def system(current_iteration, max_iteration):
    global vertices, new_vertices, final_vertices
    
    current_iteration += 1
    
    generate()
    #When threshhold of max generations is reached: second temporary point-list is added to final list
    if current_iteration >= max_iteration:
        final_vertices.extend(new_vertices)
        return final_vertices
    else:
        new_vertices.clear()
        return system(current_iteration, max_iteration)
    
#Turning the generated point-list into a drawn line
def draw_system(final_vertices):
    global vis_line
    #Draw geometry
    geom = THREE.BufferGeometry.new()
    final_vertices = to_js(final_vertices)
    geom.setFromPoints(final_vertices)
    material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
    vis_line = THREE.LineLoop.new( geom, material )

    global scene
    scene.add(vis_line)


#Space for potential GUI- might be added later (still WIP)!


# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
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
