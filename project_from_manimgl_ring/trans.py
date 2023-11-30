from manim import *

class test(Scene):
    def construct(self):
        # Create a triangle with points arranged clockwise
        triangle_cw = Polygon(
            UP, 
            RIGHT, 
            LEFT
        ).set_color(RED).set_fill(RED, 0.5)

        # Create a triangle with points arranged counterclockwise
        triangle_ccw = Polygon(
            UP, 
            LEFT, 
            RIGHT
        ).set_color(BLUE).set_fill(BLUE, 0.5).shift(DOWN)
        #.rotate(PI, UP)

        self.play(Create(triangle_cw))
        self.wait(1)

        # Transform to the counterclockwise triangle
        self.play(Transform(triangle_cw, triangle_ccw))
        self.wait(1)
