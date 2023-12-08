from manim import *

class s1(Scene):
    def construct(self):
        pass

    # 引入三角形
    def introduce_triangle(self):
        triangle = Triangle()
        self.play(Write(triangle))
        self.wait()