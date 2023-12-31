from manim import *

"""
研究点集的对齐问题

在manimgl中:
如果内外环的半径相差很小, 会渲染错误
可以猜想是三角剖分的问题

在manimce中:
可以完美解决这个问题

根源:
manimgl的渲染后端: opengl
manimce的渲染后端: cairo(如果选opengl, 代码都会报错)

三角剖分:
三角剖分对于opengl正确的着色至关重要
在manimgl中需要添加:  vm.get_triangulation()
在manimce中不需要添加

"""
class test(Scene):
    def construct(self):
        """
        直接用两个圆的点集来构造
        """
        vm = VMobject()
        vm.R = 3
        vm.dR = 1
        
        """
        分别取内外环的点集
        """
        outer_circle = Circle(radius=3).rotate(PI/2).get_points()[:4]
        inner_circle = Circle(radius=2).rotate(PI/2).get_points()[:4][::-1]

        """
        在两段圆弧的端点处进行插值
        """
        line1 = [outer_circle[-1], 
                 interpolate(outer_circle[-1], inner_circle[0], 0.3),
                 interpolate(outer_circle[-1], inner_circle[0], 0.6),
                 inner_circle[0]]
        
        line2 = [inner_circle[-1],
                interpolate(inner_circle[-1], outer_circle[0], 0.3),
                interpolate(inner_circle[-1], outer_circle[0], 0.6),
                outer_circle[0]]
        
        # 两个圆的点集拼接起来
        points_to_add = list(outer_circle) + line1 + list(inner_circle) + line2
        vm.append_points(points_to_add)

        vm.set_fill(GREEN, 1)
        vm.set_stroke(width=1)
        vm.move_to(ORIGIN)
        vm.rotate(-PI/8).rotate(PI)
        self.add(vm)
        
        rec =  self.get_unwrapped(vm).scale(0.5).shift(DOWN*2.5)
        self.add(rec)

        for index, point in enumerate(vm.get_points()):
            dot = Dot(point)
            label = Text(str(index), font_size=24).next_to(dot, point-vm.get_center(), buff=0.1)
            self.add(dot, label)

        for index, point in enumerate(rec.get_points()):
            dot = Dot(point)
            label = Text(str(index), font_size=24).next_to(dot, UP, buff=0.1)
            self.add(dot, label)

        self.play(Transform(vm, rec))
        self.wait()
    
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

        line = [result.get_points()[-1], 
                interpolate(result.get_points()[-1], result.get_points()[0], 0.3),
                interpolate(result.get_points()[-1], result.get_points()[0], 0.6),
                result.get_points()[0]] 
        result.append_points(line)

        result.set_style(
            stroke_color = ring.get_stroke_color(),
            stroke_width = ring.get_stroke_width(),
            fill_color = ring.get_fill_color(),
            fill_opacity = ring.get_fill_opacity(),
        )

        return result


