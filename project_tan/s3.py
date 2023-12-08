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

        self.coord_d = [0, 4/3, 0]
        self.coord_e = [-4/5, 12/5, 0]
        self.coord_f = [1, 0, 0]
        pass

    def construct(self):
        self.introduce_triangle()
        self.introduce_coordinate()
        self.two_geometry()
        pass
        
    def introduce_triangle(self):
        triangle = Polygon(self.coord_c, self.coord_a, self.coord_b, color=self.line_color, stroke_width= 3)
        self.play(Write(triangle), run_time=2)

        ver_c = MathTex("C", color=WHITE).next_to(self.coord_c, DOWN)
        ver_a = MathTex("A", color=WHITE).next_to(self.coord_a, DOWN)
        ver_b = MathTex("B", color=WHITE).next_to(self.coord_b, RIGHT)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, run_time=1)

        self.triangle = triangle

    # 添加坐标系
    def introduce_coordinate(self):
        plane = NumberPlane()
        self.play(Write(plane), run_time=2)

        # 显示角平分线
        half_line = Line(self.coord_c, self.coord_d, color=self.line_color)
        ver_d = MathTex("D", color=WHITE).next_to(self.coord_d, RIGHT)
        self.play(ShowCreation(half_line), run_time=1)
        self.play(Write(ver_d), run_time=1)

        # 显示直线CD的垂线
        line_ef = Line(self.coord_e, self.coord_f, color=self.line_color)
        ver_e = MathTex("E", color=WHITE).next_to(self.coord_e, LEFT)
        ver_f = MathTex("F", color=WHITE).next_to(self.coord_f, DOWN)

        self.play(GrowFromPoint(line_ef, self.coord_d), run_time=1)
        self.play(Write(ver_e), Write(ver_f), run_time=1)

    # 以费马点的例子介绍两种几何
    def two_geometry(self):
        self.clear()
        c_a = [-1.2, -0.8, 0]
        c_b = [1, -1.2, 0]
        c_c = [0, 1.2, 0]
        triangle = Polygon(c_a, c_b, c_c, color=self.line_color, stroke_width=3)
        self.play(Write(triangle), run_time=1)





