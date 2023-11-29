from manim import *

"""
manim ring_merge_arc_opengl.py test -pql --renderer=opengl

在manimgl环境下一直困扰我的一个问题: 当内外环的半径很接近的时候，会渲染错误
结果在以cairo为后端的manimce中, 这个问题得到完美解决
"""
class test(Scene):
    def construct(self):
        """
        直接用两个圆的点集来构造
        """
        vm = VMobject()
        outer_circle = Circle(radius=2.1).rotate(PI/2).points[:64]
        inner_circle = Circle(radius=2).rotate(PI/2).points[:64][::-1]

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
        
        points_to_add = list(outer_circle) + line1 + list(inner_circle) + line2
        #points_to_add = list(outer_circle) + line1 + list(inner_circle)
        vm.append_points(points_to_add)
        vm.set_fill(GREEN, 1)
        vm.set_stroke(width=1)
        self.add(vm)
        vm.R = 2.1
        vm.dR = 0.1
        #self.wait()
        rec =  self.get_unwrapped(vm).scale(0.5).shift(DOWN*2.5)
        self.add(rec)

        #self.play(Transform(vm, rec))
        self.wait()
    
    def get_unwrapped(self, ring:VMobject, to_edge = LEFT, **kwargs):
        R = ring.R
        R_plus_dr = ring.R + ring.dR
        n_anchors = ring.get_num_curves()
        # print(n_anchors)
        # print(n_anchors//2)
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
                interpolate(result.points[-1], result.points[0], 0.3),
                interpolate(result.points[-1], result.points[0], 0.6),
                result.get_points()[0]] 
        result.append_points(line)

        result.set_style(
            stroke_color = ring.get_stroke_color(),
            stroke_width = ring.get_stroke_width(),
            fill_color = ring.get_fill_color(),
            fill_opacity = ring.get_fill_opacity(),
        )

        return result


