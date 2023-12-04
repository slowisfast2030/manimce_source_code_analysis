from manim import *
import itertools as it

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
        self.circle_bottom_location = (config.frame_height/4 - 1)*DOWN
        self.n_slices = 20
        self.sector_stroke_width = 1.0
        self.ring_stroke_width = 1.0

    def construct(self):
        self.introduce_circle()
        self.introduce_index_area()
        
    def introduce_circle(self):
        # 上圆和下圆
        self.circle_top = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle_bottom = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )

        # 分别移动到上下屏
        self.circle_top.move_to(self.circle_top_location)
        self.circle_bottom.move_to(self.circle_bottom_location)

        anim_kwargs = {
            "run_time" : 3,
            "lag_ratio" : 0.1
        }

        # 获取rings和sectors
        rings = VGroup(*reversed(self.get_rings()))
        sectors = self.get_sectors(self.circle_bottom, n_slices=self.n_slices)

        self.play(
            FadeIn(rings, **anim_kwargs),
            Write(sectors, **anim_kwargs),
        )

        self.rings = rings
        self.sectors = sectors

    def introduce_index_area(self):
        vg = VGroup(self.rings, self.sectors)
        vg.generate_target()
        vg.target.arrange(RIGHT, buff = LARGE_BUFF).scale(0.2)
        vg.target.to_corner(UR, buff = LARGE_BUFF*0.5).shift(DOWN)

        area = Text("面积").match_height(vg.target).set_color_by_gradient(GREEN, BLUE)
        area.to_corner(UL, buff = LARGE_BUFF*0.5).shift(DOWN)
        self.play(MoveToTarget(vg),
                  Write(area))
        
        self.vg = vg
        self.area = area



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
        ring.set_stroke(width = self.ring_stroke_width)
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
    
    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors