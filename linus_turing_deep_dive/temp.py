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



from manim import *

class CustomMobject(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.animation_overrides[FadeIn] = self._fade_in_override
    
    def _fade_in_override(self, mobject):
        return GrowFromCenter(mobject)

class Test(Scene):
    def construct(self):
        custom_obj = CustomMobject()
        self.play(FadeIn(custom_obj))

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = Test()
        scene.render()