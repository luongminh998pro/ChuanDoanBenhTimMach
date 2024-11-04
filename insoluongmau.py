# Import các thư viện cần thiết
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

# 1. Đọc dữ liệu từ file CSV
file_path = 'data\\cardio_train.csv'  # Đường dẫn tới file dữ liệu
df = pd.read_csv(file_path, sep=';')  

# Tiền xử lý dữ liệu
df['gender'] = df['gender'].map({1: 0, 2: 1})  # 0: nam, 1: nữ
X = df.drop(columns=['cardio', 'id'])
y = df['cardio']

# Phân chia tập dữ liệu thành train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Xây dựng mô hình dự đoán
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Tính số lượng mẫu
total_samples = len(df)
cardio_counts = df['cardio'].value_counts()
samples_with_0 = cardio_counts.get(0, 0)  # Số lượng mẫu không có bệnh tim mạch (0)
samples_with_1 = cardio_counts.get(1, 0)  # Số lượng mẫu có bệnh tim mạch (1)

# In ra số liệu
print(f"Tổng số lượng mẫu: {total_samples}")
print(f"Số lượng mẫu không có bệnh tim mạch (0): {samples_with_0}")
print(f"Số lượng mẫu có bệnh tim mạch (1): {samples_with_1}")

# Thêm các đoạn mã khác ở đây nếu cần
