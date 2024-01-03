from manim import *
import itertools as it

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class rings2rects(Scene):
    def setup(self):
        self.radius = 2
        self.dR = 2/60
        self.ring_colors = [BLUE, GREEN]

        self.stroke_color = WHITE
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.unwrapped_tip = ORIGIN

        self.n_slices=60
        self.sector_stroke_width = 1.0

    def construct(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=1,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(UP, buff = MED_LARGE_BUFF*3)
        self.add(self.circle)

        self.rings = self.get_rings()
        self.add(self.rings)

        self.rings[3].set_opacity(0.5)

        self.ax_rects_curve = self.get_ax_rects_curve()
        self.ax_rects_curve.to_corner(DOWN, buff = MED_LARGE_BUFF*4)
        self.add(self.ax_rects_curve)

        self.rects = self.ax_rects_curve[1]
        self.rects.set_opacity(0.5)

        # 为每一个ring找到对应的rect
        for index, ring in enumerate(self.rings):
            rect_index = index + 1
            ring.target = self.get_target_rect(ring, rect_index)    
        
        """
        黄金5s的第一部分
        """
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
        """
        黄金5s的第二部分
        """
        self.dR = 2/30
        ring_anim_kwargs = {
            "run_time" : 4,
            "lag_ratio" : 0.1
        }
        self.rings_again = VGroup(*reversed(self.get_rings())).rotate(PI/2)
        self.add(self.rings_again)
        self.play(FadeOut(self.rings),
                  FadeOut(self.ax_rects_curve),
                  FadeIn(self.rings_again))
        
        unwrapped_rings = VGroup(*[
            self.get_unwrapped(ring, to_edge = None)
            for ring in self.rings_again
        ])
        unwrapped_rings.arrange(UP, buff = SMALL_BUFF)
        unwrapped_rings.move_to(self.unwrapped_tip, UP)

        self.play(
            #rings.animate.rotate(PI/2),
            self.rings_again.animate.move_to(unwrapped_rings.get_top()),
            path_arc = np.pi/2,
            **ring_anim_kwargs
        )

        self.play(
            Transform(self.rings_again, unwrapped_rings, **ring_anim_kwargs),
        )
        self.wait()
        
        """
        黄金5s的第三部分
        """
        sectors = self.get_sectors(self.circle, n_slices=self.n_slices)
        self.play(FadeOut(self.rings_again),
                  FadeIn(sectors))
        """
        将sectors展开
        """
        laid_sectors = sectors.copy()
        N = len(sectors)
        dtheta = TAU / N
        angles = np.arange(0, TAU, dtheta)
        for sector, angle in zip(laid_sectors, angles):
            sector.rotate(-90 * DEGREES - angle - dtheta / 2)

        laid_sectors.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        laid_sectors.move_to(1.5 * DOWN)


        """
        深度思考
        """
        self.play(TransformFromCopy(sectors, laid_sectors, run_time=2))
        self.wait()

        """
        左右的锯齿的合并
        """
        lh, rh = laid_sectors[:N // 2], laid_sectors[N // 2:]
        lh.generate_target()
        rh.generate_target()
        rh.target.rotate(PI)
        rh.target.move_to(lh[0].get_top(), UL)
        VGroup(lh.target, rh.target).set_x(0)
        rh.target.shift(UP)
        lh.target.shift(DOWN)

        self.play(
            MoveToTarget(lh, run_time=1.5),
            MoveToTarget(rh, run_time=1.5, path_arc=PI),
        )
        self.play(
            lh.animate.shift(UP),
            rh.animate.shift(DOWN),
        )
        self.wait()
        pass

    def get_target_rect(self, ring: VMobject, rect_index):
        rect = self.rects[rect_index]

        # 内外环一共16段曲线，外加两条直线，一共18段
        n_anchors = ring.get_num_curves()
        print(n_anchors)            
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

        print(len(ring.get_points()))
        print(len(target.get_points()))

        ring.target = target
        ring.original_ring = ring.copy()
        return target
    
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
        outer_circle = Circle(radius=radius+dR).rotate(0*PI/2).get_points()[:]
        inner_circle = Circle(radius=radius).rotate(0*PI/2).get_points()[:][::-1]

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
        print(len(rects_left))
        rects_left[2].set_opacity(0.5)

        res = VGroup()
        res.add(ax, rects_left, quadratic)
        return res 
    
    def get_unwrapped(self, ring:VMobject, to_edge = LEFT, **kwargs):
        R = ring.R
        R_plus_dr = ring.R + ring.dR
        n_anchors = ring.get_num_curves()
        # 18。每段圆弧由8段贝塞尔曲线构成。内外环，一共16段曲线。再加上两段直线。
        # print(n_anchors)
        
        # 如果manim没有自己想要的形状，可以自己构造点集
        result = VMobject()
        """
        这里有一个魔鬼细节：
        贝塞尔曲线和折线上的点的对应关系
        需要深刻理解

        通过set_points_as_corners方法传入了18个点【折线】的列表
        但这18个点需要进一步转换为更本质的贝塞尔曲线
        
        (18-1)*4=68
        """
        result.set_points_as_corners([
            interpolate(np.pi*R_plus_dr*LEFT,  np.pi*R_plus_dr*RIGHT, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ]+[
            interpolate(np.pi*R*RIGHT+ring.dR*UP,  np.pi*R*LEFT+ring.dR*UP, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ])
        # 68
        # print(len(result.get_points()))

        # 将折线闭合
        line = [result.get_points()[-1], 
                interpolate(result.get_points()[-1], result.get_points()[0], 0.3),
                interpolate(result.get_points()[-1], result.get_points()[0], 0.6),
                result.get_points()[0]] 
        result.append_points(line)
        # 猜测，这里的result的点集数目是32+32+4+4=72，这是圆环的点集的数目
        # 经过打印，确实 68+4=72
        # print(len(result.get_points()))

        result.set_style(
            stroke_color = ring.get_stroke_color(),
            stroke_width = ring.get_stroke_width(),
            fill_color = ring.get_fill_color(),
            fill_opacity = ring.get_fill_opacity(),
        )

        return result
    
    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors