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

        # 每一维坐标全部加1
        circ_ref = circ.copy().apply_function(
            lambda x: x+1
        )
        circ_ref.set_color(YELLOW)
        animations = circ.animate.apply_function(
            lambda p: p + np.array(
                    [
                        np.sin(p[1]),
                        np.cos(p[0]),
                        0,
                    ]
        ))
        self.add(plane, circ, circ_ref)
        self.play(animations, run_time=2)

# github colpilot真厉害！下面的代码可以自动生成。
if __name__ == "__main__":
    with tempconfig({"preview": True}):
        scene = ApplyFuncExample()
        logger.info('rendering start...')
        scene.render()

