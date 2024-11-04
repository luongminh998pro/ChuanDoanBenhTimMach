from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

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
    'active': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],     # Tất cả đều hoạt động thể chất
    'cardio': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]      # 0: Không mắc bệnh
}

# Chuyển đổi dữ liệu thành DataFrame
df_mac_benh = pd.DataFrame(data_mac_benh)
df_khong_mac_benh = pd.DataFrame(data_khong_mac_benh)

def match_department(age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active):
    # Kiểm tra trong DataFrame người mắc bệnh
    for index, row in df_mac_benh.iterrows():
        if (row['age'] == age and
            row['gender'] == gender and
            row['height'] == height and
            row['weight'] == weight and
            row['ap_hi'] == ap_hi and
            row['ap_lo'] == ap_lo and
            row['cholesterol'] == cholesterol and
            row['gluc'] == gluc and
            row['smoke'] == smoke and
            row['alco'] == alco and
            row['active'] == active):
            return "Mắc bệnh tim mạch"

    # Kiểm tra trong DataFrame người không mắc bệnh
    for index, row in df_khong_mac_benh.iterrows():
        if (row['age'] == age and
            row['gender'] == gender and
            row['height'] == height and
            row['weight'] == weight and
            row['ap_hi'] == ap_hi and
            row['ap_lo'] == ap_lo and
            row['cholesterol'] == cholesterol and
            row['gluc'] == gluc and
            row['smoke'] == smoke and
            row['alco'] == alco and
            row['active'] == active):
            return "Không mắc bệnh tim mạch"

    return "Không mắc bệnh tim mạch"

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ""
    if request.method == 'POST':
        try:
            # Nhận dữ liệu từ form
            age = int(request.form.get('age', 0))
            gender = int(request.form.get('gender', '0'))  # Đảm bảo giá trị là số
            height = float(request.form.get('height', 0))
            weight = float(request.form.get('weight', 0))
            ap_hi = int(request.form.get('ap_hi', 0))
            ap_lo = int(request.form.get('ap_lo', 0))
            cholesterol = int(request.form.get('cholesterol', 1))
            gluc = int(request.form.get('gluc', 1))
            smoke = int(request.form.get('smoke', '0'))
            alco = int(request.form.get('alco', '0'))
            active = int(request.form.get('active', '0'))

            # Dự đoán bệnh tim mạch
            prediction = match_department(age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active)
        except ValueError:
            prediction = "Dữ liệu nhập không hợp lệ!"

    return render_template('index.html', prediction=prediction)

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/LogisticRegression')
def xgboost():
    # Hiển thị giải thích thuật toán XGBoost
    return render_template('LogisticRegression.html')

@app.route('/about')
def about():
    # Hiển thị thông tin tác giả
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
