from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Crée les dossiers si nécessaire
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        template = request.files['template']
        font_file = request.files['font']
        text = request.form['text']
        font_size = int(request.form['font_size'])
        position = request.form['position'].split(',')
        position = (int(position[0]), int(position[1]))
        color = request.form['color']

        # Sauvegarder les fichiers uploadés
        template_path = os.path.join(app.config['UPLOAD_FOLDER'], template.filename)
        font_path = os.path.join(app.config['UPLOAD_FOLDER'], font_file.filename)
        template.save(template_path)
        font_file.save(font_path)

        # Générer l'image
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)
        draw.text(position, text, font=font, fill=color)

        # Sauvegarder l'image générée
        output_filename = 'output_image.png'
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        image.save(output_path)

        # Retourner le chemin de l'image pour prévisualisation
        return jsonify({"image_url": url_for('static', filename=f'output/{output_filename}')})

    return render_template('index.html')

@app.route('/static/output/<filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
