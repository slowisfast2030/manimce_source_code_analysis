from manim import *

"""
坐标系
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s3(Scene):
    def setup(self):
        self.coord_c = [-4,0,0]
        self.coord_a = [0,0,0]
        self.coord_b = [0,3,0]
        self.line_color = MAROON_B
        pass

    def construct(self):
        self.introduce_triangle()
        pass
        

    def introduce_triangle(self):
        triangle = Polygon(self.coord_c, self.coord_a, self.coord_b, color=self.line_color, stroke_width= 3)
        self.play(Write(triangle), run_time=2)

        ver_c = MathTex("C", color=WHITE).next_to(self.coord_c, DOWN)
        ver_a = MathTex("A", color=WHITE).next_to(self.coord_a, DOWN)
        ver_b = MathTex("B", color=WHITE).next_to(self.coord_b, RIGHT)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, run_time=1)
