from manim import *

def square_animation_override(square):
    return GrowFromPoint(square, [-3, -2, 0])


class MyScene(Scene):
    def construct(self):
        square = Square()
        rotate_anim = GrowFromCenter(square)
        self.play(rotate_anim)
        self.wait()

        Square.animation_overrides[GrowFromCenter] = square_animation_override
        
        square = Square()
        rotate_anim = GrowFromCenter(square)
        self.play(rotate_anim)
        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = MyScene()
        scene.render()
