from manim import *

"""
辅助圆
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class s2(Scene):
    def setup(self):
        pass

    def construct(self):
        self.diameter_angle()
        pass

    # 直径所对的圆周角是直角
    def diameter_angle(self):
        circle = Circle(radius=2, color=RED, stroke_width=2)
        self.play(Write(circle), run_time=1)
        self.wait()

        diameter = Line(LEFT*2, RIGHT*2, color=BLUE)
        self.play(Write(diameter), run_time=1)
        self.wait()

        