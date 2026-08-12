# Control_inteligente_por_voz_y_gestos

Este proyecto permite interactuar con la computadora mediante gestos de la mano capturados con la cámara y comandos de voz a través del micrófono. Desarrollado en Python con OpenCV, MediaPipe, PyAutoGUI y SpeechRecognition.

## 📜 Descripción de los Scripts

### 1. 🖱️ ControlarMouse.py

Convierte tu mano en un ratón virtual:

- **Mover el cursor:** Mueve el puntero en la pantalla siguiendo la posición de tu dedo índice (mano derecha).
- **Hacer clic:** Al juntar el pulgar y el índice (mano izquierda o gesto asignado) a una distancia menor a 35 píxeles, simula un clic del ratón.
- **Suavizado de movimiento:** Incluye un algoritmo de interpolación para evitar saltos bruscos del puntero.

### 2. 🔊 ControlarVolumen.py

Combina reconocimiento de voz y visión por computadora:

- **Control de Volumen:** Ajusta el volumen principal de Windows midiendo la distancia en pantalla entre la punta del dedo pulgar y el índice. Incluye una barra gráfica intuitiva en tiempo real.
- **Comandos de Voz:** Trabaja en segundo plano (multiprocesamiento con Threads) escuchando frases como:
  - "Activa" / "Desactiva": Habilita o deshabilita el seguimiento de la mano.
  - "Abre Valorant" (o ejecutable configurado): Abre la plataforma o juego mediante procesos en segundo plano.

## 🛠️ Guía de Instalación

### 1. Requisitos Previos

- Python 3.10, 3.11 o 3.12 instalado.
- Cámara web funcional.
- Micrófono (para los comandos de voz).

### 2. Clonar el Repositorio

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd TU-REPOSITORIO
```

### 3. Crear y Activar un Entorno Virtual

Para evitar conflictos de versiones con tu sistema global:

En Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 4. Instalar Dependencias

Instala todas las librerías necesarias ejecutando:

```bash
python -m pip install opencv-python mediapipe pyautogui numpy SpeechRecognition PyAudio pycaw comtypes
```

## 🚀 Cómo Ejecutar los Programas

Asegúrate de tener activado el entorno virtual (`.venv`).

Para probar el control del puntero:

```bash
python ControlarMouse.py
```

Para probar el control de volumen y voz:

```bash
python ControlarVolumen.py
```

(Presiona la tecla **ESC** en la ventana de la cámara para salir de cualquiera de los dos scripts).

## 🐛 Problemas Comunes y Soluciones

Durante el desarrollo de este proyecto surgieron algunos inconvenientes de compatibilidad que se resolvieron de la siguiente forma:

### 1. `ModuleNotFoundError: No module named 'mediapipe'` en VS Code

- **Causa:** El editor de VS Code estaba apuntando al intérprete global de Python y no al del entorno virtual (`.venv`) donde estaban instaladas las librerías.
- **Solución:** En VS Code presionar `Ctrl + Shift + P` → Buscar `Python: Select Interpreter` → Seleccionar la opción que contenga `.\.venv\Scripts\python.exe`.

### 2. `AttributeError: 'AudioDevice' object has no attribute 'Activate'`

- **Causa:** Cambio de sintaxis en las versiones recientes de la librería `pycaw`. El método `.Activate()` junto con `comtypes`/`ctypes` quedó obsoleto.
- **Solución:** Se simplificó la inicialización del objeto de audio reemplazando el código antiguo por:

```python
dispositivos = AudioUtilities.GetSpeakers()
volumen = dispositivos.EndpointVolume
volumen.SetMasterVolumeLevelScalar(vol_scalar, None)
```

### 3. Conflicto de Versiones entre OpenCV y NumPy

- **Causa:** Incompatibilidad entre `opencv-python` 5.x y versiones antiguas de `numpy` instaladas automáticamente por `mediapipe`.
- **Solución:** Reinstalar explícitamente versiones estables y compatibles:

```bash
python -m pip install "numpy<2" "opencv-python<4.10" --force-reinstall
```

### 4. La Cámara no abre o se congela el programa

- **Causa:** La webcam quedó bloqueada por un proceso anterior finalizado bruscamente o por otra aplicación (Zoom, Teams, etc.).
- **Solución:** Cerrar aplicaciones que usen la cámara, reiniciar el terminal y verificar en el código si el índice de la cámara es `cv2.VideoCapture(0)` o `cv2.VideoCapture(1)`.
