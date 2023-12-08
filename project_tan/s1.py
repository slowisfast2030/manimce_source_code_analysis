from manim import *

"""
角平分线
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class s1(Scene):
    def setup(self):
        self.coord_c = [-4,0,0]
        self.coord_a = [0,0,0]
        self.coord_b = [0,3,0]
        self.coord_d = [0, 4/3, 0]
        self.coord_e = [-4/5, 12/5, 0]

    def construct(self):
        # self.introduce_triangle()
        # self.introduce_half_angle()
        # self.tri_flip()
        # self.clear()
        self.introduce_four_half_angle_model()
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
        
        
        ver_e = MathTex("E", color=GREEN).next_to(self.coord_e, 0.5*(LEFT+UP))
        self.play(FadeIn(ver_e), run_time=1)

    # 角平分线4个model
    def introduce_four_half_angle_model(self):
        """
        为了显示这4个模型, 需要精确的点的控制
        所以, 借助上面的三角形, 来引入这4个模型
        """
        # 直线cb的方程: y = 3/4*x + 3
        # 在直线cb上取点(1, 3.75)
        # 在直线ca上取点(2, 0)
        # 直线cd的方程: y = 1/3*x + 4/3
        # 在直线cd上取点(1.5, 11/6)
        line_om = Line(self.coord_c, [1, 3.75, 0], color=BLUE)
        line_on = Line(self.coord_c, [2, 0, 0], color=BLUE)
        line_op = Line(self.coord_c, [1.5, 11/6, 0], color=BLUE)
        dot_o = Dot(self.coord_c, color=RED)
        dot_p = Dot(self.coord_d, color=RED)
        label_o = MathTex("o", color=RED).next_to(dot_o, DOWN)
        label_p = MathTex("p", color=RED).next_to(dot_p, RIGHT)

        self.line_gr = VGroup(line_om, 
                              line_on, 
                              line_op,
                              dot_o,
                              dot_p,
                              label_o,
                              label_p)
        

        #model_1 = self.get_model_1()
        #model_2 = self.get_model_2()
        #model_3 = self.get_model_3()
        model_4 = self.get_model_4()

        pass

    def get_model_1(self):            
        self.play(Write(self.line_gr), run_time=1)
    
        coord_m = self.coord_a
        coord_n = self.coord_e
        
        line_pm = Line(self.coord_d, coord_m, color=RED)
        line_pn = Line(self.coord_d, coord_n, color=RED)
        label_m = MathTex("m", color=RED).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=RED).next_to(coord_n, LEFT)
        self.play(Write(line_pm), 
                  Write(line_pn), 
                  Write(label_m), 
                  Write(label_n), 
                  run_time=1)
        
    def get_model_2(self):
        self.play(Write(self.line_gr), run_time=1)

        # 通过计算可知
        coord_m = [-1, 0, 0]
        coord_n = [-8/5, 9/5, 0]
        
        line_pm = Line(self.coord_d, coord_m, color=RED)
        line_pn = Line(self.coord_d, coord_n, color=RED)
        label_m = MathTex("m", color=RED).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=RED).next_to(coord_n, LEFT)
        self.play(Write(line_pm), 
                  Write(line_pn), 
                  Write(label_m), 
                  Write(label_n), 
                  run_time=1)

        
    def get_model_3(self):
        # 直线cd: y = 1/3x + 4/3
        # 直线cb: y = 3/4x + 3
        self.play(Write(self.line_gr), run_time=1)

        # 通过计算可知
        coord_m = [4/9, 0, 0]
        coord_n = [-4/9, 8/3, 0]

        line_pm = Line(self.coord_d, coord_m, color=RED)
        line_pn = Line(self.coord_d, coord_n, color=RED)
        label_m = MathTex("m", color=RED).next_to(coord_m, DOWN)
        label_n = MathTex("n", color=RED).next_to(coord_n, LEFT)
        self.play(Write(line_pm), 
                  Write(line_pn), 
                  Write(label_m), 
                  Write(label_n), 
                  run_time=1)
        
    
    def get_model_4(self):
        self.play(Write(self.line_gr), run_time=1)

        # 通过计算可知
        coord_n = (-20/9, 4/3, 0)
        line_pn = Line(self.coord_d, coord_n, color=RED) 
        label_n = MathTex("n", color=RED).next_to(coord_n, LEFT)
        self.play(Write(line_pn), 
                  Write(label_n), 
                  run_time=1) 