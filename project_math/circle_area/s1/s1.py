"""
ring to rectangle
"""
from manim import *
import itertools as it

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class ShowCreation(Create):
    pass

class s1(Scene):
    def setup(self):
        self.radius = 2.0
        self.dR = self.radius/15
        self.ring_colors = [BLUE, GREEN]

        self.stroke_color = WHITE
        self.stroke_width = 2
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.n_slices = 20
        self.sector_stroke_width = 1.0

        self.radius_line_color = MAROON_B

    def construct(self):
        """
        分镜1:
        显示圆的分割
        """
        self.split_circle()
        """
        分镜2:
        将圆环上移, 下方同时出现坐标轴
        """
        self.remove(self.radius_group)
        self.circle.set_fill(self.fill_color, self.fill_opacity)
        all_gr = VGroup(self.circle, self.rings)
        self.ax_rects_curve = self.get_ax_rects_curve()
        self.ax_rects_curve.to_corner(DOWN, buff = MED_LARGE_BUFF*4).shift(RIGHT*0.3)

        self.play(
            all_gr.animate.to_corner(UP, buff = MED_LARGE_BUFF*4),
            FadeOut(self.text),
            FadeOut(self.text_en),
            Write(self.ax_rects_curve[0]),
            run_time=1
        )
        self.rects = self.ax_rects_curve[1]
        self.rects.set_opacity(0.5)

        # 为每一个ring找到对应的rect
        ring_index = 7
        rect_index = ring_index + 1
        self.rings[ring_index].target = self.get_target_rect(self.rings[ring_index], rect_index).stretch_to_fit_width(self.dR+0.05)  
        
        # 将除了index之外的ring变暗
        # self.play(
        #     self.rings.animate.set_opacity(0.2),
        #     self.rings[ring_index].animate.set_opacity(1)
        # )

        self.rings[7].original = self.rings[7].copy()
        self.play(
            MoveToTarget(
                self.rings[7],
                path_arc = -np.pi/2,
                run_time = 2,
            )
        )
        self.play(
            Transform(self.rings[7], self.rings[7].original),
            path_arc = np.pi/2,
            run_time = 2,
        )
        self.wait()
        """
        分割为更多的圆环
        """
        self.ax = self.ax_rects_curve[0]
        text_more_rings = Text("更多的圆环").scale(0.8)
        text_more_rings.set_color_by_gradient(BLUE, GREEN)
        text_more_rings.move_to(self.ax.coords_to_point(2, 13))
        text_more_rings_en = Text("More rings").scale(0.8)
        text_more_rings_en.set_color_by_gradient(BLUE, GREEN)
        text_more_rings_en.next_to(text_more_rings, DOWN, buff = MED_LARGE_BUFF*0.5)

        self.play(
                    FadeIn(text_more_rings),
                    FadeIn(text_more_rings_en))
        self.text = text_more_rings
        self.text_en = text_more_rings_en

        rings_list = [
            self.get_rings(dR = self.radius/n).set_stroke(BLACK, 0.1)
            for n in [30,45,60]
        ]
        
        for rings in rings_list:
            self.play(
                Transform(self.rings, rings),
                lag_ratio = 0.5,
                run_time = 1
            )
        """
        全部展开
        """
        # 在全部展开之前需要重新生成rects
        self.dR = self.radius/60
        self.ax_rects_curve = self.get_ax_rects_curve()
        self.ax_rects_curve.to_corner(DOWN, buff = MED_LARGE_BUFF*4).shift(RIGHT*0.3)
        self.rects = self.ax_rects_curve[1]
        self.rects.set_opacity(0.5)

        
        # 为每一个ring找到对应的rect
        for index, ring in enumerate(self.rings):
            rect_index = index + 1
            ring.target = self.get_target_rect(ring, rect_index)
        
        self.play(
            FadeOut(self.text),
            FadeOut(self.text_en),
        )
        self.play(*[
            MoveToTarget(
                ring,
                path_arc = -np.pi/2,
                run_time = 4,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.25)
            )
            for ring, alpha in zip(
                self.rings, 
                np.linspace(0, 0.75, len(self.rings))
            )])
        self.wait()

        # 显示直线
        self.play(
            ShowCreation(self.ax_rects_curve[2].set_stroke(BLUE, 4)),
            ApplyWave(self.rings,
                      direction=RIGHT,
                      amplitude=0.2,
                      time_width=0.5),
            run_time=3
        )
        self.wait()

        """
        显示圆面积的计算
        """
        
        line_width = Line(
            self.ax.coords_to_point(0, 0),
            self.ax.coords_to_point(3, 0),
        ).set_color(self.radius_line_color).set_stroke(width=4)
        br_width = Brace(line_width, DOWN)
        text_width = br_width.get_tex("R")

        line_height = Line(
            self.rects[-1].get_corner(DR),
            self.rects[-1].get_corner(UR),
        ).set_color(self.radius_line_color).set_stroke(width=4)
        br_height = Brace(line_height, RIGHT)
        text_height = br_height.get_tex("2\pi R")

        self.play(
            GrowFromCenter(line_height),
            GrowFromCenter(line_width),
            GrowFromCenter(br_width),
            GrowFromCenter(br_height),
            Write(text_width),
            Write(text_height),
        )
        self.wait()

        


    def get_target_rect(self, ring: VMobject, rect_index):
        rect = self.rects[rect_index]

        # 内外环一共16段曲线，外加两条直线，一共18段
        n_anchors = ring.get_num_curves()
        #print(n_anchors)            
        target = VMobject()
        target.set_points_as_corners([
            interpolate(ORIGIN,  DOWN, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ]+[
            interpolate(DOWN+RIGHT, RIGHT, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ])
        # 将折线闭合
        #target.add_line_to(ORIGIN)    
        line = [target.get_points()[-1], 
                interpolate(target.get_points()[-1], target.get_points()[0], 0.3),
                interpolate(target.get_points()[-1], target.get_points()[0], 0.6),
                target.get_points()[0]] 
        target.append_points(line)


        target.stretch_to_fit_height(rect.get_height())
        target.stretch_to_fit_width(rect.get_width())
        target.move_to(rect)
        target.set_stroke(BLACK, 1)
        target.set_fill(ring.get_fill_color(), 1)

        #print(len(ring.get_points()))
        #print(len(target.get_points()))

        ring.target = target
        ring.original_ring = ring.copy()
        return target

    def get_ax_rects_curve(self, **kwargs):
        # 创建坐标轴并设置x轴和y轴的配置
        ax = Axes(
            x_range=[-0.1, 4, 1],  # 从-0.5开始以确保0会显示
            y_range=[-0.5, 20, 2.5],  # 从-0.5开始以确保0会显示
            x_length=7,
            y_length=7,
            tips=False,
            axis_config={"color": GRAY},  # 将坐标轴线条设置为灰色
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 1,2,3,4],  # 在x轴上只显示0, 5, 10
                "include_ticks": True,
                "decimal_number_config": {
                    "num_decimal_places": 0,  # 设置为0以显示整数
                    "color": BLUE,  # 设置x轴数字的颜色
                },
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 5, 10,15,20],  # 在y轴上也只显示0, 5, 10
                "numbers_with_elongated_ticks": [0, 5, 10,15,20],
                "decimal_number_config": {
                    "num_decimal_places": 0,  # 设置为0以显示整数
                    "color": BLUE,  # 设置x轴数字的颜色
                },
            },
        )
        
        # 绘制函数
        quadratic = ax.plot(lambda x: 2*PI*x, x_range=[0, 3], color=BLUE, stroke_width=2)

        # 获取黎曼矩形
        rect_num = self.radius/self.dR
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 3], dx=3/(rect_num+1), color=[BLUE, GREEN], input_sample_type="left"
        )
        #print(len(rects_left))
        # 这一行干嘛的？
        rects_left[2].set_opacity(0.5)

        res = VGroup()
        res.add(ax, rects_left, quadratic)
        return res 


    def split_circle(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.move_to(ORIGIN)
        self.radius_line = Line(
            self.circle.get_center(),
            self.circle.get_right(),
            color = self.radius_line_color
        )
        self.radius_brace = Brace(self.radius_line, buff = SMALL_BUFF)
        self.radius_label = self.radius_brace.get_tex("R", buff = SMALL_BUFF)

        self.radius_group = VGroup(
            self.radius_line, self.radius_brace, self.radius_label
        )
        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
        )
        self.circle.set_fill(opacity = 0)

        text_split = Text("圆的分割").scale(0.8)
        text_split.set_color_by_gradient(BLUE, GREEN)
        text_split.to_corner(UP, buff = MED_LARGE_BUFF*6)
        text_split_en = Text("Division of circle").scale(0.8)
        text_split_en.set_color_by_gradient(BLUE, GREEN)
        text_split_en.next_to(text_split, DOWN, buff = MED_LARGE_BUFF*0.5)

        self.play(
            Rotate(
                self.radius_line, 2*PI-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            Write(text_split),
            Write(text_split_en),
            
            run_time = 1
        )

        # 当circle执行了set_fill的动画后会覆盖掉radius_group
        # 所以需要将radius_group放到circle的上面
        self.bring_to_front(self.radius_group)

        

        rings = self.get_rings() 
        rings.set_stroke(BLACK, 0.2)
        
        self.play(
            FadeIn(
                rings,
                lag_ratio = 0.5,
                run_time = 1
            ),
            #FadeOut(self.radius_group),
            )
        
        self.text = text_split
        self.text_en = text_split_en
        self.rings = rings

    def get_ring(self, radius, dR, color = GREEN):
        ring = VMobject()
        """
        为何要旋转90度
        当旋转90度后, 圆的起点正好在正上方
        后续需要将这个圆环展开横向的长条, 开口放在正上方比较好看

        如果不旋转, 就会将开口放在右侧
        这样比较适合展开为竖直的长条

        以cairo作为后端
        circle的点集数目是多少?
        """
        #print(len(Circle(radius=radius+dR).rotate(PI/2).get_points()))
        # 经过打印后发现点集的数目是32，不是64
        # 奇怪：为何一开始写64呢？
        # 圆是由8段圆弧拼接而成，每一段圆弧由4个点构成
        outer_circle = Circle(radius=radius+dR).rotate(1*PI/2).get_points()[:]
        inner_circle = Circle(radius=radius).rotate(1*PI/2).get_points()[:][::-1]

        # 遵守manimce的约定，每一段贝塞尔曲线由4个点构成
        line1 = [outer_circle[-1], 
                 interpolate(outer_circle[-1], inner_circle[0], 0.3),
                 interpolate(outer_circle[-1], inner_circle[0], 0.6),
                 inner_circle[0]]
        
        line2 = [inner_circle[-1],
                interpolate(inner_circle[-1], outer_circle[0], 0.3),
                interpolate(inner_circle[-1], outer_circle[0], 0.6),
                outer_circle[0]]
        
        """
        将内环和外环的点集
        加上连接内外环的直线
        一起作为新的点集
        """
        points_to_add = list(outer_circle) + line1 + list(inner_circle) + line2

        ring.append_points(points_to_add)
        ring.set_stroke(width = 0)
        """
        我非常奇怪的一点:
        这样人工构造出了点集之后
        着色的时候是如何区分区域的内外呢？

        cairo后端似乎很容易
        opengl后端不容易理解
        """
        ring.set_fill(color, opacity = 1)
        # 在这里明确了ring的位置
        ring.move_to(self.circle)
        ring.R = radius 
        ring.dR = dR

        return ring

    def get_rings(self, **kwargs):
        dR = kwargs.get("dR", self.dR)
        print(dR)
        colors = kwargs.get("colors", self.ring_colors)
        radii = np.arange(0, self.radius, dR)
        colors = color_gradient(colors, len(radii))

        rings = VGroup(*[
            self.get_ring(radius, dR = dR, color = color)
            for radius, color in zip(radii, colors)
        ]).set_opacity(1)
        return rings