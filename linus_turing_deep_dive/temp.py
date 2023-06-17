# from manim import *

# def square_animation_override(square):
#     return GrowFromPoint(square, [-3, -2, 0])


# class MyScene(Scene):
#     def construct(self):
#         square = Square()
#         rotate_anim = GrowFromCenter(square)
#         self.play(rotate_anim)
#         self.wait()

#         Square.animation_overrides[GrowFromCenter] = square_animation_override

#         square = Square()
#         rotate_anim = GrowFromCenter(square)
#         self.play(rotate_anim)
#         self.wait()

# if __name__ == "__main__":
#     with tempconfig({"quality": "low_quality", "preview": True}):
#         scene = MyScene()
#         scene.render()



# from manim import *

# class CustomMobject(Rectangle):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
        
#         self.animation_overrides[FadeIn] = self._fade_in_override
    
#     def _fade_in_override(self, mobject):
#         return GrowFromCenter(mobject)

# class Test(Scene):
#     def construct(self):
#         custom_obj = CustomMobject()
#         self.play(FadeIn(custom_obj))

# if __name__ == "__main__":
#     with tempconfig({"quality": "low_quality", "preview": True}):
#         scene = Test()
#         scene.render()

# from manim import *

# class TableExamples(Scene):
#     def construct(self):
#         t0 = Table(
#             [["First", "Second"],
#             ["Third","Fourth"]],
#             row_labels=[Text("R1"), Text("R2")],
#             col_labels=[Text("C1"), Text("C2")],
#             top_left_entry=Text("TOP"))
#         t0.add_highlighted_cell((2,2), color=GREEN)
#         x_vals = np.linspace(-2,2,5)
#         y_vals = np.exp(x_vals)
#         t1 = DecimalTable(
#             [x_vals, y_vals],
#             row_labels=[MathTex("x"), MathTex("f(x)")],
#             include_outer_lines=True)
#         t1.add(t1.get_cell((2,2), color=RED))
#         t2 = MathTable(
#             [["+", 0, 5, 10],
#             [0, 0, 5, 10],
#             [2, 2, 7, 12],
#             [4, 4, 9, 14]],
#             include_outer_lines=True)
#         t2.get_horizontal_lines()[:3].set_color(BLUE)
#         t2.get_vertical_lines()[:3].set_color(BLUE)
#         t2.get_horizontal_lines()[:3].set_z_index(1)
#         cross = VGroup(
#             Line(UP + LEFT, DOWN + RIGHT),
#             Line(UP + RIGHT, DOWN + LEFT))
#         a = Circle().set_color(RED).scale(0.5)
#         b = cross.set_color(BLUE).scale(0.5)
#         t3 = MobjectTable(
#             [[a.copy(),b.copy(),a.copy()],
#             [b.copy(),a.copy(),a.copy()],
#             [a.copy(),b.copy(),b.copy()]])
#         t3.add(Line(
#             t3.get_corner(DL), t3.get_corner(UR)
#         ).set_color(RED))
#         vals = np.arange(1,21).reshape(5,4)
#         t4 = IntegerTable(
#             vals,
#             include_outer_lines=True
#         )
#         g1 = Group(t0, t1).scale(0.5).arrange(buff=1).to_edge(UP, buff=1)
#         g2 = Group(t2, t3, t4).scale(0.5).arrange(buff=1).to_edge(DOWN, buff=1)
#         self.add(g1, g2)

# if __name__ == "__main__":
#     with tempconfig({"quality": "high_quality", "preview": True}):
#         scene = TableExamples()
#         scene.render()

from manim import *

class MovingDots(Scene):
    def construct(self):
        plane = NumberPlane()
        d1,d2=Dot(color=BLUE, radius=0.2),Dot(color=GREEN, radius=0.2)
        #dg=VGroup(d1,d2).arrange(RIGHT,buff=2)
        d2.move_to(RIGHT*2)
        print(d1.get_center(),d2.get_center())

        l1=Line(d1.get_center(),d2.get_center()).set_color(RED)
        

        x=ValueTracker(0)
        y=ValueTracker(0)
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        l1.add_updater(lambda z: z.become(Line(d1.get_center(),d2.get_center())))

        d3=Dot(color=RED, radius=0.2)
        d3.add_updater(lambda z: z.set_x(l1.get_center()[0]).set_y(l1.get_center()[1]))

        self.add(plane, d1, d2, l1, d3)
        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(3))
        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = MovingDots()
        scene.render()