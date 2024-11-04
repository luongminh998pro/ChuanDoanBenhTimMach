# Import các thư viện cần thiết
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, f1_score

# 1. Đọc dữ liệu từ file CSV
file_path = 'data\\cardio_train.csv'  # Đường dẫn tới file dữ liệu
df = pd.read_csv(file_path, sep=';')  

# Hiển thị vài dòng đầu tiên của dữ liệu
print(df.head())

# In ra danh sách các cột trong DataFrame
print("Danh sách các cột trong DataFrame:", df.columns)

# 2. Tiền xử lý dữ liệu
# Kiểm tra các giá trị null
print(df.isnull().sum())

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

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Thêm các tương tác giữa các biến
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_train_poly = poly.fit_transform(X_train_scaled)
X_test_poly = poly.transform(X_test_scaled)

# 4. Xây dựng mô hình Logistic Regression với regularization
model = LogisticRegression(random_state=42, solver='liblinear', penalty='l2', C=0.1, max_iter=300)  # Tăng max_iter

# 5. Tuning tham số
param_grid = {'C': np.logspace(-4, 4, 20)}
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='roc_auc')
grid_search.fit(X_train_poly, y_train)

# Lấy mô hình tốt nhất
best_model = grid_search.best_estimator_

# 6. Dự đoán trên tập test
y_pred = best_model.predict(X_test_poly)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, best_model.predict_proba(X_test_poly)[:, 1])
f1 = f1_score(y_test, y_pred)  # Tính F1 Score

# In các số liệu đánh giá mô hình
print(f"Accuracy: {accuracy}")
print(f"ROC AUC Score: {roc_auc}")
print(f"F1 Score: {f1}")  # In F1 Score

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

# Chuyển đổi report thành DataFrame để dễ xử lý
report_df = pd.DataFrame(report).transpose()

# Tạo biểu đồ cột cho precision, recall, f1-score của từng lớp
fig, ax = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

# Biểu đồ Precision
sns.barplot(x=report_df.index[:-3], y=report_df['precision'][:-3], ax=ax[0], palette='viridis')
ax[0].set_title('Precision')
ax[0].set_xticklabels(report_df.index[:-3], rotation=45)

# Biểu đồ Recall
sns.barplot(x=report_df.index[:-3], y=report_df['recall'][:-3], ax=ax[1], palette='viridis')
ax[1].set_title('Recall')
ax[1].set_xticklabels(report_df.index[:-3], rotation=45)

# Biểu đồ F1-Score
sns.barplot(x=report_df.index[:-3], y=report_df['f1-score'][:-3], ax=ax[2], palette='viridis')
ax[2].set_title('F1-Score')
ax[2].set_xticklabels(report_df.index[:-3], rotation=45)

# Thiết lập tiêu đề chung và hiển thị biểu đồ
plt.suptitle('Classification Report Metrics by Class')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
