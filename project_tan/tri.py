from manim import *

class EquilateralTriangle(Scene):
    def construct(self):
        # Define the starting edge (line)
        start_edge = Line(LEFT+DOWN, RIGHT)
        self.add(start_edge)

        # Get the length of the starting edge
        edge_length = start_edge.get_length()

        # Create the other two sides of the equilateral triangle
        side2 = Line(start_edge.get_end(), start_edge.get_end() - edge_length * np.array([np.cos(PI/3), np.sin(PI/3), 0]))
        side3 = Line(side2.get_end(), start_edge.get_start())

        # Create the triangle
        triangle = VGroup(start_edge, side2, side3)

        # Display the triangle
        self.play(Create(triangle))
        self.wait()
