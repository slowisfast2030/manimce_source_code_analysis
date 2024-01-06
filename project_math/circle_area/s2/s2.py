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
        self.wait()
        """
        分镜2:
        取出一个扇形, 下移
        """
        self.isolate_one_sector()
        self.wait()
        """
        分镜3:
        将圆分割为更多的扇形
        """
        self.play(FadeOut(self.sector))
        sectors_list = [
            self.get_sectors(self.circle, n_slices=n_slices)
            for n_slices in [30, 44, 60]
        ]
        for sectors in sectors_list:
            self.play(Transform(self.sectors, sectors),
                      lag_ratio = 0.5,
                      run_time = 1)
            self.wait()
        """
        分镜4:
        将扇形和圆环上移，移除文字
        """
        all_gr = VGroup(self.circle,
                        self.sectors)
        self.play(
            all_gr.animate.to_corner(UP, buff = MED_LARGE_BUFF*4),
            FadeOut(self.text),
            run_time=1
        )
        """
        分镜5:
        展开所有扇形, 得到近似的矩形
        """
        self.unwrap_sectors()




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

    def isolate_one_sector(self):
        sector = self.sectors[0]
        sector.generate_target()
        sector.target.rotate(-11/20*PI, about_point=ORIGIN)
        sector.target.shift(2.5*DOWN)
        self.play(MoveToTarget(sector))
        self.sector = sector

    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors
    
    def unwrap_sectors(self):
        """
        将sectors展开
        """
        sectors = self.sectors
        laid_sectors = sectors.copy()
        N = len(sectors)
        dtheta = TAU / N
        angles = np.arange(0, TAU, dtheta)
        for sector, angle in zip(laid_sectors, angles):
            sector.rotate(-90 * DEGREES - angle - dtheta / 2)

        laid_sectors.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        laid_sectors.move_to(1.5 * DOWN)

        self.play(
            sectors.animate.scale(1).to_corner(UP, buff=MED_LARGE_BUFF*3),
        )
        """
        深度思考
        """
        self.play(TransformFromCopy(sectors, laid_sectors, run_time=2))
        self.wait()

        """
        左右的锯齿的合并
        """
        lh, rh = laid_sectors[:N // 2], laid_sectors[N // 2:]
        lh.generate_target()
        rh.generate_target()
        rh.target.rotate(PI)
        rh.target.move_to(lh[0].get_top(), UL)
        VGroup(lh.target, rh.target).set_x(0)
        rh.target.shift(UP)
        lh.target.shift(DOWN)

        self.play(
            MoveToTarget(lh, run_time=1.5),
            MoveToTarget(rh, run_time=1.5, path_arc=PI),
        )
        self.play(
            lh.animate.shift(UP),
            rh.animate.shift(DOWN),
        )