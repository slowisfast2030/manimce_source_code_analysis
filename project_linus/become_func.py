from manim import *

class BecomeScene(Scene):
    def construct(self):
        circ = Circle(fill_color=RED, fill_opacity=0.8)
        square = Square(fill_color=BLUE, fill_opacity=0.2)
        self.add(circ)
        self.wait(0.5)
        circ.become(square)
        self.wait(0.5)