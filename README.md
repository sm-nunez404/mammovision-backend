# MammoVision: Detección Inteligente de Cáncer de Mama mediante Deep Learning

<div align="center">
  <img src="assets/logo.png" alt="MammoVision Logo" width="200"/>
  <br>
  <p>
    <a href="#descripción">Descripción</a> •
    <a href="#características">Características</a> •
    <a href="#instalación">Instalación</a> •
    <a href="#uso">Uso</a> •
    <a href="#tecnologías">Tecnologías</a> •
    <a href="#resultados">Resultados</a>
  </p>
</div>

## 📋 Descripción

MammoVision es un sistema de detección inteligente de cáncer de mama que utiliza técnicas avanzadas de Deep Learning, específicamente la arquitectura YOLOv11-seg, para identificar y segmentar lesiones mamarias en imágenes mamográficas. El sistema es capaz de clasificar las lesiones como benignas o malignas con alta precisión, proporcionando una herramienta valiosa para el diagnóstico temprano.

### 🎯 Objetivos

- Detección y segmentación precisa de lesiones mamarias
- Clasificación entre lesiones benignas y malignas
- Reducción de falsos positivos y negativos
- Apoyo en el diagnóstico médico temprano

## ✨ Características

- **Detección en Tiempo Real**: Análisis rápido y eficiente de imágenes mamográficas
- **Segmentación Precisa**: Delimitación exacta de áreas sospechosas
- **Interfaz Web Intuitiva**: Fácil de usar para profesionales médicos
- **Resultados Detallados**: Información completa sobre las detecciones
- **Soporte Multi-formato**: Compatible con DICOM, PNG, JPEG y TIFF

## 🚀 Instalación

### Prerrequisitos



```bash
Python 3.10 o superior
CUDA 12.6 (para GPU)
Node.js 18.0 o superior
```



### Configuración del Entorno

1. Clonar el repositorio:




```bash
git clone https://github.com/sm-nunez404/mammovision.git
cd mammovision
```

2. Instalar dependencias del backend:


```bash
cd backend
python -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```



3. Instalar dependencias del frontend:



```bash
cd frontend
npm install
```



## 💻 Uso

### Iniciar el Backend




```bash
cd backend
python app.py
```


### Iniciar el Frontend


```bash
cd frontend
npm run dev
```



La aplicación web estará disponible en `http://localhost:3000`
El servidor del backend estará disponible en `http://localhost:5000`


## 🛠️ Tecnologías

- **Backend**:
  - Python
  - Flask
  - YOLOv11-seg
  - OpenCV
  - PyTorch

- **Frontend**:
  - Next.js
  - React
  - TailwindCSS
  - TypeScript

## 📊 Resultados

### Métricas de Rendimiento

- mAP@50: 0.485
- mAP@[50:95]: 0.315
- Precisión (Maligno): 0.545
- Recall (Maligno): 0.571

### Visualización de Resultados

<div align="center">
  <img src="assets/results.png" alt="Resultados de Detección" width="600"/>
</div>

## 📚 Dataset

El modelo fue entrenado utilizando el conjunto de datos CBIS-DDSM, que contiene:
- 2,825 imágenes mamográficas
- Anotaciones detalladas de lesiones
- Clasificación benigna/maligna
- Segmentación manual por expertos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 👥 Autores

- **Mauricio Núñez** - *Desarrollo Principal* - [sm-nunez404](https://github.com/sm-nunez404)

## 📧 Contacto

Para preguntas y soporte, por favor contacta a:
- Email: [smnunez404@gmail.com]
- GitHub: [@sm-nunez404](https://github.com/sm-nunez404)

## 🙏 Agradecimientos

- CBIS-DDSM por proporcionar el conjunto de datos
- Ultralytics por YOLOv11
- La comunidad de código abierto

---

<div align="center">
  Desarrollado con ❤️ para la detección temprana del cáncer de mama
</div>

























