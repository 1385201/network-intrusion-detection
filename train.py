# 网络入侵检测系统 - 训练代码（最终修复版）
import pandas as pd#pandas 是 Python 的数据分析库，可以读取 CSV/Excel/SQL 等文件为 DataFrame 表格，并支持清洗、分析、导出全流程操作
import matplotlib.pyplot as plt#Matplotlib 的 pyplot 模块，用于绘制图表
from sklearn.preprocessing import LabelEncoder#需要使用编码器给非数字类别转换成数字类别
from sklearn.ensemble import RandomForestClassifier#随机森林分类算法
from sklearn.metrics import accuracy_score#计算预测准确率的函数
import joblib#保存和加载 机器学习模型

# 中文显示
plt.rcParams["font.family"] = ["SimHei"]#为了解决中文乱码的问题，因为缺少其默认的中文字体类型，所以我命令「画图工具 matplotlib」，把所有图表的默认字体，全局统一设置为「黑体」


# 特征列名
columns = [f"f{i}" for i in range(41)] + ["label"]#用columns列表来为41个特征和1个标签取名字


# 读取数据
#因为标准数据集NSL-KDD是csv格式的
train = pd.read_csv("train-binary.txt", names=columns)#这行代码把一个没有表头的文本文件读成带列名的表格，准备用于机器学习（41个特征 + 1个标签）。train保存了DataFrame格式表格
test = pd.read_csv("test-binary.txt", names=columns)#这行代码把一个没有表头的文本文件读成带列名的表格，准备用于机器学习（41个特征 + 1个标签）。test保存了DataFrame格式表格


# 3个独立特征，分别用3个独立编码器
le1 = LabelEncoder()
le2 = LabelEncoder()
le3 = LabelEncoder()


# 训练集编码
train["f1"] = le1.fit_transform(train["f1"])#le1对训练集的 f1 列进行标签编码，将文字类别转换为数字，并覆盖保存回原列
train["f2"] = le2.fit_transform(train["f2"])
train["f3"] = le3.fit_transform(train["f3"])


# 测试集编码
test["f1"] = le1.transform(test["f1"])#将验证集里的第一列用刚刚训练集的规则映射一下，确保验证集和训练集的编码规则完全一致，但是测试集里不能有训练集里没出现过的转换规则
test["f2"] = le2.transform(test["f2"])
test["f3"] = le3.transform(test["f3"])


# 划分数据
X_train = train.drop("label", axis=1)#删除 label 列，剩下的作为训练特征#axis=0 表示删除行 ，axis=1 表示删除列 
y_train = train["label"]#只取 label 列，作为训练标签

X_test = test.drop("label", axis=1)#删除 label 得测试特征
y_test = test["label"]#只取 label 列，作为测试标签


# 训练模型
model = RandomForestClassifier(random_state=0)#创建一个随机森林分类器模型，固定随机数种子，让结果可复现。
model.fit(X_train, y_train)#训练模型，让它学习特征和标签的关系

# 评估
y_pred = model.predict(X_test)#用模型预测测试集的结果，类似于上面的y_train，只不过上面的y_train是真的而这里的y_pred是用刚刚训练的模型预测的
acc = accuracy_score(y_test, y_pred)#对比预测结果和真实标签，计算准确率，计算分类准确率 = 预测对的个数 / 总个数


# 输出
print("="*50)#打印 50 个等号 ==================================================
print(f"✅ 模型训练完成！准确率：{acc:.2%}")#f-string（格式化字符串）
print("="*50)#打印 50 个等号 ==================================================

# 保存模型 + 3个编码器 + 列名
joblib.dump(model, "ids_model.pkl")
joblib.dump(le1, "le1.pkl")
joblib.dump(le2, "le2.pkl")
joblib.dump(le3, "le3.pkl")
joblib.dump(columns, "columns.pkl")

print("✅ 模型已保存！")

# 可视化图表
plt.figure(figsize=(8, 4))#创建画布，长8英寸宽4英寸
test["label"].value_counts().plot(kind="bar", color=["#1f77b4", "#ff4b5c"])#同时统计所有不同值的个数，用柱状图，第一个是蓝色，第二个是红色
plt.title("网络流量类型分布（0=正常 1=攻击）")#设置图表标题
plt.show()#显示图表

