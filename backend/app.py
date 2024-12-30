from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf_processor import PDFProcessor
import io

app = Flask(__name__)
CORS(app)
pdf_processor = PDFProcessor()

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'PDF işleme servisi çalışıyor'
    })

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return {'error': 'PDF dosyası bulunamadı'}, 400
    
    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return {'error': 'Dosya seçilmedi'}, 400
    
    if not pdf_file.filename.endswith('.pdf'):
        return {'error': 'Sadece PDF dosyaları kabul edilir'}, 400

    # Parametreleri al
    ink_spots = float(request.form.get('ink_spots', 0.999))  # Varsayılan 0.999 (daha az leke)
    blur_radius = float(request.form.get('blur_radius', 0.5))  # Varsayılan 0.5
    fade_level = float(request.form.get('fade_level', 1.15))  # Varsayılan 1.15

    try:
        # PDF'i işle
        pdf_bytes = pdf_file.read()
        processed_pdf = pdf_processor.process_pdf(pdf_bytes, ink_spots, blur_radius, fade_level)
        
        # İşlenmiş PDF'i gönder
        return send_file(
            io.BytesIO(processed_pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='processed.pdf'
        )
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 