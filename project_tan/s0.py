from manim import *

"""
开场
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s0(Scene):
    def setup(self):
        self.coord_c = [-4,0,0]
        self.coord_a = [0,0,0]
        self.coord_b = [0,3,0]
        self.coord_d = [0, 4/3, 0]
        self.coord_e = [-4/5, 12/5, 0]
        self.coord_f = [1, 0, 0]

        self.line_color = MAROON_B
        self.label_color = WHITE

        self.radius = 2
        self.stroke_color = WHITE
        self.radial_line_color = MAROON_B

        self.shift_vector = np.array([-2, 1.5, 0]) - 4*UP
        self.coord_c_shift = np.array(self.coord_c) - self.shift_vector
        self.coord_a_shift = np.array(self.coord_a) - self.shift_vector
        self.coord_b_shift = np.array(self.coord_b) - self.shift_vector

        self.text_scale = 0.9
        pass

    def construct(self):
        self.opening()  
        self.introduce_three_methods()
        pass


    
    # 在屏幕上方出现一个简单的三角形，下方位置留给pi生物
    # 在三角形下方显示tan(alpha) = 3/4，求解tan(alpha/2)
    def opening(self):
        triangle = Polygon(self.coord_c_shift, 
                           self.coord_a_shift, 
                           self.coord_b_shift, 
                           color=self.line_color, stroke_width=3).set_z_index(1)
        point_c = Dot(self.coord_c_shift)
        point_a = Dot(self.coord_a_shift)
        point_b = Dot(self.coord_b_shift)

        ver_c = MathTex("C", color=self.label_color).next_to(self.coord_c_shift, DOWN).set_z_index(1)
        ver_a = MathTex("A", color=self.label_color).next_to(self.coord_a_shift, DOWN).set_z_index(1)
        ver_b = MathTex("B", color=self.label_color).next_to(self.coord_b_shift, RIGHT).set_z_index(1)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, 
                  ShowCreation(triangle),
                  run_time=1)
        self.wait()
        
        line_ca = Line(self.coord_c_shift, self.coord_a_shift)
        line_cd = Line(self.coord_c_shift, self.coord_b_shift)
        angle = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        label_angle = MathTex(r"\alpha").next_to(angle, RIGHT).scale(0.8).shift(0.05*UP)

        self.play(Write(angle), Write(label_angle), run_time=1)
        self.wait()

        text = Tex("It is already to know that $tan(\\alpha) = \\frac{3}{4}$, \\\\ then what is value of $tan(\\frac{\\alpha}{2})$?").scale(self.text_scale).next_to(triangle, DOWN, 1)
        self.play(Write(text), run_time=1)
        self.wait()

        tri_gr = VGroup(triangle, ver_c, ver_a, ver_b, point_a, point_b, point_c)

        tri_gr_up = tri_gr.copy()
        tri_gr_mid = tri_gr.copy()
        tri_gr_down = tri_gr.copy()
        all_gr = VGroup(tri_gr_up, tri_gr_mid, tri_gr_down).arrange(DOWN, buff=1.5).scale(0.8)

        self.play(FadeOut(angle),
                  FadeOut(label_angle),
                  FadeOut(text))
        self.play(FadeOut(tri_gr),
                  TransformFromCopy(tri_gr, tri_gr_up),
                  TransformFromCopy(tri_gr, tri_gr_mid),
                  TransformFromCopy(tri_gr, tri_gr_down))
        self.wait()
        self.all_gr = all_gr    

        pass

    # 屏幕从上至下出现3种解法
    """
    有一个很炫的转场
    开场中间出现了一个三角形
    然后这个三角形被分成了三个部分：上中下
    然后在上中下三个三角形的基础上分别显示三种解法

    非常丝滑
    """
    def introduce_three_methods(self):
        
        method_1 = self.introduce_first_method()
        method_2 = self.introduce_second_method()
        method_3 = self.introduce_third_method()

        # method_123 = VGroup(method_1, method_2, method_3).arrange(DOWN, buff=0.5).scale(0.7)
        # self.add(method_123)
        self.play(ShowCreation(method_1),
                  ShowCreation(method_2),
                  ShowCreation(method_3),
                  run_time=2)
        self.wait()
        
        # 将方法2和方法3变暗
        # 并没有达到预期的效果，可以在方法2和方法3上添加一个矩形框
        # self.play(method_2.animate.set_opacity(0.5),
        #           method_3.animate.set_opacity(0.5)
        #           ) 
        # self.wait() 

    # 第一种解法
    def introduce_first_method(self):
        tri_gr_up = self.all_gr[0]
        point_a = tri_gr_up[4]
        point_b = tri_gr_up[5]
        point_c = tri_gr_up[6]
        # 根据比例计算出点D的坐标
        point_d = Dot(5/9*point_a.get_center() + 4/9*point_b.get_center())

        half_line = Line(point_c.get_center(), point_d.get_center(), color=self.line_color)

        ver_d = MathTex("D", color=self.label_color).next_to(point_d, RIGHT)

        line_ca = Line(point_c.get_center(), point_a.get_center())
        line_cd = Line(point_c.get_center(), point_d.get_center())
        angle_half = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        label_angle_half = MathTex(r"\frac{\alpha}{2}").next_to(angle_half, RIGHT).scale(0.8).shift(0.05*UP)
        
        result = VGroup(half_line, 
                        ver_d,
                        angle_half, 
                        label_angle_half)
        return result
        
    # 第二种解法
    def introduce_second_method(self):
        origin = Dot(ORIGIN)
        origin_lable = MathTex("O").next_to(origin, UP)

        circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color
        )
        radius_line = Line(
            circle.get_center(),
            circle.get_right(),
            color = self.radial_line_color
        )
        radius_brace = Brace(radius_line, buff = SMALL_BUFF)
        radius_label = radius_brace.get_tex("R", buff = SMALL_BUFF)

        result = VGroup(origin, origin_lable, 
                        circle, radius_line, 
                        radius_brace, radius_label)
        return result

    # 第三种解法    
    def introduce_third_method(self):
        plane = NumberPlane()
        triangle = Polygon(self.coord_c, self.coord_a, self.coord_b, color=self.line_color, stroke_width= 3)

        ver_c = MathTex("C", color=WHITE).next_to(self.coord_c, DOWN)
        ver_a = MathTex("A", color=WHITE).next_to(self.coord_a, DOWN)
        ver_b = MathTex("B", color=WHITE).next_to(self.coord_b, RIGHT)

        # 显示角平分线
        half_line = Line(self.coord_c, self.coord_d, color=self.line_color)
        ver_d = MathTex("D", color=WHITE).next_to(self.coord_d, RIGHT)

        # 显示直线CD的垂线
        line_ef = Line(self.coord_e, self.coord_f, color=self.line_color)
        ver_e = MathTex("E", color=WHITE).next_to(self.coord_e, LEFT)
        ver_f = MathTex("F", color=WHITE).next_to(self.coord_f, DOWN)

        result = VGroup(plane, 
                        triangle, ver_c, ver_a, ver_b, 
                        half_line, ver_d, 
                        line_ef, ver_e, ver_f)
        return result

    