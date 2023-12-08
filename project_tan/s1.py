from manim import *

"""
角平分线
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s1(Scene):
    def setup(self):
        self.coord_c = [-4,0,0]
        self.coord_a = [0,0,0]
        self.coord_b = [0,3,0]
        self.coord_d = [0, 4/3, 0]
        self.coord_e = [-4/5, 12/5, 0]

        self.line_color = MAROON_B
        self.label_color = WHITE

    def construct(self):
        self.introduce_triangle()
        self.introduce_half_angle()
        self.tri_flip()
        self.clear()
        self.introduce_four_half_angle_model()
        pass

    # 引入三角形
    def introduce_triangle(self):
        triangle = Polygon(self.coord_c, 
                           self.coord_a, 
                           self.coord_b, 
                           color=self.line_color,
                           stroke_width= 3)
        self.play(ShowCreation(triangle), run_time=1)

        ver_c = MathTex("C", color=self.label_color).next_to(self.coord_c, DOWN)
        ver_a = MathTex("A", color=self.label_color).next_to(self.coord_a, DOWN)
        ver_b = MathTex("B", color=self.label_color).next_to(self.coord_b, RIGHT)
        ver_ani = list(map(FadeIn, [ver_c, ver_a, ver_b]))

        self.play(*ver_ani, run_time=1)
    
    # 引入半角
    def introduce_half_angle(self):
        
        half_line = Line(self.coord_c, self.coord_d, color=self.line_color)
        self.play(Write(half_line), run_time=1)

        ver_d = MathTex("D", color=self.label_color).next_to(self.coord_d, RIGHT)
        self.play(FadeIn(ver_d), run_time=1)

        line_ca = Line(self.coord_c, self.coord_a)
        line_cd = Line(self.coord_c, self.coord_d)
        angle_half = Angle(line_ca, line_cd, radius=0.6, other_angle=False)
        label_angle_half = MathTex(r"\alpha").next_to(angle_half, RIGHT).scale(0.8).shift(0.05*UP)

        self.play(Write(angle_half), Write(label_angle_half), run_time=1)

    # 翻转动画
    def tri_flip(self):
        flip_axis = np.array(self.coord_c) - np.array(self.coord_d)
        flip_about_point = self.coord_c
        flip_tri = Polygon(np.array(self.coord_c)+np.array([0.1, 0, 0]), self.coord_a, self.coord_d, color=TEAL)
        self.play(flip_tri.animate.rotate(PI, axis=flip_axis, about_point=flip_about_point))
        
        ver_e = MathTex("E", color=GREEN).next_to(self.coord_e, 0.5*(LEFT+UP))
        self.play(FadeIn(ver_e), run_time=1)

    # 角平分线4个model
    def introduce_four_half_angle_model(self):
        """
        为了显示这4个模型, 需要精确的点的控制
        所以, 借助上面的三角形, 来引入这4个模型
        """
        # 直线cb的方程: y = 3/4*x + 3
        # 直线cd的方程: y = 1/3*x + 4/3
        # 在直线cb上取点(1, 3.75)
        # 在直线ca上取点(2, 0)
        # 在直线cd上取点(1.5, 11/6)

        # o点就是c点, m点是a点, p点是d点, n点是e点
        coord_o = self.coord_c
        coord_p = self.coord_d

        line_om = Line(coord_o, [1, 3.75, 0], color=self.line_color)
        line_on = Line(coord_o, [2, 0, 0], color=self.line_color)
        line_op = Line(coord_o, [1.5, 11/6, 0], color=self.line_color)
        dot_o = Dot(coord_o, color=RED)
        dot_p = Dot(coord_p, color=RED)
        label_o = MathTex("o", color=self.label_color).next_to(dot_o, DOWN)
        label_p = MathTex("p", color=self.label_color).next_to(dot_p, RIGHT)

        self.line_gr = VGroup(line_om, 
                              line_on, 
                              line_op,
                              dot_o,
                              dot_p,
                              label_o,
                              label_p)
        
        self.model_1 = self.get_model_1()
        self.model_2 = self.get_model_2()
        self.model_3 = self.get_model_3()
        self.model_4 = self.get_model_4()
        model_12 = VGroup(self.model_1, self.model_2).arrange(RIGHT, buff=1)
        model_34 = VGroup(self.model_3, self.model_4).arrange(RIGHT, buff=1)
        model_1234 = VGroup(model_12, model_34).arrange(DOWN, buff=2).scale(0.6)

        self.remove(self.line_gr)
        self.play_model_12()
        self.play_model_34()
        self.wait(1)
        pass

    def get_model_1(self):                
        coord_m = self.coord_a
        coord_n = self.coord_e
        
        line_pm = Line(self.coord_d, coord_m, color=self.line_color)
        line_pn = Line(self.coord_d, coord_n, color=self.line_color)
        label_m = MathTex("m", color=self.label_color).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=self.label_color).next_to(coord_n, LEFT)
        
        return VGroup(self.line_gr.copy(), line_pm, line_pn, label_m, label_n)
    
    def get_model_2(self):
        # 通过计算可知
        coord_m = [-1, 0, 0]
        coord_n = [-8/5, 9/5, 0]
        
        line_pm = Line(self.coord_d, coord_m, color=self.line_color)
        line_pn = Line(self.coord_d, coord_n, color=self.line_color)
        label_m = MathTex("m", color=self.label_color).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=self.label_color).next_to(coord_n, LEFT)
    
        return VGroup(self.line_gr.copy(), line_pm, line_pn, label_m, label_n)

    def get_model_3(self):
        # 直线cd: y = 1/3x + 4/3
        # 直线cb: y = 3/4x + 3
        # 通过计算可知
        coord_m = [4/9, 0, 0]
        coord_n = [-4/9, 8/3, 0]

        line_pm = Line(self.coord_d, coord_m, color=self.line_color)
        line_pn = Line(self.coord_d, coord_n, color=self.line_color)
        label_m = MathTex("m", color=self.label_color).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=self.label_color).next_to(coord_n, LEFT)
        
        return VGroup(self.line_gr.copy(), line_pm, line_pn, label_m, label_n)

    def get_model_4(self):
        # 通过计算可知
        coord_n = (-20/9, 4/3, 0)

        line_pn = Line(self.coord_d, coord_n, color=self.line_color) 
        label_n = MathTex("n", color=self.label_color).next_to(coord_n, LEFT)
        
        return VGroup(self.line_gr.copy(), line_pn, label_n)
    
    # def play_model_1(self):
    #     line_gr, line_pm, line_pn, label_m, label_n = self.model_1
    #     self.play(Write(line_gr), run_time=1)
    #     self.play(Write(line_pm), 
    #               Write(line_pn), 
    #               Write(label_m), 
    #               Write(label_n), 
    #               run_time=1)

    # def play_model_2(self):
    #     line_gr, line_pm, line_pn, label_m, label_n = self.model_2
    #     self.play(Write(line_gr), run_time=1)
    #     self.play(Write(line_pm), 
    #               Write(line_pn), 
    #               Write(label_m), 
    #               Write(label_n), 
    #               run_time=1)
    
    # 合并model_1和model_2的play
    def play_model_12(self):
        line_gr_1, line_pm_1, line_pn_1, label_m_1, label_n_1 = self.model_1
        line_gr_2, line_pm_2, line_pn_2, label_m_2, label_n_2 = self.model_2
        self.play(Write(line_gr_1), Write(line_gr_2),run_time=1)

        self.play(Write(line_pm_1), 
                  Write(line_pn_1), 
                  Write(label_m_1), 
                  Write(label_n_1), 
                  Write(line_pm_2),
                  Write(line_pn_2),
                  Write(label_m_2),
                  Write(label_n_2),
                  run_time=1)

    # def play_model_3(self):
    #     line_gr, line_pm, line_pn, label_m, label_n = self.model_3
    #     self.play(Write(line_gr), run_time=1)
    #     #self.add(line_gr)
    #     self.play(Write(line_pm), 
    #               Write(line_pn), 
    #               Write(label_m), 
    #               Write(label_n), 
    #               run_time=1)
    #     pass 

    # def play_model_4(self):
    #     line_gr, line_pn, label_n = self.model_4
    #     self.play(Write(line_gr), run_time=1)
    #     #self.add(line_gr)
    #     self.play(Write(line_pn), 
    #               Write(label_n), 
    #               run_time=1)
    #     pass

    # 合并model_3和model_4的play
    def play_model_34(self):
        line_gr_3, line_pm_3, line_pn_3, label_m_3, label_n_3 = self.model_3
        line_gr_4, line_pn_4, label_n_4 = self.model_4
        self.play(Write(line_gr_3), Write(line_gr_4),run_time=1)

        self.play(Write(line_pm_3), 
                  Write(line_pn_3), 
                  Write(label_m_3), 
                  Write(label_n_3), 
                  Write(line_pn_4),
                  Write(label_n_4),
                  run_time=1)