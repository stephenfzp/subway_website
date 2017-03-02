# -- coding: UTF-8 --

'''
计算拟合参数
'''

from sklearn import linear_model
import pandas as pd
import numpy as np
import Plot_All

class calculate():
    def __init__(self, file_name):
        self.filename = file_name  #单纯的文件名
        #self.filefolder = 'uploads/' + self.filename.rsplit('.', 1)[0] #加上文件夹后的相对路径

    def open_file(self):
        '打开文件并读取数据'
        data1 = pd.read_csv('uploads/'+self.filename) # 未过滤噪点的原始数据
        return data1

    def Divide_data(self):
        '传入从文件中读取的数据按照三组参数分为三组数据输出'
        Data = self.open_file()
        import Weka_config_theta
        X1 = pd.DataFrame(Data, columns=Weka_config_theta.column_name1)
        X2 = pd.DataFrame(Data, columns=Weka_config_theta.column_name2)
        X3 = pd.DataFrame(Data, columns=Weka_config_theta.column_name3)
        return X1, X2, X3

    def least_squares(self, xMat, yMat):
        '普通线性回归'
        model1 = linear_model.LinearRegression()
        model1.fit(xMat, yMat)  # y不能为matrix类型
        # 拟合的回归系数
        Coefficients = []
        Coefficients.extend(model1.coef_);Coefficients.append(model1.intercept_)
        #print 'Coefficients: ', Coefficients  # 拟合参数 最后一个数值是截距
        # 预测值
        yPre = model1.predict(xMat)
        # 计算预测值和真实值的相关系数
        #print np.corrcoef(yPre, yMat)[0][1]
        #print model1.score(xMat, yMat)

        analysis_result = [];analysis_result.append(Coefficients);analysis_result.append(np.corrcoef(yPre, yMat)[0][1])
        return analysis_result

    def Ridgee(self, X_includeY):
        '岭回归'
        X = X_includeY.copy()
        yMat = X['F2'];del X['F2'];del X['环号']  # 取出数据集中‘F2’一列
        xMat = X

        model = linear_model.Ridge()
        model.fit(xMat, yMat)
        Coefficients = []
        Coefficients.extend(model.coef_);Coefficients.append(model.intercept_)
        yPre = model.predict(xMat)

        analysis_result = [];analysis_result.append(Coefficients);analysis_result.append(np.corrcoef(yPre, yMat)[0][1])
        return analysis_result

    def Lasso(self, X_includeY, num):
        '套索 剪刀'
        #假设 X 为依据分好类的数据，但是包括'F2'
        # import copy
        # X = copy.deepcopy(X_includeY)
        X = X_includeY.copy()
        yMat = X['F2'];del X['F2'];del X['环号'] # 取出数据集中‘F2’一列
        xMat = X
        model = linear_model.Lasso()
        model.fit(xMat, yMat)

        Coefficients = [];Coefficients.extend(model.coef_);Coefficients.append(model.intercept_) #参数和截距

        yPre = model.predict(xMat)

        # #绘图并保存
        Plot_All.Plot_ypre_ytrue(yPre, yMat, self.filename, num)  #传入文件名和文件夹的路径

        analysis_result = []
        analysis_result.append(Coefficients);analysis_result.append(np.corrcoef(yPre, yMat)[0][1]) #拟合的参数、预测值和真实值的相关系数
        return analysis_result

# # #测试
# temp = calculate('Num1.csv')
# x1, x2, x3 = temp.Divide_data()
# result = []
# result.append(temp.Lasso(x1, num='1'));result.append(temp.Lasso(x2, num='2'));result.append(temp.Lasso(x3, num='3'))
# print temp.Lasso(x3, num='3')








