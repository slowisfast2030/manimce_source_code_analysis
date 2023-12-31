from manim import *

"""
圆环的竖直相加
用加号相连
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
        # 将64改为32。因为圆弧一共只有32个点
        # 将32改为28。可以更清楚的看见缺口位置
        outer_circle = Circle(radius=radius+dR).rotate(PI/2).get_points()[:28]
        inner_circle = Circle(radius=radius).rotate(PI/2).get_points()[:28][::-1]

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
    
    # 这个函数和艺术品一样
    def get_ring_sum(self, rings):
        """
        整体的思路：
        将前3个圆环(target)和最后一个圆环(target)用加号和省略号相连
        然后通过arrange函数排列好

        剩余的圆环(target)设置为透明，移动到省略号和最后一个圆环之间

        至此，每一个圆环(target)的位置都已经确定好了
        加号和省略号也已经确定好了

        最后, 通过动画将所有的圆环(target)和加号、省略号一起显示出来
        """
        # target和符号
        arranged_group = VGroup()
        # 符号
        tex_mobs = VGroup()
        for ring in rings:
            ring.generate_target()
            ring.target.set_stroke(width = 0)

        # 前3个圆环
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
        # 最后一个圆环
        arranged_group.add(last_ring.target)
        arranged_group.arrange(DOWN, buff = SMALL_BUFF)
        # 调整整体的高度
        arranged_group.set_height(config.frame_height-1)
        arranged_group.to_corner(DOWN+LEFT, buff = MED_SMALL_BUFF)
        for mob in tex_mobs:
            mob.scale(0.7)

        # 为剩余的圆环设置style和位置
        middle_rings = rings[self.num_rings_in_ring_sum_start:-1]
        alphas = np.linspace(0, 1, len(middle_rings))
        for ring, alpha in zip(middle_rings, alphas):
            ring.target.set_fill(opacity = 0)
            ring.target.move_to(interpolate(
                #dots.get_left(), last_ring.target.get_center(), alpha
                dots.get_center(), last_ring.target.get_center(), alpha
            ))

        #print(dots.get_left())
        #print(dots.get_center())
        """
        [-5.33114233  0.13028663  0.        ]
        [-5.31205727  0.13028663  0.        ]
        """

        draw_ring_sum_anims = [Write(tex_mobs)]
        """
        genius!!!
        """
        # 注意path_arc参数
        # 负号表示顺时针，正号表示逆时针
        # 绝对值越大，弧线角度越大
        draw_ring_sum_anims += [
            MoveToTarget(
                ring,
                run_time = 3,
                #path_arc = -np.pi/3,
                path_arc = -np.pi/3,
                rate_func = squish_rate_func(smooth, alpha, alpha+0.8)
            )
            for ring, alpha in zip(rings, np.linspace(0, 0.2, len(rings)))
        ]
        """
        深入对比下上面代码中的rate_func和下面代码中的lag_ratio

        ring_anim_kwargs = {
            "run_time" : 3,
            "lag_ratio" : 0.1
        }

        self.play(
            Transform(rings, unwrapped_rings, **ring_anim_kwargs),
        )

        注: rings和unwrapped_rings是VGroup

        一点简单的思考:
        如果只有一个MoveToTarget动画, 那么rate_func参数没意义
        如果有多个MoveToTarget动画, 那么rate_func参数有意义

        本质来看, rate_func和lag_ratio所达到的效果是类似的
        同类动画如果不施加这两个参数, 会显得很生硬
        """
        
        ring_sum = VGroup(rings, tex_mobs)
        ring_sum.rings = VGroup(*[r.target for r in rings])
        ring_sum.tex_mobs = tex_mobs
        
        return ring_sum, draw_ring_sum_anims
    
"""from gpt4
Here's what the path_arc parameter does in detail:

Purpose: It determines the curvature of the path that the mobject takes 
from its initial to its final position. Instead of moving in a straight 
line, the mobject will move along an arc.

Value: The value of path_arc is given in radians. In your code, np.pi/2 
is used, which is equivalent to 90 degrees. This means the mobject will 
move along a quarter-circle arc from its starting point to its ending point.

Visualization: If you imagine the starting and ending points of the mobject's 
path as two points on a circle, the path_arc determines how much of that 
circle's circumference the mobject will follow. A path_arc of np.pi/2 means 
it follows a path equivalent to a quarter of the circle's circumference.
"""