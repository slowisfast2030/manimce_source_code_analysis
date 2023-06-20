from manim import *

class ApplyFuncExample(Scene):
    def construct(self):
        plane = NumberPlane()
        circ = Circle().scale(1.5)
        # circ_ref = circ.copy()
        # circ.apply_complex_function(
        #     lambda x: np.exp(x*1j)
        # )
        # t = ValueTracker(0)
        # circ.add_updater(
        #     lambda x: x.become(circ_ref.copy().apply_complex_function(
        #         lambda x: np.exp(x+t.get_value()*1j)
        #     )).set_color(BLUE)
        # )
        # self.add(circ_ref)
        # self.play(TransformFromCopy(circ_ref, circ))
        # self.play(t.animate.set_value(TAU), run_time=3)

        # animations = circ.animate.apply_complex_function(
        #     lambda x: np.exp(x*1j)
        # )
        animations = circ.animate.apply_function(
            lambda p: [p[0]+2, p[1]+2, 0]
        )
        self.add(plane, circ)
        self.play(animations, run_time=3)

ApplyFuncExample().render()
