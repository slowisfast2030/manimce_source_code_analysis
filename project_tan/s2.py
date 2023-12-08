from manim import *

"""
辅助圆
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s2(Scene):
    def setup(self):
        self.radius = 2
        self.stroke_color = WHITE
        self.radial_line_color = MAROON_B
        pass

    def construct(self):
        self.diameter_angle()
        self.right_angle()
        pass

    # 直径所对的圆周角是直角
    def diameter_angle(self):
        self.origin = Dot(ORIGIN)
        self.origin_lable = MathTex("O").next_to(self.origin, UP)

        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color
        )
        self.radius_line = Line(
            self.circle.get_center(),
            self.circle.get_right(),
            color = self.radial_line_color
        )
        self.radius_brace = Brace(self.radius_line, buff = SMALL_BUFF)
        self.radius_label = self.radius_brace.get_tex("R", buff = SMALL_BUFF)

        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
            ShowCreation(self.origin),
            Write(self.origin_lable),
        )
        #self.circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                self.radius_line, 2*PI-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            run_time = 2
        )

        self.wait(1)

        # raidus_brace和radius_label的消失
        # 半径变成直径
        self.line_diameter = Line(
            self.circle.get_left(),
            self.circle.get_right(),
            color = self.radial_line_color
        )
        self.play(
            FadeOut(self.radius_brace),
            FadeOut(self.radius_label),
            GrowFromCenter(self.line_diameter),
            self.origin_lable.animate.next_to(self.origin, DOWN),
            run_time = 1
        )

        self.circle_gr = VGroup(self.circle, 
                                self.line_diameter,
                                self.origin,
                                self.origin_lable)
    
    # 在圆上任取一点, 连接和直径的端点
    def right_angle(self):
        self.clear()
        self.add(self.circle_gr)

        # 获取重要元素
        circle, line_diameter, origin, origin_lable = self.circle_gr
        self.wait()

        # 在圆周上任取一点
        percent = 0.2
        gr1 = self.get_mov_point(percent)



        self.play(ShowCreation(gr1[0]),
                  Write(gr1[1]),
                  run_time=1)   
        self.wait()

        self.play(ShowCreation(gr1[2]),
                  ShowCreation(gr1[3]))
        
        # 移动C点
        # percent = 0.5
    

    def get_mov_point(self, percent):
        circle, line_diameter, origin, origin_lable = self.circle_gr

        circle_point = Dot(circle.point_from_proportion(percent))
        circle_point_lable = MathTex("C").next_to(circle_point, UP)
        line_1 = Line(circle_point, line_diameter.get_left(), color=self.radial_line_color)
        line_2 = Line(circle_point, line_diameter.get_right(), color=self.radial_line_color)

        gr = VGroup(circle_point, circle_point_lable, line_1, line_2)
        return gr
