from flask import Flask, render_template, send_from_directory, send_file, request
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_from_directory('static/produto', 'downize.exe', as_attachment=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img', 'favicon.png', mimetype='image/png')

def gerar_qrcode_pix(valor='10.00', descricao='Apoio ao Downize'):
    pix_key = "8300bbc5-a1bf-4b85-b48a-0fed9f47bc09"
    payload = f"00020126360014BR.GOV.BCB.PIX0114{pix_key}5204000053039865802BR5925Downize Projeto6009Sao Paulo62110506{descricao[:25]}540{valor}6304"
    img = qrcode.make(payload)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

@app.route('/pix-qrcode')
def pix_qrcode():
    valor = request.args.get('valor', '10.00')
    descricao = request.args.get('desc', 'Apoio ao Downize')
    buf = gerar_qrcode_pix(valor, descricao)
    return send_file(buf, mimetype='image/png')

@app.route('/pix-qrcode-download')
def pix_qrcode_download():
    valor = request.args.get('valor', '10.00')
    descricao = request.args.get('desc', 'Apoio ao Downize')
    buf = gerar_qrcode_pix(valor, descricao)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode-pix.png')

if __name__ == '__main__':
    app.run(debug=True)
