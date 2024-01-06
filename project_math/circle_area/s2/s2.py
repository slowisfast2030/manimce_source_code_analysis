"""
Sector Sum:
1.将整个圆分成n个扇形, 每个扇形的角度为360/n
2.将上半圆和下半圆分别移到整个圆的下方，然后展开为锯齿状
3.合并两个锯齿状, 得到近似的矩形
"""
from manim import *
import itertools as it

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920

class ShowCreation(Create):
    pass

class s2(Scene):
    def setup(self):
        self.n_slices = 60
        self.sector_stroke_width = 1.0

    def construct(self):
        radius = 2.0

        # Slice up circle
        circle = Circle(radius=radius)
        circle.set_stroke(WHITE, 1)
        circle.set_fill(BLUE_E, 1)

        question = Text("Area?")
        question.next_to(circle, UP)

        sectors = self.get_sectors(circle, n_slices=self.n_slices)

        self.play(
            DrawBorderThenFill(circle),
            Write(question, stroke_color=WHITE)
        )
        self.wait()
        """
        这个效果挺不错
        sectors会覆盖在circle上
        """
        self.play(Write(sectors))
        self.remove(circle)

    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors