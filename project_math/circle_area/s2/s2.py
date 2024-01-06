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
        self.radius = 2.0
        self.stroke_color = WHITE
        self.stroke_width = 2
        self.fill_color = BLUE_E
        self.fill_opacity = 0.75

        self.n_slices = 20
        self.sector_stroke_width = 1.0

    def construct(self):
        """
        分镜1:
        显示圆的分割
        """
        self.split_circle()
        

        """
        分镜2:
        取出一个扇形, 下移
        """
        sector = self.sectors[0]

    def split_circle(self):
        circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        circle.move_to(ORIGIN)
        circle.move_to(ORIGIN)  
        circle.set_stroke(WHITE, 1)
        circle.set_fill(BLUE_E, 0.75)

        text_split = Text("圆的分割").scale(0.8)
        text_split.set_color_by_gradient(BLUE, GREEN)
        text_split.to_corner(UP, buff = MED_LARGE_BUFF*6)

        sectors = self.get_sectors(circle, n_slices=self.n_slices)

        self.play(
            DrawBorderThenFill(circle),
            
        )
        #self.wait()
        
        self.play(Write(sectors),
                  Write(text_split))
        
        self.text = text_split
        self.circle = circle
        self.sectors = sectors

    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors