# Crear un script de prueba: test_model.py
from models.model_handler import MammoVisionModel
import os
from PIL import Image
import cv2

def test_model():
    try:
        model = MammoVisionModel()
        
        # Directorio de imágenes de prueba
        test_dir = "test_images"
        
        # Probar todas las imágenes en el directorio
        for image_file in os.listdir(test_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                image_path = os.path.join(test_dir, image_file)
                print(f"\nProcesando imagen: {image_file}")
                
                # Leer y mostrar información de la imagen
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    print(f"Dimensiones: {img.shape}")
                    print(f"Rango de valores: [{img.min()}, {img.max()}]")
                    print(f"Tipo de datos: {img.dtype}")
                
                # Realizar predicción
                predictions = model.predict(image_path)
                print(f"Número de detecciones: {len(predictions)}")
                
                # Mostrar detalles de cada detección
                for i, pred in enumerate(predictions, 1):
                    print(f"\nDetección {i}:")
                    print(f"Tipo: {pred['type']}")
                    print(f"Confianza: {pred['confidence']:.2f}")
                    print(f"Ubicación: {pred['location']}")
                
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")

if __name__ == "__main__":
    test_model()