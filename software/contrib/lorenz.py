'''
Implementation of a simple Lorenz Attractor, see 

https://en.wikipedia.org/wiki/Lorenz_system

Default uses well known values of s=10,r=28,b=2.667. 
'''

class attractor:
    def __init__(self, point=(0.,1.,1.05), params=(10,28,2.667), dt=0.01):
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
        self.s = params[0]
        self.r = params[1]
        self.b = params[2]
        self.dt = dt
        self.x_min = self.x
        self.y_min = self.y
        self.z_min = self.z
        self.x_max = self.x
        self.y_max = self.y
        self.z_max = self.z
        # arbitrary initial range values    
        self.x_range = 100
        self.y_range = 100
        self.z_range = 100
        
    # The range of values produced depends on the parameters. If we
    # know the range, we can then normalise coordinates for use when
    # generating CV. This method runs through a number of iterations
    # to estimate ranges.
    def estimateRanges(self,steps=100000):
    
        # Execute a number of steps to get upper and lower bounds. 
        for i in range(steps):
            self.step()
            
            self.x_max = max(self.x, self.x_max)
            self.y_max = max(self.y, self.y_max)
            self.z_max = max(self.z, self.z_max)
            self.x_min = min(self.x, self.x_min)
            self.y_min = min(self.y, self.y_min)
            self.z_min = min(self.z, self.z_min)

        self.x_range = self.x_max-self.x_min
        self.y_range = self.y_max-self.y_min
        self.z_range = self.z_max-self.z_min

    def x_scaled(self):
        return (100.0 * (self.x - self.x_min))/self.x_range

    def y_scaled(self):
        return (100.0 * (self.y - self.y_min))/self.y_range

    def z_scaled(self):
        return (100.0 * (self.z - self.z_min))/self.z_range
    
    def __str__(self):
        return (f"({self.x:2.2f},{self.y:2.2f},{self.z:2.2f})({self.s},{self.r},{self.b})")

    def step(self):
        '''
        Update the point.
        '''
        x_dot = self.s*(self.y - self.x)
        y_dot = self.r*self.x - self.y - self.x*self.z
        z_dot = self.x*self.y - self.b*self.z
        self.x += x_dot * self.dt
        self.y += y_dot * self.dt
        self.z += z_dot * self.dt

def main():
    a = attractor()
    a.estimateRanges()
    print(a)
    print(f"Min x:{a.x_min:8.2f} y:{a.y_min:8.2f} z:{a.z_min:8.2f}")
    print(f"Max x:{a.x_max:8.2f} y:{a.y_max:8.2f} z:{a.z_max:8.2f}")
    print(f"Ran x:{a.x_range:8.2f} y:{a.y_range:8.2f} z:{a.z_range:8.2f}")

if __name__ == "__main__":
    main()

