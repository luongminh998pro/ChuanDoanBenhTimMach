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

# Hiển thị 5 dòng đầu tiên của dữ liệu
print(df.head(5))

# Xem thông tin của dataframe
df.info()

# Đếm số lượng mẫu trong cột cardio
cardio_counts = df['cardio'].value_counts()

# In ra số lượng mẫu
print("Số lượng mẫu với giá trị 0 (không có bệnh tim mạch):", cardio_counts.get(0, 0))
print("Số lượng mẫu với giá trị 1 (có bệnh tim mạch):", cardio_counts.get(1, 0))

# Vẽ biểu đồ cột cho số lượng mẫu trong cột cardio
plt.figure(figsize=(8, 5))
sns.barplot(x=cardio_counts.index, y=cardio_counts.values, palette='viridis')
plt.title('Số lượng mẫu trong cột cardio')
plt.xlabel('Cardio (0: không có bệnh, 1: có bệnh)')
plt.ylabel('Số lượng mẫu')
plt.xticks(ticks=[0, 1], labels=['Không có bệnh', 'Có bệnh'], rotation=0)
plt.show()

# 2. Tiền xử lý dữ liệu
# Kiểm tra các giá trị null
print(df.isnull().sum())

# Nếu có giá trị null thì xử lý, ở đây giả sử không có null
# Chuyển đổi cột 'gender' (1 là nam, 2 là nữ)
if 'gender' in df.columns:
    df['gender'] = df['gender'].map({1: 0, 2: 1})  # 0: nam, 1: nữ
else:
    print("Cột 'gender' không có trong DataFrame.")

# Tách dữ liệu thành biến độc lập và phụ thuộc
X = df.drop(columns=['cardio', 'id'])  # Loại bỏ cột 'cardio' và 'id'
y = df['cardio']  # Nhãn mục tiêu (bệnh tim mạch)

# 3. Phân chia tập dữ liệu thành train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu (đối với Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Xây dựng mô hình dự đoán - sử dụng Logistic Regression
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# 5. Dự đoán trên tập test
y_pred = model.predict(X_test_scaled)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:, 1])
print(f"Accuracy: {accuracy}")
print(f"ROC AUC Score: {roc_auc}")

# In ra báo cáo chi tiết
report = classification_report(y_test, y_pred, output_dict=True)
print(classification_report(y_test, y_pred))

# In riêng recall và precision cho từng lớp
recall_0 = report['0']['recall']  # Recall cho lớp 0
recall_1 = report['1']['recall']  # Recall cho lớp 1
precision_0 = report['0']['precision']  # Precision cho lớp 0
precision_1 = report['1']['precision']  # Precision cho lớp 1

print(f"Recall cho lớp 0: {recall_0}")
print(f"Recall cho lớp 1: {recall_1}")
print(f"Precision cho lớp 0: {precision_0}")
print(f"Precision cho lớp 1: {precision_1}")

# Ma trận nhầm lẫn
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Vẽ biểu đồ mắc bệnh theo giới tính
plt.figure(figsize=(10, 6))
gender_cardio_counts = df.groupby(['gender', 'cardio']).size().unstack()
gender_cardio_counts.columns = ['Không có bệnh', 'Có bệnh']
gender_cardio_counts.plot(kind='bar', stacked=False, color=['lightblue', 'salmon'])
plt.title('Mắc bệnh tim mạch theo giới tính')
plt.xlabel('Giới tính (0: Nam, 1: Nữ)')
plt.ylabel('Số lượng mẫu')
plt.xticks(ticks=[0, 1], labels=['Nam', 'Nữ'], rotation=0)
plt.legend(title='Cardio')
plt.show()

# Vẽ biểu đồ histogram cho cột tuổi
plt.figure(figsize=(10, 6))
df['age_years'] = df['age'] / 365  # Chia cột 'age' cho 365 để có tuổi
sns.histplot(df['age_years'], bins=30, kde=True, color='purple')
plt.title('Phân phối tuổi (tính bằng năm)')
plt.xlabel('Tuổi (năm)')
plt.ylabel('Tần suất')
plt.show()

# Vẽ heatmap cho ma trận tương quan
plt.figure(figsize=(12, 8))
correlation_matrix = df.corr()  # Tính toán ma trận tương quan
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Ma trận tương quan giữa các đặc trưng')
plt.show()
