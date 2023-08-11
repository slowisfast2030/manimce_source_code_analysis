from manim import *

class VMobjectDemo(Scene):
    def construct(self):
        plane = NumberPlane()
        my_vmobject = VMobject(color=GREEN)
        my_vmobject.points = [
            np.array([-0.8, -0.8, 0]),  # start of first curve
            np.array([-0.4, 0.4, 0]),
            np.array([0.4, -0.4, 0]),
            np.array([0.8, 0.8, 0])
          
        ]
        
        self.add(plane, my_vmobject)