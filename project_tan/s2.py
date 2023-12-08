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
        angle = PI/3
        circle_point = Dot(circle.point_at_angle(angle))
        circle_point_lable = MathTex("C").next_to(circle_point, UP)
        line_1 = Line(circle_point.get_center(), line_diameter.get_left(), color=self.radial_line_color)
        line_2 = Line(circle_point.get_center(), line_diameter.get_right(), color=self.radial_line_color)

        self.play(ShowCreation(circle_point),
                  Write(circle_point_lable),
                  run_time=1)   
        self.wait()

        self.play(ShowCreation(line_1),
                  ShowCreation(line_2))
        
        move_lines = VGroup(line_1, line_2)
        
        # 为move_lines添加updater
        def circle_gr_updater(mob):
            new_line_1 = Line(circle_point.get_center(), line_diameter.get_left(), color=self.radial_line_color)
            new_line_2 = Line(circle_point.get_center(), line_diameter.get_right(), color=self.radial_line_color) 
            line_1.become(new_line_1)
            line_2.become(new_line_2)
            print("===")
        
        move_lines.add_updater(circle_gr_updater)

        # C点绕圆周运动
        self.play(Rotate(circle_point, PI/2, about_point=circle.get_center()),
                  run_time=2) 

        # 移除更新器
        move_lines.remove_updater(circle_gr_updater)
        

