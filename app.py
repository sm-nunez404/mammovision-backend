import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.model_handler import MammoVisionModel

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": ["https://mammovision-frontend.vercel.app", "http://localhost:3000"]}})

# Obtén la ruta del modelo
MODEL_PATH = os.environ.get('MODEL_PATH', '/home/mauri/Documentos/ai-projects/mammovision/mammovision-backend/models/mammovision.pt')
# Verifica si el archivo existe
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"No se encontró el modelo en: {MODEL_PATH}")

model = MammoVisionModel(MODEL_PATH)

# Cargar las variables de entorno
#UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Configurar la carpeta de uploads
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Asegurar permisos de escritura
    os.chmod(UPLOAD_FOLDER, 0o755)

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "MammoVision API is running"})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Guardar el archivo original
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            
            # Realizar predicción
            predictions, processed_filename = model.predict(filename)
            
            # Construir URLs completas
            base_url = request.host_url.rstrip('/') + '/uploads/'
            image_url = base_url + os.path.basename(filename)
            processed_image_url = base_url + 'processed_' + os.path.basename(filename)
            
            return jsonify({
                'status': 'success',
                'imageUrl': image_url,
                'processedImageUrl': processed_image_url,
                'predictions': predictions
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500





# Agregar ruta para servir las imágenes
@app.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/predict', methods=['OPTIONS'])
def options():
    return '', 200  # Respuesta vacía para OPTIONS

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # O especifica tu origen
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)