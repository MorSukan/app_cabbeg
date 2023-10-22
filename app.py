from flask import Flask, render_template, request
import requests
import json
from roboflow import Roboflow
rf = Roboflow(api_key="hGegkoy8IkVOXti6XHB1")
project = rf.workspace().project("cabbage-low")
model = project.version(1).model
img = "test1.jpg"
# infer on a local image
text = model.predict(img, confidence=40, overlap=30).json()
print(len(text['predictions']))

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    count_cabbage = 0

    if request.method == 'POST':
        # Check if a file has been uploaded
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                # Send the uploaded file to Roboflow for prediction
                api_key = "hGegkoy8IkVOXti6XHB1"
                url = "https://detect.roboflow.com/cabbage-low/1?api_key=hGegkoy8IkVOXti6XHB1"
                files = {'file': ('image.jpg', uploaded_file.read())}
                headers = {'Authorization': f'Bearer {api_key}'}
                response = requests.post(url, headers=headers, files=files)
                data = response.json()
                
                # Get the predictions
                predictions = data['predictions']
                
                # Count the number of 'Cabbage' class
                for prediction in predictions:
                    if prediction['class'] == 'Cabbage':
                        count_cabbage += 1

    return render_template('index.html', count_cabbage=count_cabbage)

# นิยามฟังก์ชันที่มีอยู่แล้วสำหรับคำนวณราคา
def calculate_price():
    price_per_kg = float(request.form['price_per_kg'])
    num_cabbages = int(request.form['num_cabbages'])
    weight_per_cabbage = float(request.form['weight_per_cabbage'])

    total_weight = num_cabbages * weight_per_cabbage
    total_price = total_weight * price_per_kg

    return f"น้ำหนักทั้งหมด: {total_weight} กิโลกรัม\nราคาทั้งหมด: {total_price} บาท"

# เส้นทางสำหรับการคำนวณและแสดงผลลัพธ์
@app.route('/calculate', methods=['POST'])
def calculate():
    result = calculate_price()
    return result

# เส้นทางสำหรับแสดงฟอร์ม
@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)