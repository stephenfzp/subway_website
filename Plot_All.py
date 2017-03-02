# -- coding: UTF-8 --

'''
专门画图（直方图，散点图。。）
'''

from pylab import *
import mpld3
import os
mpl.rcParams['font.sans-serif'] = ['SimHei']   #AR PL UMing CN代表：宋体。SimHei代表：黑体   #漏了一个import
mpl.rcParams['axes.unicode_minus'] = False  #解决负号问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')


column_name = ['贯入度', '刀盘扭矩', '左上土仓压力', '刀盘转速', '推进速度', 'F2']


def Plot_scatter_oneX_Y(X11, X12, X21, X22, X31, X32, X41, X42, X51, X52, index=0):
    '传入五组参数绘图'
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 4)
    ax5 = fig.add_subplot(2, 3, 5)

    ax1.scatter(X11, X12)
    ax2.scatter(X21, X22)
    ax3.scatter(X31, X32)
    ax4.scatter(X41, X42)
    ax5.scatter(X51, X52)

    plt.title(column_name[index])
    plt.show()


def Plot_hist(X11, X21, X31, X41, X51, index=0):
    '根据传入的五组的数据画出分布直方图'
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 4)
    ax5 = fig.add_subplot(2, 3, 5)

    bins = 100
    ax1.hist(X11, bins=bins)
    ax2.hist(X21, bins=bins)
    ax3.hist(X31, bins=bins)
    ax4.hist(X41, bins=bins)
    ax5.hist(X51, bins=bins)

    plt.title(column_name[index])
    plt.show()

def Plot_ypre_ytrue(yPre, yTrue, file_name, file_num):
    '绘制真实值和预测值的对比曲线和散点图'
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(yPre, 'r', label='预测值')
    ax1.plot(yTrue, 'b', label='真实值')
    ax1.legend(loc='upper left')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.scatter(yTrue, yPre)
    ax2.set_xlabel('真实值')
    ax2.set_ylabel('预测值')

    plt.title('y的预测值和y的真实值对比')
    #plt.show()
    #mpld3.show()
    file_folder = file_name.rsplit('.', 1)[0]
    suppose_folder = 'uploads/'+file_folder
    save_filename = suppose_folder + '/' + file_folder + '_' +file_num +'.html'
    print 'save_filename:', save_filename
    if not os.path.exists(suppose_folder):
        os.mkdir(suppose_folder)
    mpld3.save_html(fig=fig, fileobj=str(save_filename))