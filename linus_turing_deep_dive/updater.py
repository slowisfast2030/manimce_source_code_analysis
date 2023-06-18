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
    with tempconfig({"quality": "high_quality", "preview": False, "disable_caching": False}):
        scene = MovingDots()
        scene.render()