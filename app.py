from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import os
from bidi.algorithm import get_display
import arabic_reshaper

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_poster', methods=['POST'])
def generate_poster():
    language = request.form['language']
    name = request.form['name']
    image_path = create_poster(language, name)
    image_path = image_path.replace('static/', '')  # Remove the 'static/' prefix
    return redirect(url_for('poster', image_path=image_path))

@app.route('/poster/<image_path>')
def poster(image_path):
    return render_template('poster.html', image_path=image_path)

def create_poster(language, name):
    if language == 'ar':
        font_path = 'static/jrac-font-ar.ttf'
        poster_path = 'static/poster-ar.png'
        position = (500, 3900)  # Example position for Arabic

        # Reshape and reorder the Arabic text
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)
        name = bidi_text
    else:
        font_path = 'static/jrac-font-en.ttf'
        poster_path = 'static/poster-en.png'
        position = (2800, 3900)  # Example position for English

    # Load the poster and font
    image = Image.open(poster_path)
    font = ImageFont.truetype(font_path, size=150)

    # Draw the name on the poster
    draw = ImageDraw.Draw(image)
    draw.text(position, name, font=font, fill='#616264')

    # Save the edited poster
    output_path = f'static/{name}_{language}.png'
    image.save(output_path)  # Save the image

    return output_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)