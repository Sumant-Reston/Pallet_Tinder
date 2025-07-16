from flask import Flask, render_template_string, redirect, url_for, send_from_directory, request
import os
import threading
import shutil
import random

app = Flask(__name__)

IMAGE_FOLDER = 'Pallet_images'
GOOD_FOLDER = 'GoodPallet'
BAD_FOLDER = 'BadPallet'
UNKNOWN_FOLDER = 'UnknownPallet'
SORTED_FILE = 'sorted_images.txt'
lock = threading.Lock()

# Ensure folders exist
os.makedirs(GOOD_FOLDER, exist_ok=True)
os.makedirs(BAD_FOLDER, exist_ok=True)
os.makedirs(UNKNOWN_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def get_unsorted_images():
    if os.path.exists(SORTED_FILE):
        with open(SORTED_FILE, 'r') as f:
            sorted_images_live = set(line.strip() for line in f)
    else:
        sorted_images_live = set()

    all_images = [f for f in os.listdir(IMAGE_FOLDER)
                  if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"))]
    unsorted = [img for img in all_images if img not in sorted_images_live]
    random.shuffle(unsorted)
    return unsorted

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pallet Tinder</title>
    <style>
        body {
            background: #f2f2f2;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 1em;
            color: #333;
        }
        .card {
            position: relative;
            background: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            border-radius: 20px;
            overflow: hidden;
            width: 80vw;
            max-width: 600px;
            max-height: 70vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1em;
            transition: transform 0.3s ease-in-out;
        }
        .card img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        .buttons {
            display: flex;
            justify-content: center;
            gap: 2em;
            flex-wrap: wrap;
        }
        .btn {
            font-size: 2em;
            padding: 0.4em 1em;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .btn:hover {
            transform: scale(1.1);
        }
        .btn.good { background: #4CAF50; color: white; }
        .btn.bad { background: #F44336; color: white; }
        .btn.unknown { background: #FFC107; color: white; }
    </style>
</head>
<body>
    <h1>Pallet Tinder</h1>
    {% if image %}
        <div class="card">
            <img src="{{ url_for('image_file', filename=image) }}" alt="Image" />
        </div>
        <form method="post" action="/sort" id="sortForm">
            <input type="hidden" name="image" value="{{ image }}" id="imageInput" />
            <input type="hidden" name="result" value="" id="resultInput" />
            <div class="buttons">
                <button type="button" class="btn bad" onclick="submitSort('bad')">👎</button>
                <button type="button" class="btn unknown" onclick="submitSort('unknown')">❓</button>
                <button type="button" class="btn good" onclick="submitSort('good')">👍</button>
            </div>
        </form>
    {% else %}
        <h2>All images sorted!</h2>
    {% endif %}

    <script>
        function submitSort(value) {
            document.getElementById("resultInput").value = value;
            document.getElementById("sortForm").submit();
        }

        document.addEventListener("keydown", function(event) {
            if (event.key === "ArrowLeft") {
                submitSort("bad");
            } else if (event.key === "ArrowRight") {
                submitSort("good");
            } else if (event.key === "ArrowUp") {
                submitSort("unknown");
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    with lock:
        unsorted = get_unsorted_images()
        if not unsorted:
            return render_template_string(TEMPLATE, image=None)
        img_name = unsorted[0]
        return render_template_string(TEMPLATE, image=img_name)

@app.route('/images/<filename>')
def image_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/sort', methods=['POST'])
def sort():
    img_name = request.form.get('image')
    result = request.form.get('result')
    if not img_name or result not in ('good', 'bad', 'unknown'):
        return redirect(url_for('index'))

    src_path = os.path.join(IMAGE_FOLDER, img_name)
    dest_folder = {
        'good': GOOD_FOLDER,
        'bad': BAD_FOLDER,
        'unknown': UNKNOWN_FOLDER
    }.get(result)

    if dest_folder is None:
        return redirect(url_for('index'))

    dest_path = os.path.join(dest_folder, img_name)

    with lock:
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            with open(SORTED_FILE, 'a') as f:
                f.write(img_name + '\n')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
