from manim import *

class s3(Scene):
    def setup(self):
        self.radius = 2
        self.dR = 2/60
        self.ring_colors = [BLUE, GREEN]

        self.stroke_color = WHITE
        self.stroke_width = 1
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.unwrapped_tip = ORIGIN

    def construct(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(UP, buff = MED_LARGE_BUFF*4)
        self.add(self.circle)
