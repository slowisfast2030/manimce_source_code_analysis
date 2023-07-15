from manim import *

class BecomeScene(Scene):
    def construct(self):
        circ = Circle(fill_color=RED, fill_opacity=0.8)
        square = Square(fill_color=YELLOW, fill_opacity=0.2)
        self.add(circ)
        self.wait(1)
        circ.become(square)
        self.wait(1)
        circ.pointwise_become_partial(square, 0, 0.6)
        self.wait(0.5)


class ExampleScene(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        # Show the circle
        self.add(circle)

        # Transition a portion of the circle to a square
        circle.pointwise_become_partial(square, 0, 0.5)

        # Wait for a moment
        self.wait()

        # Transition the rest of the circle to the square
        circle.pointwise_become_partial(square, 0.5, 1)

        # Wait for a moment
        self.wait()


class MyScene(Scene):
    def construct(self):
        # Create a VMobject
        my_vmobject = VMobject()

        # Add points to the VMobject
        my_vmobject.set_points_as_corners([ORIGIN, RIGHT, UP, LEFT-1, LEFT+DOWN+RIGHT])
        self.add(my_vmobject)
        self.wait(1)
        print("*"*100)
        print(my_vmobject.get_last_point())

        # Add a line to the VMobject
        my_vmobject.add_line_to(2*RIGHT)

        # Display the VMobject on the screen
        self.play(Create(my_vmobject))
        self.wait()