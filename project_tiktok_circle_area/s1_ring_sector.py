from manim import *

"""
上下屏各出现一个圆
分别采取ring和sector的切割方法
"""
# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

# 一个很聪明的方案
class ShowCreation(Create):
    pass

class s1(Scene):
    def setup(self):
        self.radius = 2
        self.dR = 0.2
        self.stroke_color = WHITE
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75
        self.circle_corner = UP + LEFT
        self.radial_line_color = MAROON_B
        self.ring_colors = [BLUE, GREEN]
        self.unwrapped_tip = ORIGIN
        self.circle_top_location = (config.frame_height/4 - 1)*UP
        self.circle_bottom = (config.frame_height/4 - 1)*DOWN

    def construct(self):
        self.circle_top = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle_top.move_to(self.circle_top_location)
        self.play(
            self.circle_top.animate.set_fill(self.fill_color, self.fill_opacity),
            run_time=1
        )

        rings = VGroup(*reversed(self.get_rings()))
        ring_anim_kwargs = {
            "run_time" : 3,
            "lag_ratio" : 0.1
        }
        self.add(rings)

        self.play(
            FadeIn(rings, **ring_anim_kwargs),
        )

    def get_ring(self, radius, dR, color = BLUE):
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
        ring.move_to(self.circle_top)
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