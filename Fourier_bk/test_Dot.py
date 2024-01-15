from manim import *

class GlowingDotScene(Scene):
    def construct(self):
        # 创建一个点
        dot = Dot(point=ORIGIN, color=YELLOW)

        # 增加点的大小和光晕效果
        dot.scale(1.5)  # 改变点的大小
        dot.set_glow_factor(1)  # 设置发光效果

        # 将点添加到场景中
        self.add(dot)
        self.wait(2)
