from manim import *

class ToyExample(Scene):
    def construct(self):
        orange_square = Square(color=ORANGE, fill_opacity=0.5)
        blue_circle = Circle(color=BLUE, fill_opacity=0.5)
        self.add(orange_square)
        self.play(ReplacementTransform(orange_square, blue_circle, run_time=3))
        small_dot = Dot()
        small_dot.add_updater(lambda mob: mob.next_to(blue_circle, DOWN))
        self.play(Create(small_dot))
        self.play(blue_circle.animate.shift(RIGHT))
        self.wait()
        self.play(FadeOut(blue_circle, small_dot))

with tempconfig({"quality": "medium_quality", "preview": False}):
    '''
    from manim import *顺带导入了config对象
    tempconfig上下文可以临时修改config对象的值
    '''
    print("config of toy example:", config)
    scene = ToyExample()
    '''
    跳转到render的源码，我们会发现：
    scene.render()函数内部分为三步：
    1.self.setup()
    2.self.construct()
    3.self.tear_down()
    '''
    scene.render()

'''
法一:
python toy_example.py

法二:
manim toy_example.py ToyExample -pql

思考:
1.严格来讲，法二的完整命令是
python -m manim toy_example.py ToyExample -pql
`toy_example.py ToyExample -pql`是manim的参数
2.法二的本质就是法一。会对ToyExample类进行实例化，并调用render函数。
'''

'''
在vscode中点击上述代码中的变量，并不会跳转到安装的库的源码，而是跳转到当前文件夹下载的源码。
vscode肯定有一个地方可以配置。
'''