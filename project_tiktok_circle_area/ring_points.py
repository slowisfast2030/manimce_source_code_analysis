from manim import *

class BezierPointsOfCircle(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE, radius=3)
        self.add(circle)
        
        # Get all the points making up the cubic Bézier curves of the circle
        bezier_points = circle.get_points()
        
        # Iterate over each point and add a label
        for i, point in enumerate(bezier_points):
            dot = Dot(point, color=RED).scale(0.5)  # Create a small red dot at the point
            label = Text(f"{i}", font_size=24).next_to(dot, UP)  # Create a label with the index number
            self.add(dot, label)  # Add the dot and label to the scene

        self.wait()
