import svgpathtools
import numpy as np
import matplotlib.pyplot as plt
import os

def svg_path_num(path_to_file):
   path,_=svgpathtools.svg2paths(path_to_file)
   base_name = os.path.splitext(svg_path)[0]
   file_name = f"{base_name}_part_length.txt"
   with open(file_name, "w") as f:
       for i in range(len(path)):
           f.write(f"{i} {path[i].length()}\n")
       
   return len(path) 

"""
nvec: 
是傅里叶级数的系数的个数。因为傅里叶级数的展开项一般为无穷项。所以可以选一个合适的数目展开即可。
实际可视化的时候, 可以选择小于等于nvec的向量数目画图

npoint:
计算傅里叶级数时在轮廓上的采样点数, 以离散的方法计算积分
"""
def svg_to_coef(path_to_file,nvec=2001,npoint=10000,npath=0,conj=True,reverse=False):
    
    path,_=svgpathtools.svg2paths(path_to_file)
    """
    svg文件解析后的path是一个list
    即可能有多个path标签
    """
    path=path[npath]
    """
    需要特别注意这里的endpoint参数
    查看画出来的图，发现普遍没有闭合
    可能是这个原因

    将endpoint改为True,有显著变化

    在修改之前，画图有两个问题:
    1. 画出来的图不是闭合的
    2. 画图开始部分有点扭曲

    修改之后, 画图的开始部分变得光滑了
    但是画出来的图还是不闭合的

    需要进一步研究

    注: 提高points, 图像仍然无法闭合
    """
    points=np.linspace(0,1,npoint,endpoint=True)
    pathvals=np.zeros_like(points,dtype="complex")
    """
    svg文件第一个path的长度
    单位: 像素
    """
    pathlength=path.length()
    print(f"\033[92mpart {npath} length : {pathlength}\033[0m")

    if reverse:
        for i in range(len(points)):
            pathvals[i]=path.point(path.ilength(pathlength-pathlength*points[i]))
    else:
        for i in range(len(points)):
            """
            先获取路径物理长度的百分比所对应的长度
            然后再获取该百分比长度对应的百分比
            """
            pathvals[i]=path.point(path.ilength(pathlength*points[i]))
    
    """
    这里为何要取共轭?

    取共轭相当于将路径沿着x轴翻转
    图像形状不变

    经过测试后发现, 只有取共轭才能按照预期的顺序还出图像

    终于明白为何要取共轭了:
    svg文件的坐标系与数学中的坐标系不同
    svg文件中的y轴是向下的
    """
    if conj==True:
        pathvals=np.conj(pathvals).copy()
    
    coefs=list(range(nvec // 2, -nvec// 2, -1))
    coefs.sort(key=abs)
    # coefs: [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
    
    """
    np.trapz 是 NumPy 库中的一个函数, 用于通过梯形法则(Trapezoidal rule)来近似计算数值积分。
    这个方法在数值分析和计算数学中非常常见, 特别是在处理离散数据集或者无法获得解析解的积分问题时。

    梯形法则的原理：
    梯形法则基于将积分区间分割为许多小的梯形段，然后计算这些梯形的面积之和来近似整个积分的值。
    对于每个小梯形, 底边是x轴上的一小段区间, 而上边是函数值所形成的线段。通过计算所有这些梯形的面积
    并将它们加起来，可以得到整个函数在给定区间的积分近似值。
    """
    fourier_coef=np.zeros(nvec,dtype="complex")
    # points原本的范围是[0,1], 现在变为[0,2pi]
    # 可以理解为周期由1变为2pi
    # 可以作为np.trapz的x参数
    points*=2*np.pi
    for i in range(len(coefs)):
        coef=coefs[i]
        #exponent=np.exp(1j*coef*points)
        # 使用-1更加符合傅里叶级数的计算公式
        # 这里的points中包含了2pi
        # 需要和傅里叶级数的计算公式中的2pi进行区分
        # 傅里叶级数的计算公式中的2pif已经被抵消了，就是1
        # 而这里的points本质是时间t的采样
        exponent=np.exp(-1j*coef*points)

        fourier_coef[i]=np.trapz(np.multiply(exponent,pathvals),points)/(2*np.pi)
    # 从list变为array
    coefs=np.array(coefs)
    return coefs,fourier_coef

"""
画出来的图显得有点小
可以通过调整coef_scale来放大
"""
coef_scale = 1
def save_coef(coefs,fourier_coef,file_path):
    f=open(file_path,"w")
    for i in range(len(coefs)):
        f.write("{} {}".format(coefs[i],coef_scale*fourier_coef[i]))
        # 写完一个参数后换行
        if i<len(coefs)-1:
            f.write("\n")

if __name__ == "__main__":
    svg_path = "new.svg"
    svg_path = "happynewyear.svg"
    svg_path = "dragon.svg"
    svg_path = "chunhua.svg"
    svg_path = "xuwen.svg"
    base_name = os.path.splitext(svg_path)[0]  # Extracts 'Ale' from 'Ale.svg'

    num = svg_path_num(svg_path)
    for i in range(num):  # Adjust the range as needed
        coefs, fourier_coef = svg_to_coef(svg_path, npath=i, conj=True)
        output_filename = f"{base_name}_{i}.txt"  # Formats the output file name using the base name
        save_coef(coefs, fourier_coef, output_filename)

"""
执行这份文件后, 会生成两类文件
1.filename_part_length.txt 包含各个闭合path的长度
2.filename_i.txt 每一个闭合path的傅里叶系数
"""