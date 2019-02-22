import pymunk               # Import pymunk..

space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0,0        # Set its gravity


space.fi
body = pymunk.Body(1,10)  # Create a Body with mass and moment
body.position = 50,100      # Set the position of the body

pymunk.Body.update_velocity(body,(5,2),1,2)


poly = pymunk.Poly.create_box(body) # Create a box shape and attach to body
space.add(body, poly)       # Add both body and shape to the simulation

x=5
y=5
for i in range(100):
    print(body.position)
    
    if x ==4:
        x=0
    if y ==4:
        y=0
    if i==0:
        x-=1
        y-=1
    

    print(x,y,body.angle)
    space.step(1)
    pymunk.Body.update_velocity(body,(x,y),.9,1)