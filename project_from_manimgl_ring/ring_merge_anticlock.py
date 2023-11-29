from manim import *

"""
将circle的点集设置为顺时针
会出现奇怪的渲染效果
"""
class test(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        ring = Circle(radius = 2, num_components=9).center()
        ring.set_stroke(width = 0.5)
        ring.set_fill(RED,0.5)

        # 将ring的点集变为顺时针
        #ring.rotate(PI, RIGHT)

        for index, point in enumerate(ring.points):
            dot = Dot(point)
            label = Text(str(index), font_size=24).next_to(dot, point-ring.get_center(), buff=0.1)
            self.add(dot, label)

        self.add(ring)
