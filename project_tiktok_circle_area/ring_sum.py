from manim import *

# 下面这几行设置竖屏
# config.frame_width = 9
# config.frame_height = 16

# config.pixel_width = 1080
# config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class RingSum(Scene):
    def setup(self):
        self.radius = 1.5
        self.fill_opacity = 0.75
        self.circle_corner = UP + LEFT
        self.dR = 0.1
        self.ring_colors = [BLUE, GREEN]
        self.corner = 2*UP + 5*LEFT

    def construct(self):
        rings = self.get_rings()
        self.add(rings)

    def get_ring(self, radius, dR, color = GREEN):
        ring = VMobject()
        outer_circle = Circle(radius=radius+dR).rotate(PI/2).get_points()[:64]
        inner_circle = Circle(radius=radius).rotate(PI/2).get_points()[:64][::-1]

        line1 = [outer_circle[-1], 
                 interpolate(outer_circle[-1], inner_circle[0], 0.3),
                 interpolate(outer_circle[-1], inner_circle[0], 0.6),
                 inner_circle[0]]
        
        line2 = [inner_circle[-1],
                interpolate(inner_circle[-1], outer_circle[0], 0.3),
                interpolate(inner_circle[-1], outer_circle[0], 0.6),
                outer_circle[0]]
        
        points_to_add = list(outer_circle) + line1 + list(inner_circle) + line2
        ring.append_points(points_to_add)
        ring.set_stroke(width = 0)
        ring.set_fill(color, opacity = 1)
        ring.move_to(self.corner)
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