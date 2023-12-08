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
        self.double_relation()
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

        # 创建一个圆周上的点
        circle_point = Dot(point=circle.point_at_angle(PI/3), color=RED)
        circle_point_lable = MathTex("C").next_to(circle_point, UP)
        self.play(ShowCreation(circle_point),
                  Write(circle_point_lable),
                  run_time=1)   

        # 创建两条线段，从圆周上的点指向圆的直径的两端
        line_1 = Line(circle_point.get_center(), line_diameter.get_left(), color=self.radial_line_color)
        line_2 = Line(circle_point.get_center(), line_diameter.get_right(), color=self.radial_line_color)
        
        move_lines = VGroup(line_1, line_2)
        """
        这里有一个非常奇怪的点
        如果删除self.add(move_lines)
        更新动画就会异常

        猜想:
        move_lines必须显示的添加到场景中, 后续的更新动画才会起作用
        可以是self.add(move_lines)
        也可以是self.play(ShowCreation(move_lines))
        但不能仅仅是
        self.play(ShowCreation(line_1),
                  ShowCreation(line_2))
        因为这种方式仅仅添加了line_1和line_2, 而没有添加move_lines
        """
        self.add(move_lines)
        self.play(ShowCreation(line_1),
                  ShowCreation(line_2))
        
        # 更新器
        def move_lines_updater(mob):
            new_line_1 = Line(circle_point.get_center(), line_diameter.get_left(), color=self.radial_line_color)
            new_line_2 = Line(circle_point.get_center(), line_diameter.get_right(), color=self.radial_line_color)
            line_1.become(new_line_1)
            line_2.become(new_line_2)

        def circle_point_lable_updater(mob):
            circle_point_lable.next_to(circle_point, UP) 

        # 添加更新器
        move_lines.add_updater(move_lines_updater)
        circle_point_lable.add_updater(circle_point_lable_updater)

        # 播放动画：点沿圆周运动
        self.play(Rotate(circle_point, PI, about_point=circle.get_center(), rate_func=linear), run_time=4)

        # 移除更新器
        move_lines.remove_updater(move_lines_updater)
        circle_point_lable.remove_updater(circle_point_lable_updater)


    # 圆心角和圆周角之间的关系
    def double_relation(self):
        self.clear()
        circle, line_diameter, origin, origin_lable = self.circle_gr
        self.add(circle, origin, origin_lable)
        self.wait()

        # 显示圆周角和圆心角
        point_a = Dot(circle.point_at_angle(PI + PI/6), color=RED)
        point_b = Dot(circle.point_at_angle(PI + 5*PI/6), color=RED)
        point_c = Dot(circle.point_at_angle(PI/2), color=RED)
        label_a = MathTex("A").next_to(point_a, LEFT)
        label_b = MathTex("B").next_to(point_b, RIGHT)
        label_c = MathTex("C").next_to(point_c, UP)

        line_ao = Line(point_a.get_center(),origin, color=self.radial_line_color)
        line_bo = Line(point_b.get_center(),origin, color=self.radial_line_color)
        line_ac = Line(point_a.get_center(),point_c.get_center(), color=self.radial_line_color)
        line_bc = Line(point_b.get_center(),point_c.get_center(), color=self.radial_line_color)

        self.play(ShowCreation(point_a),
                  ShowCreation(point_b),
                  ShowCreation(point_c),
                  Write(label_a),
                  Write(label_b),
                  Write(label_c),
                  run_time=1)
        self.wait()

        self.play(ShowCreation(line_ao),
                    ShowCreation(line_bo),
                    ShowCreation(line_ac),
                    ShowCreation(line_bc))
        self.wait()

        # 将line_ac, line_bc, label_c打包
        line_label_gr = VGroup(line_ac, line_bc, label_c)
        self.add(line_label_gr)

        # 更新器
        def line_label_gr_updater(mob):
            new_line_ac = Line(point_a.get_center(),point_c.get_center(), color=self.radial_line_color)
            new_line_bc = Line(point_b.get_center(),point_c.get_center(), color=self.radial_line_color)
            new_label_c = MathTex("C").next_to(point_c, UP)
            line_ac.become(new_line_ac)
            line_bc.become(new_line_bc)
            label_c.become(new_label_c)

        line_label_gr.add_updater(line_label_gr_updater)

        # 播放动画：点沿圆周运动
        self.play(Rotate(point_c, 3*PI/4, about_point=circle.get_center(), rate_func=linear), run_time=3)
        self.wait()

