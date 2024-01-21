from manim import *
import itertools
import os

# 下面这几行设置竖屏
config.frame_width = 9
config.frame_height = 16

config.pixel_width = 1080
config.pixel_height = 1920
# manimce v0.17.3
class FourierCirclesSceneWithCamera(ZoomedScene):
    def __init__(self, 
    n_vectors=10,
    big_radius=2,
    vector_config={
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
    },
    circle_color=BLUE,
    circle_config={
            "stroke_width": 1,
        },
    base_frequency=1,
    slow_factor=0.5,
    Hide_0th_vector=True,
    parametric_function_step_size=0.001,
    drawn_path_color=RED,
    drawn_path_stroke_width=3,
    interpolate_config=[0,1],
    zoomed_display_height= 3,
    zoomed_display_width= 4,
    image_frame_stroke_width=3,
    zoom_factor=0.3,
    default_frame_stroke_width=0.1,
    cairo_line_width_multiple=0.01,
    zoom_camera_to_full_screen_config= {
            "run_time": 3,
            "func": smooth,
            "velocity_factor": 1
        },
    zoomed_display_corner=UL,
    zoomed_display_corner_buff=0.0,
    **kwargs,
    ):
        self.circle_color=circle_color
        self.n_vectors=n_vectors
        self.big_radius=big_radius
        self.vector_config=vector_config
        self.circle_config=circle_config
        self.base_frequency=base_frequency
        self.slow_factor=slow_factor
        self.parametric_function_step_size=parametric_function_step_size
        self.drawn_path_color=drawn_path_color
        self.drawn_path_stroke_width=drawn_path_stroke_width
        self.interpolate_config=interpolate_config
        self.zoomed_display_height=zoomed_display_height
        self.zoomed_display_width=zoomed_display_width
        self.image_frame_stroke_width=image_frame_stroke_width
        self.zoom_factor=zoom_factor
        self.default_frame_stroke_width=default_frame_stroke_width
        self.cairo_line_width_multiple=cairo_line_width_multiple
        self.zoom_camera_to_full_screen_config=zoom_camera_to_full_screen_config
        
        self.Hide_0th_vector=Hide_0th_vector
        self.zoomed_display_corner=zoomed_display_corner
        self.zoomed_display_corner_buff=zoomed_display_corner_buff
        self.zoom_position=lambda mob: mob.next_to(self.zoomed_display_corner,buff=self.zoomed_display_corner_buff) 
        ZoomedScene.__init__(self,camera_class=MultiCamera, zoom_factor=self.zoom_factor,zoomed_display_width=self.zoomed_display_width,
        zoomed_display_height=self.zoomed_display_height,
        image_frame_stroke_width=self.image_frame_stroke_width,
        zoomed_display_corner=self.zoomed_display_corner,
        zoomed_display_corner_buff=self.zoomed_display_corner_buff,
        **kwargs)
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )

        """"
        自定义了一个时钟

        由于整个动画的播放时间为self.wait(1/self.slow_factor)
        导致了self.vector_clock的最大值为1
        """
        def add_dt(m,dt):
            m.increment_value(dt*self.slow_factor_tracker.get_value())
        self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
        self.add(self.vector_clock)

    

    def setup(self):
        ZoomedScene.setup(self)
        

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for _ in range(self.n_vectors)]

    def get_color_iterator(self):
        return itertools.cycle(self.drawn_path_color)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        """
        self.center_tracker只使用了一次
        是第一个向量的旋转中心

        猜测: 后续还需要将其移到coefficients[0]的位置

        更新: 在执行这个函数以前, coefs[0]已经被设置为了0+2j
        需要搞明白, 第一个vector的旋转中心是何时移到这个位UP

        更新:
        第一个vector在整个动画中被隐藏了
        第一个vector是静止的, 旋转中心即起点是原点
        所以，在动画中, 第一个可见的向量(即第二个向量)的起点其实是原点和coeffs[0]的和
        """
        self.center_tracker = VectorizedPoint(ORIGIN)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        """
        有一系列vector
        每一个vector的旋转中心都是上一个vector的终点
        环环相扣

        所以, 这里的last_vector是上一个vector
        而不是最后一个vector
        """
        last_vector = None
        
        for i in range(len(freqs)):
            freq=freqs[i]
            coefficient=coefficients[i]

            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            
            if i<len(freqs)-1:
                """
                返回添加了updater的vector
                有点震惊
                """
                vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            else:
                """
                这里的取名就有点歧义了
                这里的last就不是上一个的意思了
                而是最后一个
                """
                vector=self.get_rotating_last_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            
            """
            将频率为0的向量隐藏
            因为频率为0的向量, 是静止的
            """
            if (i==0 and self.Hide_0th_vector):
                vector.set_opacity(0)

            vectors.add(vector)
            """
            重置上一个vector
            """
            last_vector = vector
        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func):
        """
        获取每一个旋转向量
        coefficient: 复数。模长为向量长度，幅角为向量初始旋转角度
        freq: 旋转频率
        center_func: 函数。返回向量的旋转中心
        """
        vector = Vector(abs(coefficient)*RIGHT, **self.vector_config)

        """
        获取向量的初始相位
        """
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)

        """
        对于每一个vector而言, 都有一个freq, coefficient, center_func
        最让人眼前一亮的是center_func
        center_func是一个函数, 返回的是vector的旋转中心
        每一帧调用这个函数一次, 计算新的旋转中心

        在python中, 从来没有见过将函数作为对象的属性
        """
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func

        """
        使用updater的示例:

        def update_dot(mob, dt):
            mob.rotate_about_origin(dt)

        dot.add_updater(update_dot)
        """
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector, dt):
        """
        每一帧调用一次
        更新向量的长度和角度和起点
        """
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def update_last_vector(self, vector, dt):
        """
        和update_vector一样
        """
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        #vector_end=vector.get_end()
        #self.zoomed_camera.frame.move_to(vector_end)
        return vector

    def get_rotating_last_vector(self, coefficient, freq, center_func):
        """
        获取最后一个旋转向量
        和get_rotating_vector一样
        """
        vector = Vector(abs(coefficient)*RIGHT, **self.vector_config)
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_last_vector)
        return vector

    def get_circles(self, vectors):
        """
        基于vectors集合, 获取circles集合
        """
        ans=VGroup(*[
            self.get_circle(
                vector,
            )
            for vector in vectors
        ])

        """
        隐藏第一个circle
        """
        if self.Hide_0th_vector:
            ans[0].set_opacity(0)
        
        return ans

    def get_circle(self, vector):
        """
        对于每一个circle来讲
        半径应该是固定的
        不需要为半径添加updater
        """
        circle = Circle(color=self.circle_color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set(width=2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        """
        所有的vectors首尾相连
        最后一个vector的终点是t的函数
        """
        coefs = np.array([v.coefficient for v in vectors])
        freqs = np.array([v.freq for v in vectors])
        """
        第一个vector的起点其实是原点
        """
        center = vectors[0].get_start()
        """
        如果 coefs = [c1, c2], freqs = [f1, f2]
        先拿出c1, f1
        然后拿出c2, f2
        最后求和
        """
        def compute_curve(t):
            """
            看来第一版的作者也是煞费苦心
            """
            """
            lambda t: center + functools.reduce(operator.add, [
                complex_to_R3(
                    coef * np.exp(TAU * 1j * freq * t)
                )
                for coef, freq in zip(coefs, freqs)
            ])
            """
            return complex_to_R3(coefs.dot(np.exp(TAU*1j*freqs*t)))

        path = ParametricFunction(compute_curve,
            t_range=[0,1,self.parametric_function_step_size],
            color=self.drawn_path_color,use_smoothing=False
        )
        return path

    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, fade=False, **kwargs):
        """
        初步理解:
        如何显示画图的过程:
        将图像分成n段, 每一段的宽度为stroke_width
        还没有画出来的部分, 宽度为0

        也就是说, 整张图一开始已经存在
        只是让你在每一时刻只看见一部分
        """
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        """
        转换后, path就分为了很多段
        经过打印, 发现是1000份

        查看path的代码, 发现是ParametricFunction
        ParametricFunction的参数t_range=[0,1,0.001]

        如果整个路径被划分为1000份
        每一帧可以显示一份
        那么一共需要1000帧的时间
        假设1秒钟30帧
        那么一共需要33.3333秒的时间
        """
        broken_path = CurvesAsSubmobjects(path)
        broken_path.curr_time = 0
        start, end = self.interpolate_config

        def update_path(path, dt):
            alpha = self.get_drawn_path_alpha()
            n_curves = len(path)
            #print(n_curves)
            #1000
            for a, sp in zip(np.linspace(0, 1, n_curves), path):
                b = (alpha - a)
                if b < 0:
                    width = 0
                else:
                    if fade:
                        width = stroke_width * interpolate(start, end, (1 - (b % 1)))
                    else:
                        width = stroke_width
                sp.set_stroke(width=width)
            path.curr_time += dt
            return path

        broken_path.set_color(self.drawn_path_color)
        broken_path.add_updater(update_path)
        return broken_path

    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        """
        并没有使用这个函数
        """
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= ORIGIN
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]

class Normal_happy_pro(FourierCirclesSceneWithCamera):
    """
    显示汉字"乐"
    顺序显示，非并行
    """
    def read_coefs_freqs(self,filename, vector_num):
        f=open(filename,"r")
        freqs=[]
        coefs=[]
        lines=f.readlines()
        for line in lines:
            a,b=line.split()
            freqs.append(int(a))
            coefs.append(complex(b))
        
        coefs=coefs[:vector_num]
        freqs=freqs[:vector_num]
        coefs=np.array(coefs)
        freqs=np.array(freqs)

        return coefs,freqs
       
    def construct(self):
        super().__init__(n_vectors=200,#控制向量数量
        slow_factor=1/3,#控制时间长短，slow factor越小，画的速度越慢,      
        cairo_line_width_multiple=0.01,#控制缩放镜头里线的长短
        default_frame_stroke_width=0.1,)#控制缩放镜头边框长短
        
        part_length = [1014.1104089718626,
                       190.25475395399974,
                       196.97960990760595]

        # 读取三部分参数 
        coefs_0, freqs_0=self.read_coefs_freqs(r"Ale_0.txt", self.n_vectors)
        coefs_1, freqs_1=self.read_coefs_freqs(r"Ale_1.txt", self.n_vectors)
        coefs_2, freqs_2=self.read_coefs_freqs(r"Ale_2.txt", self.n_vectors)

        # 需要缩小参数
        coefs_0/=22
        coefs_1/=22
        coefs_2/=22
    
        #coefs_i[0]控制了图像的中心位置，需要微调到最适合的位置
        shift_val = complex(0,0) - coefs_0[0]
        coefs_0[0]+=shift_val
        coefs_1[0]+=shift_val
        coefs_2[0]+=shift_val

        self.slow_factor_tracker = ValueTracker(
            self.slow_factor/(part_length[0]/part_length[1])
        ) 
        def add_dt(m,dt):
            m.increment_value(dt*self.slow_factor_tracker.get_value())

        # 画出三部分
        self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
        self.add(self.vector_clock)
        le0_vector=self.get_rotating_vectors(coefficients=coefs_0,freqs=freqs_0)
        le0_circle=self.get_circles(le0_vector)
        le0_drawn_path=self.get_drawn_path(le0_vector)
        self.add(le0_vector,le0_circle,le0_drawn_path)
        self.wait((1/self.slow_factor)*(part_length[0]/part_length[1]) + 1/15)
        """
        清除上述对象的所有updater
        """
        for v in le0_vector:
            v.clear_updaters()
        for c in le0_circle:
            c.clear_updaters()
        le0_drawn_path.clear_updaters()
        self.remove(*[le0_vector], *[le0_circle], self.vector_clock)

        """
        为什么在开始前已经有了路径的轮廓？
        和self.vector_clock有关
        """
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor/(part_length[1]/part_length[1])
        ) 
        self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
        self.add(self.vector_clock)
        le1_vector=self.get_rotating_vectors(coefficients=coefs_1,freqs=freqs_1)
        le1_circle=self.get_circles(le1_vector)
        le1_drawn_path=self.get_drawn_path(le1_vector)
        self.add(le1_vector,le1_circle,le1_drawn_path)
        self.wait(1/self.slow_factor + 1/15)
        """
        清除上述对象的所有updater
        """
        for v in le1_vector:
            v.clear_updaters()
        for c in le1_circle:
            c.clear_updaters()
        le1_drawn_path.clear_updaters()
        self.remove(*[le1_vector], *[le1_circle], self.vector_clock)

        self.slow_factor_tracker = ValueTracker(
            self.slow_factor/(part_length[2]/part_length[1])
        ) 
        self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
        self.add(self.vector_clock)
        le2_vector=self.get_rotating_vectors(coefficients=coefs_2,freqs=freqs_2)
        le2_circle=self.get_circles(le2_vector)
        le2_drawn_path=self.get_drawn_path(le2_vector)
        self.add(le2_vector,le2_circle,le2_drawn_path)
        self.wait((1/self.slow_factor)*(part_length[2]/part_length[1]) + 1/15)

class Normal_happy_pro_plus(FourierCirclesSceneWithCamera):
    """
    显示汉字"乐"
    """
    def read_coefs_freqs(self,filename, vector_num):
        f=open(filename,"r")
        freqs=[]
        coefs=[]
        lines=f.readlines()
        for line in lines:
            a,b=line.split()
            freqs.append(int(a))
            coefs.append(complex(b))
        
        coefs=coefs[:vector_num]
        freqs=freqs[:vector_num]
        coefs=np.array(coefs)
        freqs=np.array(freqs)

        return coefs,freqs
       
    def construct(self):
        super().__init__()


        def process_word(n_vectors, all_time, svg_path, origin, scale_factor):
            self.n_vectors = n_vectors
            all_time = all_time
            svg_path = svg_path
            origin = origin

            base_name = os.path.splitext(svg_path)[0]  # Extracts 'Ale' from 'Ale.svg'

            part_length = []
            part_length_file = f"{base_name}_part_length.txt"
            with open(part_length_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.split()
                    part_length.append(float(line[1]))
            
            print(part_length)
            # 初始化存储结果的字典
            coefs_freqs_dicts = []

            # 循环处理每个文件
            for i in range(len(part_length)):
                file_name = f"{base_name}_{i}.txt"
                coefs, freqs = self.read_coefs_freqs(file_name, self.n_vectors)
                # 整体缩小参数
                coefs/=scale_factor
                coefs_freqs_dicts.append({'coefs': coefs, 'freqs': freqs})

            shift_val = origin - coefs_freqs_dicts[0]["coefs"][0] 
            for i in range(len(part_length)):
                coefs_freqs_dicts[i]["coefs"][0]+=shift_val

            def add_dt(m,dt):
                m.increment_value(dt*self.slow_factor_tracker.get_value())
            

            def process_part(part_index, coefs_freqs_dicts, part_length):
                ratio = part_length[part_index]/ sum(part_length)
                part_time = all_time * ratio

                # Calculate the slow factor based on the part lengths
                self.slow_factor = 1/part_time
                self.slow_factor_tracker = ValueTracker(self.slow_factor)

                # Initialize and add the vector clock
                self.vector_clock = ValueTracker(0.0).add_updater(add_dt)
                self.add(self.vector_clock)

                # Create and add vectors, circles, and drawn paths
                vectors = self.get_rotating_vectors(
                    coefficients=coefs_freqs_dicts[part_index]["coefs"],
                    freqs=coefs_freqs_dicts[part_index]["freqs"]
                )
                circles = self.get_circles(vectors)
                drawn_path = self.get_drawn_path(vectors)
                self.add(vectors, circles, drawn_path)

                # Wait based on the slow factor
                self.wait(1 / self.slow_factor + 1 / 15)

                # Clear updaters and remove objects
                for v in vectors:
                    v.clear_updaters()
                for c in circles:
                    c.clear_updaters()
                drawn_path.clear_updaters()
                self.remove(*vectors, *circles, self.vector_clock)

            # Example of how to use the function for each part
            for part_index in range(len(part_length)):
                process_part(part_index, coefs_freqs_dicts, part_length)


        svg_path = "new.svg"
        svg_path = "happynewyear.svg"
        svg_path = "dragon.svg"
        #svg_path = "chunhua.svg"
        #svg_path = "xuwen.svg"
        process_word(n_vectors=400, 
                     all_time=20, 
                     svg_path=svg_path, 
                     origin=complex(-1.2,-1.3),
                     scale_factor=22)
