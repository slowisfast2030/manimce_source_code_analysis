from manim import *

# 一个很聪明的方案
class ShowCreation(Create):
    pass

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

        #self.add(circle, radius_group)

        self.play(
            ShowCreation(radius_line),
            GrowFromCenter(radius_brace),
            Write(radius_label),
        )
        circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                radius_line, 2*np.pi-0.001, 
                about_point = circle.get_center(),
            ),
            ShowCreation(circle),
            run_time = 2
        )

        self.bring_to_front(radius_group)

        self.play(
            circle.animate.set_fill(fill_color, fill_opacity)
        )

        
