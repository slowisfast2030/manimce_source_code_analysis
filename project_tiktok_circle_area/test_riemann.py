from manim import *

class GetRiemannRectanglesExample(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], 
                  y_range=[0, 10, 1],
                  x_length=5,
                  y_length=5,
                  tips=False,
                  axis_config={"include_numbers": True})
        quadratic = ax.plot(lambda x: 1 * x, x_range=[0, 10], color=TEAL)

        
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 10], dx=0.2, color=[BLUE, GREEN]
        )

        self.add(
            ax, rects_left, quadratic
        )