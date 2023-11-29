from manim import *

"""
在manimgl环境下:
圆环和长条都可以实现
但是动画效果不好
需要研究下怎样对齐点集

在manimce环境下:
同上

根源:
还是点集没有对齐
"""
class test(Scene):
    def construct(self):
        ring = self.get_ring(1, 0.18).rotate(PI/2).shift(UP).scale(2)
        #self.play(FadeIn(ring))
        self.add(ring)

        unwrapped = self.get_unwrapped(ring).shift(DOWN*3) 

        for index, point in enumerate(ring.get_points()):
            dot = Dot(point)
            if index < 24:
                label = Text(str(index), font_size=24).next_to(dot, point-ring.get_center(), buff=0.1)
            else:
                label = Text(str(index), font_size=24).next_to(dot, ring.get_center()-point, buff=0.1)
                pass
            self.add(dot, label)

        for index, point in enumerate(unwrapped.get_points()):
            dot = Dot(point)
            if index < 21:
                label = Text(str(index), font_size=24).next_to(dot, DOWN, buff=0.1)
            else:
                label = Text(str(index), font_size=24).next_to(dot, UP, buff=0.1)
            self.add(dot, label)


        # 点集没有对齐。所以动画很难看
        self.play(Transform(ring, unwrapped))
    
    def get_ring(self, radius, dR, color = RED):
        ring = Circle(radius = radius + dR).center()
        inner_ring = Circle(radius = radius).center()
        # 点睛之笔。特别注意点集的顺序。
        inner_ring.rotate(PI, RIGHT)
        # 此时inner_ring的点集是顺时针的

        ring.append_vectorized_mobject(inner_ring)
        ring.set_stroke(width = 0)
        ring.set_fill(color,1)
        ring.R = radius 
        ring.dR = dR
        return ring
    
    def get_unwrapped(self, ring:VMobject, to_edge = LEFT, **kwargs):
        R = ring.R
        R_plus_dr = ring.R + ring.dR
        n_anchors = ring.get_num_curves()

        # 如果manim没有自己想要的形状，可以自己构造点集
        result = VMobject()
        result.set_points_as_corners([
            interpolate(np.pi*R_plus_dr*LEFT,  np.pi*R_plus_dr*RIGHT, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ]+[
            interpolate(np.pi*R*RIGHT+ring.dR*UP,  np.pi*R*LEFT+ring.dR*UP, a)
            for a in np.linspace(0, 1, n_anchors//2)
        ])
        result.set_style(
            stroke_color = ring.get_stroke_color(),
            stroke_width = ring.get_stroke_width(),
            fill_color = ring.get_fill_color(),
            fill_opacity = ring.get_fill_opacity(),
        )

        return result