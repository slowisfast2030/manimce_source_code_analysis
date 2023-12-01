from manim import *

class CircleArea(Scene):
    def construct(self):
        radius = 1.5
        stroke_color = WHITE
        fill_color = BLUE_E
        fill_opacity = 0.75
        circle_corner = UP + LEFT
        radial_line_color = MAROON_B


        circle = Circle(
            radius = radius,
            stroke_color = stroke_color,
            fill_color = fill_color,
            fill_opacity = fill_opacity,
        )
        circle.to_corner(circle_corner, buff = MED_LARGE_BUFF)
        
        radius_line = Line(
            circle.get_center(),
            circle.get_right(),
            color = radial_line_color
        )
        radius_brace = Brace(radius_line, buff = SMALL_BUFF)
        radius_label = radius_brace.get_tex("R", buff = SMALL_BUFF)

        radius_group = VGroup(
            radius_line, radius_brace, radius_label
        )

        self.add(circle, radius_group)
