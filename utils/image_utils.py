import cv2
import numpy as np
from PIL import Image
import io
import os

class ImageProcessor:
    @staticmethod
    def save_upload(image_bytes, filename):
        upload_dir = os.path.join(os.path.dirname(__file__), '../data/uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        return filepath

    @staticmethod
    def draw_predictions(image_path, predictions):
        # Cargar imagen
        image = cv2.imread(image_path)
        
        # Colores para diferentes tipos de lesiones
        colors = {
            'benign': (0, 255, 0),  # Verde
            'malignant': (0, 0, 255)  # Rojo
        }
        
        # Dibujar predicciones
        for pred in predictions:
            x = int(pred['location']['x'])
            y = int(pred['location']['y'])
            w = int(pred['location']['width'])
            h = int(pred['location']['height'])
            
            # Dibujar rectángulo
            cv2.rectangle(image, (x, y), (x + w, y + h), 
                         colors[pred['type']], 2)
            
            # Añadir texto
            label = f"{pred['type']} {pred['confidence']:.2f}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                       colors[pred['type']], 2)
            
            # Si hay máscara, dibujarla
            if pred.get('mask') is not None:
                mask = pred['mask'].astype(np.uint8) * 255
                image = cv2.addWeighted(image, 1, mask, 0.5, 0)
        
        return image