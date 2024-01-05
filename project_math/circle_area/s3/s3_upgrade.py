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

        self.radius_line_color = MAROON_B

        self.stroke_color = WHITE
        self.stroke_width = 2
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.unwrapped_tip = ORIGIN + MED_LARGE_BUFF*DOWN

        self.num_lines = 24
        self.line_color = BLACK

        self.ring_index_proportion = 0.6
        self.ring_shift_val = 3.5*DOWN


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
        self.add(self.circle, *self.radius_group)

    def construct(self):
        """
        分镜1:
        画出圆, 抛出问题
        """
        self.introduce_circle()
        #self.wait()
        # 多种划分
        self.try_to_understand_area()
        """
        分镜2:
        显示分割
        """
        self.bring_to_front(self.radius_group)
        self.slice_into_rings()
        self.wait(1)
        
        """
        分镜3:
        拿出一个圆环并展开
        """
        self.isolate_one_ring()
        self.unwrap_ring(self.ring)

        
        """
        分镜4:
        将圆分割为更多的圆环
        """
        self.play(FadeOut(self.ring),
                  FadeOut(self.unwrapped),)
        rings_list = [
            self.get_rings(dR = self.radius/n).set_stroke(BLACK, 0.1)
            for n in [20,25,30]
        ]
        text_more_rings = Text("更多的圆环").scale(0.8)
        text_more_rings.set_color_by_gradient(BLUE, GREEN)
        text_more_rings.to_corner(UP, buff = MED_LARGE_BUFF*6)
        self.play(FadeOut(self.text),
                    FadeIn(text_more_rings))
        self.text = text_more_rings

        for rings in rings_list:
            self.play(
                Transform(self.rings, rings),
                lag_ratio = 0.5,
                run_time = 1
            )
            self.wait(0.5)

        """
        分镜5:
        将圆环和圆上移, 移除文字
        拿出一个圆环进行展开
        """
        all_gr = VGroup(self.circle, self.radius_group, self.rings)
        self.play(
            all_gr.animate.to_corner(UP, buff = MED_LARGE_BUFF*4),
            FadeOut(self.text)
        )
        """
        分镜6:
        展开所有圆环
        """
        self.unwrap_rings(self.rings)
        # pass

    def introduce_circle(self):
        self.remove(self.circle)
        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
        )
        self.circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                self.radius_line, 2*PI-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            run_time = 1
        )

        # 当circle执行了set_fill的动画后会覆盖掉radius_group
        # 所以需要将radius_group放到circle的上面
        self.bring_to_front(self.radius_group)

        text_split = Text("圆的分割").scale(0.8)
        text_split.set_color_by_gradient(BLUE, GREEN)
        text_split.to_corner(UP, buff = MED_LARGE_BUFF*6)
        text_split_en = Text("Division of circle").scale(0.8)
        text_split_en.set_color_by_gradient(BLUE, GREEN)
        text_split_en.next_to(text_split, DOWN, buff = MED_LARGE_BUFF*0.5)

        self.play(
            self.circle.animate.set_fill(self.fill_color, self.fill_opacity),
            #self.circle.animate.set_stroke_color(BLACK),
            Write(text_split),
            Write(text_split_en),
            run_time=0.5
        )
        self.play(self.circle.animate.set_stroke_color(BLACK))
        self.text = text_split
    
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
        rings.set_stroke(BLACK, 0.2)

        self.play(
            FadeIn(
                rings,
                lag_ratio = 0.5,
                run_time = 1
            )
        )
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
        ])
        return rings
    
    def isolate_one_ring(self):
        text_one_ring = Text("取出一个圆环").scale(0.8)
        text_one_ring.set_color_by_gradient(BLUE, GREEN)
        text_one_ring.to_corner(UP, buff = MED_LARGE_BUFF*6)

        rings = self.rings
        index = int(self.ring_index_proportion*len(rings))
        original_ring = rings[index]
        ring = original_ring.copy()

        self.remove(self.radius_group)
        self.play(
            FadeOut(self.text),
            FadeIn(text_one_ring),
            ring.animate.shift(self.ring_shift_val),
            original_ring.animate.set_fill(None, 0.25),
            path_arc = np.pi/2,
        )

        self.text = text_one_ring
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

    def unwrap_ring(self, ring, **kwargs):
        unwrapped = self.get_unwrapped(ring, **kwargs)
        unwrapped.move_to(ring.get_bottom())
        self.play(
            Transform(ring, unwrapped, run_time = 1),
        )
        self.unwrapped = unwrapped

    def unwrap_rings(self, rings, **kwargs):
        self.remove(rings)
        self.add(self.radius_group.to_corner(UP, buff = MED_LARGE_BUFF*4+2))
        #rings = VGroup(*reversed(rings))
        self.dR = self.radius/30
        rings = VGroup(*reversed(self.get_rings()))
        rings.set_stroke(BLACK, 0.1)
        unwrapped_rings = VGroup(*[
            self.get_unwrapped(ring, to_edge = None)
            for ring in rings
        ])
        unwrapped_rings.arrange(UP, buff = SMALL_BUFF)
        unwrapped_rings.move_to(self.unwrapped_tip, UP)
        ring_anim_kwargs = {
            "run_time" : 3,
            "lag_ratio" : 0.1
        }
        self.add(rings)

        # 很有层次感
        # self.play(
        #     FadeIn(rings, **ring_anim_kwargs),
        # )

        self.wait()
        # 注意path_arc参数
        self.play(
            #rings.animate.rotate(PI/2),
            rings.animate.move_to(unwrapped_rings.get_top()+DOWN*0),
            path_arc = np.pi/2,
            **ring_anim_kwargs
        )

        self.wait()
        self.play(
            Transform(rings, unwrapped_rings, **ring_anim_kwargs),
        )
    

