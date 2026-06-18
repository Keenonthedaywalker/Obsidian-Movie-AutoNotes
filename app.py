from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        return f"Hello {name}, POST request received"
    return render_template('register.html')

@app.route('/login', methods=["POST"])
def login():
    print(1)

if __name__ == '__main__':
    app.run(debug=True)