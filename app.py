from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit the size of uploads to 16MB

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('website.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['pdf']
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('home'))

@app.route('/validate', methods=['GET'])
def validate():
    return "True"  # Simply returns True for now, expand as needed.

if __name__ == '__main__':
    app.run()
