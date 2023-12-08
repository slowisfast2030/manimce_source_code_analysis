from manim import *

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class s1(Scene):
    def construct(self):
        self.introduce_triangle()
        self.introduce_half_angle()
        self.tri_flip()
        pass

    # 引入三角形
    def introduce_triangle(self):
        coord_c = [-4,0,0]
        coord_a = [0,0,0]
        coord_b = [0,3,0]
        triangle = Polygon(coord_c, coord_a, coord_b, color=RED)
        self.play(Write(triangle), run_time=2)

        ver_c = MathTex("C", color=RED).next_to(coord_c, DOWN)
        ver_a = MathTex("A", color=RED).next_to(coord_a, DOWN)
        ver_b = MathTex("B", color=RED).next_to(coord_b, RIGHT)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, run_time=1)

        self.coord_c = coord_c
        self.coord_a = coord_a
        self.coord_b = coord_b
    
    # 引入半角
    def introduce_half_angle(self):
        self.coord_d = [0, 4/3, 0]
        half_line = Line(self.coord_c, self.coord_d, color=BLUE)
        self.play(Write(half_line), run_time=1)

        ver_d = MathTex("D", color=BLUE).next_to(self.coord_d, RIGHT)
        self.play(FadeIn(ver_d), run_time=1)

        line_ca = Line(self.coord_c, self.coord_a, color=RED)
        line_cd = Line(self.coord_c, self.coord_d, color=BLUE)
        angle_half = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        label_angle_half = MathTex(r"\alpha").next_to(angle_half, RIGHT).scale(0.8).shift(0.05*UP)

        self.play(Write(angle_half), Write(label_angle_half), run_time=1)

    # 翻转动画
    def tri_flip(self):
        flip_axis = np.array(self.coord_c) - np.array(self.coord_d)
        flip_point = self.coord_c
        flip_tri = Polygon(self.coord_c, self.coord_a, self.coord_d, color=GREEN)
        self.play(flip_tri.animate.rotate(PI, axis=flip_axis, about_point=flip_point))
        
        self.coord_e = [-4/5, 12/5, 0]
        ver_e = MathTex("E", color=GREEN).next_to(self.coord_e, 0.5*(LEFT+UP))
        self.play(FadeIn(ver_e), run_time=1)
