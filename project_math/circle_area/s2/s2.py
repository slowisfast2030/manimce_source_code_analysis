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

        self.radius_line_color = MAROON_B

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

        text_more_sectors = Text("更多的扇形").scale(0.8)
        text_more_sectors.set_color_by_gradient(BLUE, GREEN)
        text_more_sectors.to_corner(UP, buff = MED_LARGE_BUFF*6)
        text_more_sectors_en = Text("More sectors").scale(0.8)
        text_more_sectors_en.set_color_by_gradient(BLUE, GREEN)
        text_more_sectors_en.next_to(text_more_sectors, DOWN, buff = MED_LARGE_BUFF*0.5)

        self.play(FadeOut(self.text),
                    FadeOut(self.text_en),
                    FadeIn(text_more_sectors),
                    FadeIn(text_more_sectors_en))
        self.text = text_more_sectors
        self.text_en = text_more_sectors_en

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
                        self.radius_group,
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

        """
        分镜6:
        计算面积
        """
        line_width = Line(self.lh[0].get_corner(DL), self.lh[-1].get_corner(DR))
        line_width.set_color(self.radius_line_color)
        line_width_br = Brace(line_width, DOWN)
        text_width = line_width_br.get_tex("\pi R")

        line_height = Line(self.lh[15].get_bottom(), self.lh[15].get_top()) 
        line_height.set_color(self.radius_line_color)
        line_height_br = Brace(line_height, RIGHT)
        text_height = line_height_br.get_tex("R")

        self.play(ShowCreation(line_height),
                  ShowCreation(line_width),
                  GrowFromCenter(line_width_br),
                  GrowFromCenter(line_height_br),
                  Write(text_width),
                  Write(text_height))

        area = Text("面积").scale(0.8).set_color_by_gradient(BLUE, BLUE)
        l_brace = MathTex(r"(")
        r_brace = MathTex(r")=")
        height = MathTex(r"R")
        mul = MathTex(r"\times")
        bottom = MathTex(r"\pi R")
        remains = MathTex(r"= \pi R^2")
        #r_brace = MathTex(r")")
        small_circle = self.circle.copy().match_height(l_brace)
        area_gr = VGroup(area, 
                         l_brace, 
                         small_circle, 
                         r_brace,
                         height,
                         mul,
                         bottom,
                         remains).arrange(RIGHT, buff = SMALL_BUFF)
        
        pos = (self.circle.get_bottom() + self.lh.get_top())/2
        area_gr.move_to(pos)
        self.add(area_gr)
        #self.play(Write(area_gr))
        self.play(
            FadeIn(area),
            Write(l_brace),
            TransformFromCopy(self.circle, small_circle),
            Write(r_brace),
            Write(mul),
            Write(remains),
            TransformFromCopy(text_height, height),
            TransformFromCopy(text_width, bottom),
            run_time = 2
        )



    def split_circle(self):
        self.circle = Circle(
            radius = self.radius,
            stroke_color = self.stroke_color,
            stroke_width=self.stroke_width,
            fill_color = self.fill_color,
            fill_opacity = self.fill_opacity,
        )
        self.circle.move_to(ORIGIN)
        self.radius_line = Line(
            self.circle.get_center(),
            self.circle.get_right(),
            color = self.radius_line_color
        )
        self.radius_brace = Brace(self.radius_line, buff = SMALL_BUFF)
        self.radius_label = self.radius_brace.get_tex("R", buff = SMALL_BUFF)

        self.radius_group = VGroup(
            self.radius_line, self.radius_brace, self.radius_label
        )
        self.play(
            ShowCreation(self.radius_line),
            GrowFromCenter(self.radius_brace),
            Write(self.radius_label),
        )
        self.circle.set_fill(opacity = 0)

        self.play(
            Rotate(
                self.radius_line, 2*PI-0.001, 
                about_point = self.circle.get_center(),
            ),
            ShowCreation(self.circle),
            
            run_time = 1
        )

        # 当circle执行了set_fill的动画后会覆盖掉radius_group
        # 所以需要将radius_group放到circle的上面
        self.bring_to_front(self.radius_group)

        text_split = Text("圆的分割").scale(0.8)
        text_split.set_color_by_gradient(BLUE, GREEN)
        text_split.to_corner(UP, buff = MED_LARGE_BUFF*6)
        text_split_en = Text("Division of circle").scale(0.8)
        text_split_en.set_color_by_gradient(BLUE, GREEN)
        text_split_en.next_to(text_split, DOWN, buff = MED_LARGE_BUFF*0.5)

        sectors = self.get_sectors(self.circle, n_slices=self.n_slices)
        
        self.play(
            Write(sectors),
            Write(text_split),
            Write(text_split_en),)
        
        
        
        self.text = text_split
        self.text_en = text_split_en
        self.sectors = sectors

    def isolate_one_sector(self):
        text_one_sector = Text("取出一个扇形").scale(0.8)
        text_one_sector.set_color_by_gradient(BLUE, GREEN)
        text_one_sector.to_corner(UP, buff = MED_LARGE_BUFF*6)
        text_one_sector_en = Text("Isolate one sector").scale(0.8)
        text_one_sector_en.set_color_by_gradient(BLUE, GREEN)
        text_one_sector_en.next_to(text_one_sector, DOWN, buff = MED_LARGE_BUFF*0.5)

        self.remove(self.radius_group)
        sector = self.sectors[0]
        sector.generate_target()
        sector.target.rotate(-11/20*PI, about_point=ORIGIN)
        sector.target.shift(2.5*DOWN)
        self.play(
            FadeOut(self.text),
            FadeOut(self.text_en),
            FadeIn(text_one_sector),
            FadeIn(text_one_sector_en),
            MoveToTarget(sector))
        self.sector = sector
        self.text = text_one_sector
        self.text_en = text_one_sector_en

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
        self.circle.set_stroke(BLACK)
        self.circle.set_fill(opacity = 1)
        sectors = self.sectors
        laid_sectors = sectors.copy()
        N = len(sectors)
        dtheta = TAU / N
        angles = np.arange(0, TAU, dtheta)
        for sector, angle in zip(laid_sectors, angles):
            sector.rotate(-90 * DEGREES - angle - dtheta / 2)

        laid_sectors.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        laid_sectors.move_to(1.5 * DOWN)

        """
        深度思考
        """
        self.play(Transform(sectors, laid_sectors, run_time=2))
        self.wait()

        """
        左右的锯齿的合并
        """
        lh, rh = sectors[:N // 2], sectors[N // 2:]
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

        self.lh = lh
        self.rh = rh
