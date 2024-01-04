from manim import *

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class ShowCreation(Create):
    pass

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

        self.num_lines = 24

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
        self.try_to_understand_area()


    def try_to_understand_area(self):
        line_sets = [
            VGroup(*[
                Line(
                    self.circle.point_from_proportion(alpha),
                    self.circle.point_from_proportion(func(alpha)),
                )
                for alpha in np.linspace(0, 1, self.num_lines)
            ])
            for func in [
                lambda alpha : 1-alpha,
                lambda alpha : (0.5-alpha)%1,
                lambda alpha : (alpha + 0.4)%1,
                lambda alpha : (alpha + 0.5)%1,
            ]
        ]
        for lines in line_sets:
            lines.set_stroke(BLACK, 2)
        lines = line_sets[0]

        self.play(
            ShowCreation(
                lines, 
                run_time = 2, 
                lag_ratio = 0.5
            )
        )
        self.wait(2)
        for new_lines in line_sets[1:]:
            self.play(
                Transform(lines, new_lines),
            )
            self.wait()
        self.wait()
        self.play(FadeOut(lines))