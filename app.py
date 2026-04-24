from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Flask sẽ tự động tìm index.html trong thư mục templates
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)