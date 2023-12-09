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
        self.label_color = WHITE

        self.coord_d = [0, 4/3, 0]
        self.coord_e = [-4/5, 12/5, 0]
        self.coord_f = [1, 0, 0]

        self.shift_vector = np.array([-2, 1.5, 0]) - 3*UP
        self.coord_c_shift = np.array(self.coord_c) - self.shift_vector
        self.coord_a_shift = np.array(self.coord_a) - self.shift_vector
        self.coord_b_shift = np.array(self.coord_b) - self.shift_vector
        pass

    def construct(self):
        self.opening()
        #self.introduce_triangle()
        #self.introduce_coordinate()
        #self.two_geometry()
        pass
        
    # 开场
    # 屏幕中间出现一个三角形，屏幕下方出现pi生物
    def opening(self):
        # 引入三角形
        triangle = Polygon(self.coord_c_shift, 
                           self.coord_a_shift, 
                           self.coord_b_shift, 
                           color=self.line_color, stroke_width=3).set_z_index(1)
        ver_c = MathTex("C", color=self.label_color).next_to(self.coord_c_shift, DOWN).set_z_index(1)
        ver_a = MathTex("A", color=self.label_color).next_to(self.coord_a_shift, DOWN).set_z_index(1)
        ver_b = MathTex("B", color=self.label_color).next_to(self.coord_b_shift, RIGHT).set_z_index(1)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, 
                  ShowCreation(triangle),
                  run_time=1)
        self.wait()
        
        tri_gr = VGroup(triangle, ver_c, ver_a, ver_b)
        # 引入坐标平面
        # 将整个画面网上提一点，为下方的pi生物让出空间
        plane = NumberPlane().shift(3*UP)
        self.play(Write(plane), 
                  run_time=1)
        self.wait()
        
        # 淡出pi生物, 将整个场景移到屏幕中间
        self.play(plane.animate.shift(-plane.get_center()),
                tri_gr.animate.shift(-self.coord_a_shift),
                  run_time=1)
        self.wait()

        pass

    def introduce_triangle(self):
        plane = NumberPlane()
        self.play(Write(plane), run_time=1)

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
        # plane = NumberPlane()
        # self.play(Write(plane), run_time=2)

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
        c_a = [-1.4, -1, 0]
        c_b = [1.1, -1.4, 0]
        c_c = [0, 1.2, 0]
        triangle = Polygon(c_a, c_b, c_c, color=self.line_color, stroke_width=3)
        self.play(Write(triangle), run_time=1)

        ver_a = MathTex("A", color=WHITE).next_to(c_a, DOWN)
        ver_b = MathTex("B", color=WHITE).next_to(c_b, DOWN)
        ver_c = MathTex("C", color=WHITE).next_to(c_c, UP)
        ver_ani = list(map(FadeIn, [ver_a, ver_b, ver_c]))
        self.play(*ver_ani, run_time=1)

        tri_bc = self.get_equilateral_triangle(Line(c_b, c_c))
        dot_e_label = MathTex("E", color=WHITE).next_to(tri_bc[2], RIGHT)

        tri_ca = self.get_equilateral_triangle(Line(c_c, c_a))
        dot_d_label = MathTex("D", color=WHITE).next_to(tri_ca[2], LEFT)

        tri_ab = self.get_equilateral_triangle(Line(c_a, c_b))
        dot_f_label = MathTex("F", color=WHITE).next_to(tri_ab[2], DOWN)

        self.play(Write(dot_e_label), Write(dot_d_label), Write(dot_f_label), run_time=1)

        self.play(ShowCreation(tri_bc[0].reverse_points()),
                  ShowCreation(tri_bc[1]),
                    ShowCreation(tri_ca[0].reverse_points()),
                    ShowCreation(tri_ca[1]),
                    ShowCreation(tri_ab[0].reverse_points()),
                    ShowCreation(tri_ab[1]),
                    run_time=1)
        
        # 显示费马点
        line_ae = Line(c_a, tri_bc[2].get_center(), color=BLUE_C)
        line_bd = Line(c_b, tri_ca[2].get_center(), color=BLUE_C)
        line_cf = Line(c_c, tri_ab[2].get_center(), color=BLUE_C)

        self.play(ShowCreation(line_ae),
                    ShowCreation(line_bd),
                    ShowCreation(line_cf),
                    run_time=1) 
        
    def get_equilateral_triangle(self, line):
        # 将line顺指针和逆时针各旋转一次
        start = line.get_start()
        end = line.get_end() 
        
        # 以start为旋转中心，顺时针旋转PI/3
        line1 = Line(start, end).copy().set_color(WHITE)
        line1.rotate(-PI/3, about_point=start) 
        # 将end也顺时针旋转PI/3
        dot = Dot(end)
        dot.rotate(-PI/3, about_point=start)

        # 以end为旋转中心，逆时针旋转PI/3
        line2 = Line(start, end).copy().set_color(WHITE)
        line2.rotate(PI/3, about_point=end)

        return VGroup(line1, line2, dot)






