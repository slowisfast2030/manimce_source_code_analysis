from manim import *

class GetRiemannRectanglesExample(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], 
                  y_range=[0, 10, 1],
                  x_length=10,
                  y_length=5,
                  tips=False)
        quadratic = ax.plot(lambda x: 1.5 * x, x_range=[0, 7], color=TEAL)

        
        # the colour of rectangles below the x-axis is inverted
        # due to show_signed_area
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 7], dx=0.15, color=[BLUE, GREEN]
        )

        

        self.add(
            ax, rects_left, quadratic
        )