from manim import *

class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number,  **kwargs)
        # Set start and end
        self.start = start
        self.end = end
        self.count = 0

    # def interpolate_mobject(self, alpha: float) -> None:
    # 如果查看animation源码，这里实现interpolate和interpolate_mobject都可以
    def interpolate(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        self.count += 1
        logger.info(f'custom_animation.py: Count.interpolate() {self.count}')
        #logger.info('custom_animation.py: Count.interpolate()')
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)

    def begin(self) -> None:
        # Set value of DecimalNumber to start
        logger.info('custom_animation.py: Count.begin()')
        # 此处执行self.interpolate(0)或者self.interpolate_mobject(0)都可以
        self.mobject.set_value(self.start)
    
    def finish(self) -> None:
        # Set value of DecimalNumber to end
        logger.info('custom_animation.py: Count.finish()')
        # 此处执行self.interpolate(1)或者self.interpolate_mobject(1)都可以
        self.mobject.set_value(self.end)


class CountingScene(Scene):
    def construct(self):
        # Create Decimal Number and add it to scene
        number = DecimalNumber().set_color(RED).scale(5)
        # Add an updater to keep the DecimalNumber centered as its value changes
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)
        self.wait()

        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)

        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "medium_quality", "preview": True, "disable_caching": False}):
        scene = CountingScene()
        logger.info('all is well')
        scene.render()

"""
执行这份脚本，可以发现如下输出：
INFO     custom_animation.py: Count.begin()
INFO     custom_animation.py: Count.interpolate()
INFO     custom_animation.py: Count.interpolate()
INFO     custom_animation.py: Count.interpolate()
INFO     custom_animation.py: Count.interpolate()
INFO     custom_animation.py: Count.interpolate()
...
INFO     custom_animation.py: Count.finish()

说明，所谓的动画效果，只不过是通过不断调用interpolate()函数来实现的。

引入了self.count变量，可以发现，interpolate()函数被调用的次数。
high_quality    interpolate()函数被调用了240次
medium_quality  interpolate()函数被调用了120次
low_quality     interpolate()函数被调用了60次
"""