from manim import *

class GetRiemannRectanglesExample(Scene):
        def construct(self):
            ax = Axes(y_range=[-2, 10])
            quadratic = ax.plot(lambda x: 0.5 * x ** 2 - 0.5)

            # the rectangles are constructed from their top right corner.
            # passing an iterable to `color` produces a gradient
            rects_right = ax.get_riemann_rectangles(
                quadratic,
                x_range=[-4, -3],
                dx=0.25,
                color=(TEAL, BLUE_B, DARK_BLUE),
                input_sample_type="right",
            )

            # the colour of rectangles below the x-axis is inverted
            # due to show_signed_area
            rects_left = ax.get_riemann_rectangles(
                quadratic, x_range=[-1.5, 1.5], dx=0.15, color=YELLOW
            )

            bounding_line = ax.plot(
                lambda x: 1.5 * x, color=BLUE_B, x_range=[3.3, 6]
            )
            bounded_rects = ax.get_riemann_rectangles(
                bounding_line,
                bounded_graph=quadratic,
                dx=0.15,
                x_range=[4, 5],
                show_signed_area=False,
                color=(MAROON_A, RED_B, PURPLE_D),
            )

            self.add(
                ax, bounding_line, quadratic, rects_right, rects_left, bounded_rects
            )

            self.wait(3)

class myScene(Scene):
    def construct(self):
        points = [ORIGIN, UP, RIGHT, LEFT]
        dots = VMobject()
        dots.set_points_smoothly(points)
        self.add(dots)
        self.play(Create(dots))
        self.wait()

        dots2 = VMobject()
        dots2.set_points_as_corners(points)
        self.add(dots2)
        self.play(Create(dots2))
        self.wait()

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