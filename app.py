import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models.model_handler import MammoVisionModel

app = Flask(__name__)
CORS(app)

# Cargar las variables de entorno
MODEL_PATH = os.getenv('MODEL_PATH')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

# Configurar la carpeta de uploads
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar el modelo
try:
    model = MammoVisionModel(MODEL_PATH)
    print("Modelo cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo: {str(e)}")
    raise

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
            image_url = base_url + file.filename
            processed_image_url = base_url + processed_filename
            
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)