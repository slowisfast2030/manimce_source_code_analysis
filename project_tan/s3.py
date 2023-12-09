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
        self.introduce_vertical_line() 
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
        
        """重要！！！
        此时, 这里需要剪辑技巧
        新建一个场景, 专门解释平面几何和解析几何
        将这个场景剪辑到这里
        然后再执行下面的代码
        """

        # 淡出pi生物, 将整个场景移到屏幕中间
        self.play(plane.animate.shift(-plane.get_center()),
                  tri_gr.animate.shift(-self.coord_a_shift),
                  run_time=1)
        self.wait()

        self.tri_gr = tri_gr
        self.plane = plane
        pass


    # 添加坐标系
    def introduce_vertical_line(self):

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


class pr(s3):
    def construct(self):

        self.two_geometry() 
        self.two_geometry_example()
        pass

    # 引入两种几何
    def two_geometry(self):
        svg_compass = SVGMobject("compass.svg").set_color(GREEN_B)
        svg_ruler = SVGMobject("ruler.svg").set_color(TEAL_E).match_height(svg_compass)
        svg_gr = VGroup(svg_ruler, svg_compass).arrange(RIGHT, buff=0.5).scale(1.5)

        # 解析几何
        plane = NumberPlane().scale(0.5)

        # 整体
        geo_gr = VGroup(svg_gr, plane).arrange(DOWN, buff=2).scale(1.1)

        # Display the image
        self.play(Write(svg_gr[0]),
                  Write(svg_gr[1]),
                  Write(plane),
                  run_time = 2)
        self.wait(1)

        self.play(FadeOut(geo_gr))
        self.wait(1)
        pass

    # 以将军饮马问题介绍两种几何
    def two_geometry_example(self):
        bank = Line([-4, 0, 0], [4, 0, 0], color=WHITE)
        point_a = Dot([-1, 1, 0], color=WHITE)
        point_b = Dot([2, 2, 0], color=WHITE)
        label_a = MathTex("A", color=WHITE).next_to(point_a, UP)
        label_b = MathTex("B", color=WHITE).next_to(point_b, UP)
        bank_gr = VGroup(bank, point_a, point_b, label_a, label_b)

        # 上
        bank_up = bank_gr.copy()
        # 下
        bank_down = bank_gr.copy()

        bank_up_down = VGroup(bank_up, bank_down).arrange(DOWN, buff=3)
        bank_up.shift(UP)
        self.play(Write(bank_up_down), run_time=1)
        self.wait()

        # 求解A的对称点
        ver_dis = bank_up[1].get_center()[1] - bank_up[0].get_center()[1]
        point_a_sym_x = bank_up[1].get_center()[0]
        point_a_sym_y = bank_up[1].get_center()[1] - 2*ver_dis
        point_a_sym = Dot([point_a_sym_x, point_a_sym_y, 0], color=WHITE)
        label_a_sym = MathTex("A'", color=WHITE).next_to(point_a_sym, DOWN)

        line_a_sym_b = Line(point_a_sym.get_center(), bank_up[2].get_center(), color=RED)   
        
        plane = NumberPlane().shift(bank_down[0].get_center()).scale(0.7)
        point_c = Dot(plane.get_center() + RIGHT, color=WHITE)
        label_c = MathTex("C(x,y)", color=RED).next_to(point_c, DOWN)
        self.play(Write(plane), 
                  Write(point_a_sym), 
                  Write(label_a_sym), 
                  Write(point_c),
                  Write(label_c),
                  ShowCreation(line_a_sym_b),
                  run_time=1)

        self.wait()

        pass

    # 以费马点的例子介绍两种几何
    def two_geometry_example_depreate(self):
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





