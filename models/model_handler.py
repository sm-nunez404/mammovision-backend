from ultralytics import YOLO
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
import io
import cv2

class MammoVisionModel:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Usando dispositivo: {self.device}")
        
        self.model_path = model_path
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"No se encontró el modelo en: {self.model_path}")
        
        try:
            self.model = self.load_model()
            print("Modelo cargado exitosamente")
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            raise

    def load_model(self):
        try:
            # Cargar el modelo usando YOLO
            model = YOLO(self.model_path)
            return model
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            raise

    def predict(self, image_path):
        try:
            # Realizar predicción con segmentación
            results = self.model(image_path, task='segment')
            
            # Obtener la imagen original
            original_image = cv2.imread(image_path)
            H, W = original_image.shape[:2]
            
            # Crear una copia para las anotaciones
            annotated_image = original_image.copy()
            
            # Procesar resultados
            predictions = []
            for result in results:
                if result.masks is not None:  # Verificar si hay máscaras de segmentación
                    for i, (mask, box) in enumerate(zip(result.masks, result.boxes)):
                        # Obtener la máscara de segmentación
                        segment = mask.data[0].cpu().numpy()
                        segment = cv2.resize(segment, (W, H))
                        
                        # Crear máscara binaria
                        binary_mask = (segment > 0.5).astype(np.uint8)
                        
                        # Aplicar desenfoque gaussiano para suavizar los bordes
                        binary_mask = cv2.GaussianBlur(binary_mask, (5, 5), 0)
                        
                        # Obtener información de la detección
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = result.names[cls]
                        
                        # Definir color según el tipo de lesión
                        color = [0, 255, 0] if class_name.lower() == 'benigno' else [0, 0, 255]  # Verde para benigno, Rojo para maligno
                        
                        # Crear overlay con el color correspondiente
                        overlay = np.zeros_like(original_image)
                        overlay[binary_mask > 0] = color  # Usar el color según el tipo
                        
                        # Combinar con la imagen original
                        alpha = 0.3  # Ajustar transparencia
                        cv2.addWeighted(overlay, alpha, annotated_image, 1.0, 0, annotated_image)
                        
                        # Calcular el centro de masa de la segmentación
                        moments = cv2.moments(binary_mask)
                        if moments["m00"] != 0:
                            cx = int(moments["m10"] / moments["m00"])
                            cy = int(moments["m01"] / moments["m00"])
                        else:
                            cx, cy = W//2, H//2
                        
                        # Aumentar el tamaño del texto y mejorar visibilidad
                        label = f"{class_name.upper()} {(conf*100):.1f}%"
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 1.2  # Aumentado de 0.6 a 1.2
                        thickness = 3     # Aumentado de 2 a 3
                        
                        # Obtener tamaño del texto
                        (text_width, text_height), baseline = cv2.getTextSize(
                            label, font, font_scale, thickness
                        )
                        
                        # Aumentar el padding para un fondo más grande
                        padding = 10  # Aumentado de 5 a 10
                        
                        # Agregar borde blanco al texto para mejor legibilidad
                        # cv2.putText(
                        #     annotated_image,
                        #     label,
                        #     (cx - text_width//2, cy - padding),
                        #     font,
                        #     font_scale,
                        #     (0, 0, 0),  # Borde negro
                        #     thickness + 2
                        # )
                        
                        # Texto principal
                        # cv2.putText(
                        #     annotated_image,
                        #     label,
                        #     (cx - text_width//2, cy - padding),
                        #     font,
                        #     font_scale,
                        #     (255, 255, 255),  # Texto blanco
                        #     thickness
                        # )
                        
                        # Obtener las dimensiones de la región segmentada
                        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        if contours:
                            x, y, w, h = cv2.boundingRect(contours[0])
                        else:
                            x, y = cx, cy
                            w, h = 100, 100  # valores por defecto si no se encuentra contorno
                        
                        # Agregar a las predicciones
                        predictions.append({
                            'type': class_name,
                            'confidence': conf,
                            'location': {
                                'x': float(x),
                                'y': float(y),
                                'width': float(w),
                                'height': float(h)
                            }
                        })
            
            # Guardar imagen procesada
            processed_filename = 'processed_' + os.path.basename(image_path)
            processed_path = os.path.join(
                os.path.dirname(os.path.dirname(image_path)), 
                'data', 
                'uploads',
                processed_filename
            )
            cv2.imwrite(processed_path, annotated_image)
            
            return predictions, processed_filename
            
        except Exception as e:
            print(f"Error en la predicción: {str(e)}")
            raise