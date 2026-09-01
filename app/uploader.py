# pegar o arquivo escolhido, fazer upload para o ambiente e gerar um dataframe
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever'


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(f'static/uploads/{filename}')
        return redirect(url_for('upload'))

    return render_template('index.html', form=form)


@app.route('/uploaded', methods=['GET'])
def upload():
    files = os.listdir('static/uploads/')
    return render_template('upload.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)
