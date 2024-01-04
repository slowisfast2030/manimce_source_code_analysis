from manim import *

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class ShowCreation(Create):
    pass

class s3(Scene):
    def setup(self):
        self.radius = 2
        self.dR = self.radius/15
        self.ring_colors = [BLUE, GREEN]

        self.stroke_color = BLACK
        self.stroke_width = 1
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.unwrapped_tip = ORIGIN

        self.num_lines = 24
        self.line_color = BLACK

        self.ring_index_proportion = 0.6
        self.ring_shift_val = 5*DOWN

        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(UP, buff = MED_LARGE_BUFF*4)
        self.add(self.circle)

    def construct(self):
        # 引入多种分割
        self.try_to_understand_area()
        # 引入ring分割
        self.slice_into_rings()

        self.isolate_one_ring()

        self.unwrap_rings(self.ring)

        # self.play(ApplyWave(self.rings,
        #                     #direction = RIGHT,
        #                     #time_width=0.5,
        #                     amplitude=0.1,
        #                     run_time=3),
        #           ApplyWave(self.circle,
        #                     #direction = RIGHT,
        #                     #time_width=0.5,
        #                     amplitude=0.1,
        #                     run_time=3), 
        #           )
        
        self.wait()

        """
        将圆分割为更多的圆环
        """
        print(self.radius)
        rings_list = [
            self.get_rings(dR = self.radius/n)
            for n in [20]
        ]
        for rings in rings_list:
            self.play(
                Transform(self.rings, rings),
                lag_ratio = 0,
                run_time = 2
            )
            self.wait()


        # self.play(FadeOut(self.ring),
        #           FadeOut(self.unwrapped))

    def try_to_understand_area(self):
        line_sets = [
            VGroup(*[
                Line(
                    self.circle.point_from_proportion(alpha),
                    self.circle.point_from_proportion(func(alpha)),
                )
                for alpha in np.linspace(0, 1, self.num_lines)
            ])
            for func in [
                lambda alpha : 1-alpha,
                lambda alpha : (0.5-alpha)%1,
                lambda alpha : (alpha + 0.4)%1,
                lambda alpha : (alpha + 0.5)%1,
            ]
        ]
        for lines in line_sets:
            lines.set_stroke(self.line_color, 2)
        lines = line_sets[0]

        self.play(
            ShowCreation(
                lines, 
                run_time = 2, 
                lag_ratio = 0.5
            )
        )
        for new_lines in line_sets[1:]:
            self.play(
                Transform(lines, new_lines),
            )
            self.wait()
        self.play(FadeOut(lines))

    def slice_into_rings(self):
        rings = self.get_rings()
        rings.set_stroke(BLACK, 1)

        self.play(
            FadeIn(
                rings,
                lag_ratio = 0.5,
                run_time = 1
            )
        )
        self.wait(1)
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
        colors = kwargs.get("colors", self.ring_colors)
        radii = np.arange(0, self.radius, dR)
        colors = color_gradient(colors, len(radii))

        rings = VGroup(*[
            self.get_ring(radius, dR = dR, color = color)
            for radius, color in zip(radii, colors)
        ]).set_opacity(0.8)
        return rings
    
    def isolate_one_ring(self):
        rings = self.rings
        index = int(self.ring_index_proportion*len(rings))
        original_ring = rings[index]
        ring = original_ring.copy()

        self.play(
            ring.animate.shift(self.ring_shift_val),
            original_ring.animate.set_fill(None, 0.25)
        )

        self.wait()

        self.play(*[
            ApplyMethod(
                r.set_fill, YELLOW, 
                rate_func = squish_rate_func(there_and_back, alpha, alpha+0.15),
                run_time = 3
            )
            for r, alpha in zip(rings, np.linspace(0, 0.85, len(rings)))
        ])
        self.wait()

        self.original_ring = original_ring
        self.ring = ring

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
    
    def unwrap_rings(self, ring, **kwargs):
        unwrapped = self.get_unwrapped(ring, **kwargs)
        unwrapped.move_to(ring.get_bottom()+DOWN)
        self.play(
            TransformFromCopy(ring, unwrapped, run_time = 3),
        )
        self.unwrapped = unwrapped