from manim import *

class s1(Scene):
    def construct(self):
        self.introduce_triangle()
        self.introduce_half_angle()
        pass

    # 引入三角形
    def introduce_triangle(self):
        coord_c = [-4,0,0]
        coord_a = [0,0,0]
        coord_b = [0,3,0]
        triangle = Polygon(coord_c, coord_a, coord_b, color=RED)
        self.play(Write(triangle), run_time=2)

        ver_c = Tex("C", color=RED).next_to(coord_c, DOWN)
        ver_a = Tex("A", color=RED).next_to(coord_a, DOWN)
        ver_b = Tex("B", color=RED).next_to(coord_b, RIGHT)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, run_time=1)

        self.coord_c = coord_c
        self.coord_a = coord_a
        self.coord_b = coord_b
    
    def introduce_half_angle(self):
        self.coord_d = [0, 4/3, 0]
        half_line = Line(self.coord_c, self.coord_d, color=BLUE)
        self.play(Write(half_line), run_time=1)

        ver_d = Tex("D", color=BLUE).next_to(self.coord_d, RIGHT)
        self.play(FadeIn(ver_d), run_time=1)

        line_ca = Line(self.coord_c, self.coord_a, color=RED)
        line_cd = Line(self.coord_c, self.coord_d, color=BLUE)
        angle_half = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        self.play(Write(angle_half))