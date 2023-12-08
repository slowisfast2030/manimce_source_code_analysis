from manim import *

class s1(Scene):
    def construct(self):
        self.introduce_triangle()
        pass

    # 引入三角形
    def introduce_triangle(self):
        triangle = Polygon([-4,0,0],
                           [0,0,0],
                           [0,3,0])
        self.play(Write(triangle), run_time=2)
        self.wait()