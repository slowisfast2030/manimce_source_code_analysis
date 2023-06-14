from manim import *

class CircleAndSquare(Scene):
    def construct(self):
        circle = Circle(color=RED, radius=1)
        square = Square(color=BLUE, side_length=2)
        circle.shift(LEFT*3)
        square.shift(RIGHT*3)
        self.add(circle, square)

        # Set the square as the target for the circle
        circle.target = square

        # Create the animation
        self.play(MoveToTarget(circle))

with tempconfig({"quality": "medium_quality", "preview": True}):
    scene = CircleAndSquare()
    scene.render()