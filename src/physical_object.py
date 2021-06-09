# author Eksoss/chicoviana #

from dataclasses import dataclass
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

@dataclass
class Physx:
    position: np.ndarray # (m, m, m)
    speed: np.ndarray # (m/s, m/s, m/s)
    mass: float # kg

    @property
    def energy(self, ):
        return self.mass * np.power(self.speed, 2).sum() / 2

    def apply_force(self, origin):
        self.speed += origin.force / self.mass

    def update(self, dt):
        self.position += self.speed * dt


@dataclass
class SpringProperties: # dunno if it's an abuse of properties
    fixed_point: np.ndarray
    free_point: np.ndarray
    neutral_length: float
    k: float

    @property
    def force(self, ):
        return - self.k * (self.length - self.neutral_length) * self.direction

    @property
    def direction(self, ):
        return (self.free_point - self.fixed_point) / self.length

    @property
    def length(self, ):
        return np.linalg.norm(self.free_point - self.fixed_point)
    

class PointObject(Physx):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Spring(SpringProperties):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
@dataclass
class GravityForce: # maybe it's a bad idea to make it this way
    acceleration: np.ndarray
    origin: PointObject

    @property
    def force(self, ):
        return self.acceleration * self.origin.mass
    
mola = Spring(fixed_point=np.zeros(3), free_point=np.ones(3), neutral_length=1., k=20.)

p1 = PointObject(position=np.array([0.5, 0., 0.]), speed=np.array([0., 0., 0.]), mass=10.)
p1_gravity = GravityForce(acceleration=np.array([0., -9.8, 0.]), origin=p1)

mola.free_point = p1.position
p1.apply_force(mola)

fig, ax = plt.subplots()

def animate(i):
    plt.clf()
    p1.update(0.01)
    mola.free_point = p1.position
    p1.apply_force(mola)
    p1.apply_force(p1_gravity)

    p1.speed *= 0.98

    plt.plot(*p1.position[:2], 'or', label='speed: %s'%np.array2string(p1.speed, formatter={'float': lambda x: "%.3f"%x}))
    plt.axis([-5., 5., -20., 5.])
    plt.plot([0, p1.position[0]], [0, p1.position[1]], 'b', alpha=0.5, label='length: %.3fm'%mola.length)

    plt.legend()
    plt.tight_layout()

    return fig, 


ani = animation.FuncAnimation(fig, animate, frames=300, interval=5)
# ani.save('test.gif')
plt.show()


