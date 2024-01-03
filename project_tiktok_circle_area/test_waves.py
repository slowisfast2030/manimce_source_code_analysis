from manim import *

class ApplyingWaves(Scene):
    def construct(self):
        tex = Tex("WaveWaveWaveWaveWave").scale(2)
        self.play(ApplyWave(tex))
        self.play(ApplyWave(
            tex,
            direction=RIGHT,
            time_width=0.5,
            amplitude=0.3
        ))
        self.play(ApplyWave(
            tex,
            rate_func=linear,
            ripples=4
        ))