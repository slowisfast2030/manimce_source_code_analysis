from manim import *

class GetRiemannRectanglesExample(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])
        quadratic = ax.plot(lambda x: 1.5 * x)

        
        # the colour of rectangles below the x-axis is inverted
        # due to show_signed_area
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 7], dx=0.15, color=[BLUE, GREEN]
        )

        

        self.add(
            ax, quadratic, rects_left
        )