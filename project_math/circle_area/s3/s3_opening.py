from manim import *

"""
左上角出现一个圆
圆变成圆环
圆环展开为长条
"""

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s3_opening(Scene):

    def setup(self):
        self.radius = 2
        self.stroke_color = WHITE
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75
        self.circle_corner = UP + LEFT
        self.radial_line_color = MAROON_B
        self.dR = self.radius/30
        self.ring_colors = [BLUE, GREEN]
        self.unwrapped_tip = ORIGIN + MED_LARGE_BUFF*DOWN

        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=2,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.to_corner(UP, buff = MED_LARGE_BUFF*4)
        self.circle.set_fill(self.fill_color, self.fill_opacity)
        self.add(self.circle)
        
    def construct(self):
        self.introduce_area()
        self.introduce_rings()

    def introduce_area(self):   
        area = MathTex("\pi R^2").scale(1.3)
        area.move_to(self.circle)
        self.add(area)
        pass
        
    def introduce_rings(self):
        rings = VGroup(*reversed(self.get_rings()))
        rings.set_stroke(BLACK, 0.2)
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

        self.play(
            rings.animate.move_to(unwrapped_rings.get_top()+DOWN*0),
            path_arc = np.pi/2,
            **ring_anim_kwargs
        )

        #self.wait(0.5)
        self.play(
            Transform(rings, unwrapped_rings, **ring_anim_kwargs),
        )
        #self.wait()

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
        outer_circle = Circle(radius=radius+dR).rotate(PI/2).get_points()[:32]
        inner_circle = Circle(radius=radius).rotate(PI/2).get_points()[:32][::-1]

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