from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dữ liệu mẫu
data_mac_benh = {
    'age': [62, 65, 70, 58, 75, 67, 80, 64, 73, 68, 72, 76, 74, 61, 78, 69, 66, 74, 77, 63, 71, 79, 66, 60, 72],
    'gender': [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],  # 0: Nam, 1: Nữ
    'height': [168, 170, 165, 160, 175, 180, 155, 165, 172, 178, 160, 167, 170, 175, 162, 165, 177, 162, 170, 169, 165, 173, 175, 168, 171],
    'weight': [70, 85, 90, 80, 82, 88, 72, 80, 76, 85, 82, 77, 90, 81, 79, 88, 83, 75, 91, 86, 87, 89, 74, 81, 78],  # Cân nặng là số tròn
    'ap_hi': [150, 160, 145, 155, 170, 165, 160, 155, 158, 162, 175, 145, 160, 150, 170, 165, 172, 160, 157, 163, 174, 161, 159, 164, 158],  # Huyết áp tâm thu cao
    'ap_lo': [90, 95, 85, 92, 100, 98, 94, 90, 88, 96, 102, 87, 93, 91, 99, 95, 88, 90, 92, 94, 97, 91, 89, 92, 93],    # Huyết áp tâm trương cao
    'cholesterol': [2, 3, 3, 2, 3, 2, 3, 1, 2, 3, 2, 3, 3, 2, 3, 3, 2, 1, 2, 2, 1, 3, 2, 2, 3], # Cholesterol thay đổi
    'gluc': [1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 3, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 2, 1, 1, 1],       # Glucose thay đổi
    'smoke': [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1],      # Một số người hút thuốc
    'alco': [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],       # Một số người uống rượu
    'active': [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],     # Hoạt động thể chất khác nhau
    'cardio': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]      # 1: Mắc bệnh
}

data_khong_mac_benh = {
    'age': [50, 45, 30, 40, 35, 55, 65, 30, 25, 28, 34, 48, 52, 60, 53, 45, 33, 38, 29, 31, 41, 49, 55, 46, 43],
    'gender': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],  # 0: Nam, 1: Nữ
    'height': [160, 175, 180, 165, 172, 158, 174, 168, 159, 177, 163, 170, 165, 172, 169, 160, 174, 168, 175, 171, 169, 165, 162, 166, 173],
    'weight': [65, 70, 60, 65, 70, 75, 80, 63, 55, 58, 64, 66, 67, 69, 71, 72, 73, 68, 62, 65, 70, 74, 78, 72, 76],  # Cân nặng là số tròn
    'ap_hi': [120, 130, 110, 115, 125, 130, 135, 112, 108, 118, 124, 119, 123, 126, 132, 120, 118, 121, 125, 130, 132, 120, 121, 126, 128],  # Huyết áp tâm thu bình thường
    'ap_lo': [80, 85, 75, 78, 80, 82, 85, 76, 74, 77, 79, 81, 80, 78, 81, 80, 82, 81, 80, 79, 78, 82, 83, 80, 79],    # Huyết áp tâm trương bình thường
    'cholesterol': [1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1], # Cholesterol bình thường
    'gluc': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],       # Glucose bình thường
    'smoke': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      # Không hút thuốc
    'alco': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       # Không uống rượu
    'active': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],     # Hoạt động thể chất cao
    'cardio': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]      # 0: Không mắc bệnh
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    ap_hi = int(request.form['ap_hi'])
    ap_lo = int(request.form['ap_lo'])
    cholesterol = int(request.form['cholesterol'])
    gluc = int(request.form['gluc'])
    smoke = int(request.form['smoke'])
    alco = int(request.form['alco'])
    active = int(request.form['active'])
    
    # Giả lập kết quả dự đoán đơn giản
    result = 'Có khả năng mắc bệnh tim mạch' if cholesterol == 3 or gluc == 3 or ap_hi >= 140 or ap_lo >= 90 else 'Không có khả năng mắc bệnh tim mạch'
    
    return render_template('result.html', result=result)

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/LogisticRegression')
def xgboost():
    # Hiển thị giải thích thuật toán Logistic Regression
    return render_template('LogisticRegression.html')

@app.route('/about')
def about():
    # Hiển thị thông tin tác giả
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
