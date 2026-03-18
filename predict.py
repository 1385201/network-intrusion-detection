# 网络入侵检测系统 - 完整闭环版（复试专用）
import pandas as pd#pandas 是 Python 的数据分析库，可以读取 CSV/Excel/SQL 等文件为 DataFrame 表格，并支持清洗、分析、导出全流程操作
import joblib#保存和加载 机器学习模型

# 新增：随机取数 + 写日志
import random #用于生成随机数
from datetime import datetime #获取时间函数



# 加载模型
print("✅ 加载训练好的模型...")
model = joblib.load("ids_model.pkl")
le1 = joblib.load("le1.pkl")
le2 = joblib.load("le2.pkl")
le3 = joblib.load("le3.pkl")
columns = joblib.load("columns.pkl")


# 读取流量数据
test = pd.read_csv("test-binary.txt", names=columns)#用columns给test变成DataFrame的格式表格，与训练集保持一致
test["f1"] = le1.transform(test["f1"])#将验证集里的第一列用刚刚训练集的规则映射一下，确保验证集和训练集的编码规则完全一致，但是测试集里不能有训练集里没出现过的转换规则
test["f2"] = le2.transform(test["f2"])
test["f3"] = le3.transform(test["f3"])
X_test = test.drop("label", axis=1)#删除标签列


# ===================== 闭环核心：模拟【实时新流量】输入 =====================


print("\n🔍 实时流量检测中...")
# 随机取一条流量（模拟真实环境：新来了一条流量）
random_index = random.randint(0, len(X_test)-1)#生成0~len(X_test)-1之间的随机数
sample = X_test.iloc[[random_index]]#取出这一行数据
result = model.predict(sample)[0]#模型预测这条流量是正常还是攻击，因为model.predect返回值是一个列表，取列表的第一个元素当然这里也是唯一一个元素


# 输出结果
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#获取时间
if result == 1:#表示预测结果是攻击流量
    detect_result = f"[{current_time}] 🚨 警告：检测到攻击流量！"
else:#0表示预测结果是整除的访问流量
    detect_result = f"[{current_time}] ✅ 正常：流量安全！"
print(detect_result)


# ===================== 闭环补充：保存检测日志（真实项目必备）=====================
with open("检测日志.txt", "a", encoding="utf-8") as f:#打开日志文件，追加模式写入，"a"表示追加模式（append），不覆盖旧内容encoding="utf-8"把中文 检测日志 转成二进制保存
    f.write(detect_result + "\n")#写入检测结果，换行
print("✅ 检测结果已保存到日志文件！")

