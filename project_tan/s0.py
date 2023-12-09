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

        self.line_color = MAROON_B
        self.label_color = WHITE
        pass

    def construct(self):
        self.introduce_three_methods()
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
        self.add(method_1)
        self.wait(1)


        # self.introduce_second_method()
        # self.introduce_third_method()

        pass    

    # 第一种解法
    def introduce_first_method(self):
        triangle = Polygon(self.coord_c, 
                           self.coord_a, 
                           self.coord_b, 
                           color=self.line_color,
                           stroke_width= 3)
        ver_c = MathTex("C", color=self.label_color).next_to(self.coord_c, DOWN)
        ver_a = MathTex("A", color=self.label_color).next_to(self.coord_a, DOWN)
        ver_b = MathTex("B", color=self.label_color).next_to(self.coord_b, RIGHT)

        half_line = Line(self.coord_c, self.coord_d, color=self.line_color)

        ver_d = MathTex("D", color=self.label_color).next_to(self.coord_d, RIGHT)

        line_ca = Line(self.coord_c, self.coord_a)
        line_cd = Line(self.coord_c, self.coord_d)
        angle_half = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        label_angle_half = MathTex(r"\alpha").next_to(angle_half, RIGHT).scale(0.8).shift(0.05*UP)
        
        result = VGroup(triangle, 
                        ver_c, ver_a, ver_b, 
                        half_line, ver_d,
                        angle_half, label_angle_half)
        return result
        
    # 第二种解法
    def introduce_second_method(self):

        pass

    # 第三种解法    
    def introduce_third_method(self):

        pass

    