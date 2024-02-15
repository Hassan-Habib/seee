import random
from flask import Flask, request, render_template, jsonify
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)


def generate(number):
    vari = ''
    tex = '0100000000xxxxxx1725073110ve090a#2127608752238'

    # Replace 'xxxxxx' with the number provided by the client
    tex = tex.replace('xxxxxx', str(number))

    # Find the index of the '#' symbol
    hash_index = tex.find('#')
    if hash_index != -1:
        vari += tex[:hash_index + 1]  # Keep everything before the '#'
        vari += ''.join([str(random.randint(0, 9)) for _ in range(13)])  # Generate 13 random digits after the '#'

    print(vari)
    return vari


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_click', methods=['POST', 'GET'])
def handle_click():
    input_text = request.form['inputField']
    generated_text = generate(input_text)

    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(generated_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a BytesIO object
    qr_img_bytes_io = BytesIO()
    qr_img.save(qr_img_bytes_io)  # Remove format='PNG' argument
    qr_img_bytes_io.seek(0)

    # Convert BytesIO object to base64 encoded string
    qr_img_base64 = base64.b64encode(qr_img_bytes_io.getvalue()).decode('utf-8')
    qr_img_base64_encoded = "data:image/png;base64," + qr_img_base64

    return jsonify({'generated_text': generated_text, 'qr_code_image': qr_img_base64_encoded})


if __name__ == '__main__':
    app.run(debug=True)
