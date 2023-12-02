"""
Sector Sum:
1.将整个圆分成n个扇形, 每个扇形的角度为360/n
2.将上半圆和下半圆分别移到整个圆的下方，然后展开为锯齿状
3.合并两个锯齿状, 得到近似的矩形
"""
from manim import *
import itertools as it

class SectorSum(Scene):
    n_slices = 20
    sector_stroke_width = 1.0

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

        """
        将sectors展开
        """
        laid_sectors = sectors.copy()
        N = len(sectors)
        dtheta = TAU / N
        angles = np.arange(0, TAU, dtheta)
        for sector, angle in zip(laid_sectors, angles):
            sector.rotate(-90 * DEGREES - angle - dtheta / 2)

        laid_sectors.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        laid_sectors.move_to(1.5 * DOWN)

        self.play(
            sectors.animate.scale(0.7).to_corner(UL),
            question.animate.to_corner(UR),
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
        self.wait()

        """genius
        天才的做法
        """
        self.play(*(
            LaggedStart(*(
                ShowPassingFlash(piece, time_width=2)
                for piece in group.copy().set_fill(opacity=0).set_stroke(RED, 5)
            ), lag_ratio=0.02, run_time=3)
            for group in [laid_sectors, sectors]
        ))
        self.wait()
        

    def get_sectors(self, circle, n_slices=20, fill_colors=[BLUE_D, BLUE_E]):
        angle = TAU / n_slices
        sectors = VGroup(*(
            Sector(angle=angle, start_angle=i * angle, fill_color=color, fill_opacity=1)
            for i, color in zip(range(n_slices), it.cycle(fill_colors))
        ))
        sectors.set_stroke(WHITE, self.sector_stroke_width)
        sectors.replace(circle, stretch=True)
        return sectors