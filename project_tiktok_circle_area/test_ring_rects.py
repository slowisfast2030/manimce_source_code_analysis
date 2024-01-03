from manim import *

class rings2rects(Scene):
    def setup(self):
        self.radius = 1.5
        self.dR = 0.15
        self.ring_colors = [BLUE, GREEN]

        self.stroke_color = WHITE
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

    def construct(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=1,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(LEFT, buff = MED_LARGE_BUFF)
        self.add(self.circle)

        self.rings = self.get_rings()
        self.add(self.rings)

        self.ax_rects_curve = self.get_ax_rects_curve()
        self.ax_rects_curve.to_corner(RIGHT, buff = MED_LARGE_BUFF)
        self.add(self.ax_rects_curve)

        self.rects = self.ax_rects_curve[1]
        


        pass
    
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
        outer_circle = Circle(radius=radius+dR).rotate(0*PI/2).get_points()[:28]
        inner_circle = Circle(radius=radius).rotate(0*PI/2).get_points()[:28][::-1]

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
        colors = kwargs.get("colors", self.ring_colors)
        radii = np.arange(0, self.radius, dR)
        colors = color_gradient(colors, len(radii))

        rings = VGroup(*[
            self.get_ring(radius, dR = dR, color = color)
            for radius, color in zip(radii, colors)
        ])
        return rings
    
    def get_ax_rects_curve(self, **kwargs):
        # 创建坐标轴并设置x轴和y轴的配置
        ax = Axes(
            x_range=[-0.1, 4, 1],  # 从-0.5开始以确保0会显示
            y_range=[-0.5, 20, 2.5],  # 从-0.5开始以确保0会显示
            x_length=6,
            y_length=6,
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
        rects_left = ax.get_riemann_rectangles(
            quadratic, x_range=[0, 3], dx=3/11, color=[BLUE, GREEN], input_sample_type="left"
        )
        print(len(rects_left))
        rects_left[2].set_opacity(0.5)

        res = VGroup()
        res.add(ax, rects_left, quadratic)
        return res 