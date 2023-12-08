from manim import *

class s1(Scene):
    def construct(self):
        self.introduce_triangle()
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

        self.play(*ver_ani, run_time=2)