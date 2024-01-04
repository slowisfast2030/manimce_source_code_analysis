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
        self.dR = self.radius/15
        self.ring_colors = [BLUE, GREEN]

        self.radius_line_color = MAROON_B

        self.stroke_color = WHITE
        self.stroke_width = 1
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.unwrapped_tip = ORIGIN

        self.num_lines = 24
        self.line_color = BLACK

        self.ring_index_proportion = 0.6
        self.ring_shift_val = 5*DOWN


        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.move_to(ORIGIN)
        self.radius_line = Line(
            self.circle.get_center(),
            self.circle.get_right(),
            color = self.radius_line_color
        )
        self.radius_brace = Brace(self.radius_line, buff = SMALL_BUFF)
        self.radius_label = self.radius_brace.get_tex("R", buff = SMALL_BUFF)

        self.radius_group = VGroup(
            self.radius_line, self.radius_brace, self.radius_label
        )
        self.add(self.circle, *self.radius_group)

    def construct(self):
        self.introduce_circle()
        pass

    def introduce_circle(self):
        self.remove(self.circle)
        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
        )
        self.circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                self.radius_line, 2*PI-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            run_time = 1
        )

        # 当circle执行了set_fill的动画后会覆盖掉radius_group
        # 所以需要将radius_group放到circle的上面
        self.bring_to_front(self.radius_group)

        self.play(
            self.circle.animate.set_fill(self.fill_color, self.fill_opacity)
        )