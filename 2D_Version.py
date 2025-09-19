import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# We'll use a class to maintain state across calls
class Animator:
    def __init__(self):
        self.x_list = []  # List of [x1, x2, x3] for each time step
        self.y_list = []  # List of [y1, y2, y3] for each time step
        self.is_started = False
        self.ani = None

    def animate(self, x=None, y=None, command=None):
        if command == 'Start':
            if self.is_started or not self.x_list or not self.y_list:
                print("Animation already started or no data collected.")
                return
            self.is_started = True

            fig, ax = plt.subplots()
            colors = ['red', 'blue', 'green']
            scatters = [ax.plot([], [], 'o', color=colors[i], markersize=8)[0] for i in range(3)]
            trajectories = [ax.plot([], [], '-', color=colors[i], linewidth=1)[0] for i in range(3)]

            ax.set_aspect('equal')
            ax.set_title('3-Body Simulation Animation')

            def update(frame):
                for i in range(3):
                    scatters[i].set_data([self.x_list[frame][i]], [self.y_list[frame][i]])
                    traj_x = [pos[i] for pos in self.x_list[:frame+1]]
                    traj_y = [pos[i] for pos in self.y_list[:frame+1]]
                    trajectories[i].set_data(traj_x, traj_y)
                ax.relim()  # <-- recompute limits according to data
                ax.autoscale_view()  # <-- automatically scale the axes
                return scatters + trajectories

            self.ani = animation.FuncAnimation(
                fig, update, frames=len(self.x_list), interval=50, blit=False
            )
            plt.show()

        else:
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
p1=np.random.randint(0,30,size=2)
m1=10
v1=np.random.randint(-3,0,size=2)

# body 2
p2=np.random.randint(0,30,size=2)
m2=10
v2=np.random.randint(-3,3,size=2)

# body 3
p3=np.random.randint(0,30,size=2)
m3=10
v3=np.random.randint(0,3,size=2)

# G Const
G=1 #6.67430*(10**(-11)) is the actual value , but this is so small 
# small timestep
dt=0.01

# managing collision (when two bodies touch each they make elastic collision)
# they touch each other when they are below the distance of 2 btw each other (1 is their radius)
def collision(x):
    global v1,v2,v3,p1,p2,p3
    # a means v1 and v2
    # b means v1 and v3
    # c means v2 and v3
    if x == "a":
        n=(p2-p1)/mod(p2-p1)
        u1n=np.dot(v1,n)
        u2n=np.dot(v2,n)
        u1t=v1-u1n*n
        u2t=v2-u2n*n
        v1=(u2n*n)+u1t
        v2=(u1n*n)+u2t

    elif x == "b":
        n=(p3-p1)/mod(p3-p1)
        u1n=np.dot(v1,n)
        u3n=np.dot(v3,n)
        u1t=v1-u1n*n
        u3t=v3-u3n*n
        v1=(u3n*n)+u1t
        v3=(u1n*n)+u3t

    else:
        n=(p3-p2)/mod(p3-p2)
        u2n=np.dot(v2,n)
        u3n=np.dot(v3,n)
        u2t=v2-u2n*n
        u3t=v3-u3n*n
        v2=(u3n*n)+u2t
        v3=(u2n*n)+u3t

for _ in range(10000):
    ra=(p2-p1) # vector btw body 1 and body 2 
    rb=(p3-p1) # vector btw body 1 and body 3
    rc=(p3-p2) # vector btw body 2 and body 3
    if mod(p1-p2) < 0.1 :
        collision("a")
    elif mod(p1-p3) < 0.1 :
        collision("b")
    elif mod(p3-p2) < 0.1 :
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
