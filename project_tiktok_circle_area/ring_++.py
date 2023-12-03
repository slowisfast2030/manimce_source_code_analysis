from manim import *

"""
圆环的竖直相加
"""
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
        self.num_rings_in_ring_sum_start = 3

    def construct(self):
        rings = self.get_rings()
        self.add(rings)
        ring_sum, draw_ring_sum_anims = self.get_ring_sum(rings)
        self.play(*draw_ring_sum_anims)

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
    
    def get_ring_sum(self, rings):
        arranged_group = VGroup()
        tex_mobs = VGroup()
        for ring in rings:
            ring.generate_target()
            ring.target.set_stroke(width = 0)

        for ring in rings[:self.num_rings_in_ring_sum_start]:
            plus = Tex("+")
            arranged_group.add(ring.target)
            arranged_group.add(plus)
            tex_mobs.add(plus)
        dots = Tex("\\vdots")
        plus = Tex("+")
        arranged_group.add(dots, plus)
        tex_mobs.add(dots, plus)
        last_ring = rings[-1]

        arranged_group.add(last_ring.target)
        arranged_group.arrange(DOWN, buff = SMALL_BUFF)
        arranged_group.set_height(config.frame_height-1)
        arranged_group.to_corner(DOWN+LEFT, buff = MED_SMALL_BUFF)
        for mob in tex_mobs:
            mob.scale(0.7)

        middle_rings = rings[self.num_rings_in_ring_sum_start:-1]
        alphas = np.linspace(0, 1, len(middle_rings))
        for ring, alpha in zip(middle_rings, alphas):
            ring.target.set_fill(opacity = 0)
            ring.target.move_to(interpolate(
                dots.get_left(), last_ring.target.get_center(), alpha
            ))

        draw_ring_sum_anims = [Write(tex_mobs)]
        draw_ring_sum_anims += [
            MoveToTarget(
                ring,
                run_time = 3,
                path_arc = -np.pi/3,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.8)
            )
            for ring, alpha in zip(rings, np.linspace(0, 0.2, len(rings)))
        ]
        
        ring_sum = VGroup(rings, tex_mobs)
        ring_sum.rings = VGroup(*[r.target for r in rings])
        ring_sum.tex_mobs = tex_mobs
        
        return ring_sum, draw_ring_sum_anims