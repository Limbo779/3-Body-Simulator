import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# We'll use a class to maintain state across calls
class Animator:
    def __init__(self):
        self.x_list = []  # To collect x coordinates over time
        self.y_list = []  # To collect y coordinates over time
        self.is_started = False  # Flag to prevent multiple animations

    def animate(self, x=None, y=None, command=None):
        if command == 'Start':
            if self.is_started or not self.x_list or not self.y_list:
                print("Animation already started or no data collected.")
                return
            self.is_started = True
            
            # Create figure and axis
            fig, ax = plt.subplots()
            
            # Set axis limits with padding
            all_x = [xi for sublist in self.x_list for xi in sublist]
            all_y = [yi for sublist in self.y_list for yi in sublist]
            ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
            ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
            ax.set_aspect('equal')
            ax.set_title('3-Body Simulation Animation')
            
            # Initialize scatters for three bodies with different colors
            colors = ['red', 'blue', 'green']
            scatters = [ax.plot([], [], 'o', color=colors[i], markersize=8)[0] for i in range(3)]
            
            # Update function for animation
            def update(frame):
                for i in range(3):
                    scatters[i].set_data(self.x_list[frame][i], self.y_list[frame][i])
                return scatters
            
            # Create and show animation
            ani = animation.FuncAnimation(fig, update, frames=len(self.x_list), interval=50, blit=True)
            plt.show()
        
        else:
            # Collect data inside the loop (assume x and y are lists like [x1, x2, x3])
            if x is not None and y is not None:
                self.x_list.append(x)
                self.y_list.append(y)
            else:
                print("Please provide x and y lists when calling inside the loop.")

# Create an instance for Animation
animator = Animator()

def mod(x): # returns the modular of a vector
    return (np.dot(x,x))**(0.5)

# body 1
p1=np.random.randint(0,10,size=2)
m1=10
v1=np.array([0,0])

# body 2
p2=np.random.randint(0,10,size=2)
m2=10
v2=np.array([0,0])

# body 3
p3=np.random.randint(0,10,size=2)
m3=10
v3=np.array([0,0])

# G Const
G=1 #6.67430*(10**(-11)) is the actual value , but this is so small 
# small timestep
dt=0.01

# managing collision (when two bodies touch each they make elastic collision)
# they touch each other when they are below the distance of 2 btw each other (1 is their radius)
def collision(x):
    global v1,v2,v3
    # a means v1 and v2
    # b means v1 and v3
    # c means v2 and v3
    if x == "a":
        v1=v1*(-1)
        v2=v2*(-1)   
    elif x == "b":
        v1=v1*(-1)
        v3=v3*(-1)
    else:
        v3=v3*(-1)
        v2=v2*(-1)
for _ in range(3000):
    ra=(p2-p1) # vector btw body 1 and body 2 
    rb=(p3-p1) # vector btw body 1 and body 3
    rc=(p3-p2) # vector btw body 2 and body 3
    if mod(p1-p2) < 0.5 :
        collision("a")
    elif mod(p1-p3) < 0.5 :
        collision("b")
    elif mod(p3-p2) < 0.5 :
        collision("c")
    fa=(G*m1*m2*ra)/(mod(ra)**3) # force between body 1 and body 2
    fb=(G*m1*m3*rb)/(mod(rb)**3) # force between body 1 and body 3
    fc=(G*m3*m2*rc)/(mod(rc)**3) # force between body 2 and body 3
    
    # position and velocity updating
    
    # body 1
    p1 = p1+v1*dt+(((fa+fb)*(dt**2))/(2*m1))
    v1 = v1 + (((fa+fb)*dt)/m1)

    # body 2
    p2 = p2+v2*dt+(((fc-fa)*(dt**2))/(2*m2))
    v2 = v2 + (((fc-fa)*dt)/m2)

    # body 3
    p3 = p3+v3*dt+(((-fc-fb)*(dt**2))/(2*m3))
    v3 = v3 + (((-fc-fb)*dt)/m3)

    #plt.scatter([p1[0],p2[0],p3[0]],[p1[1],p2[1],p3[1]])
    x=[p1[0],p2[0],p3[0]]
    y=[p1[1],p2[1],p3[1]]
    
    animator.animate(x, y)

animator.animate(command='Start')    

