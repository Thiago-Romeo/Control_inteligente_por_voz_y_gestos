import cv2
import mediapipe as mp
import math
import numpy as np
import speech_recognition as sr
import threading
import subprocess 
import pyautogui
import time

from pycaw.pycaw import AudioUtilities

# =========================
# AUDIO WINDOWS
# =========================

tracking_activo = False  # Tracking de dedos
modo = "volumen"
ultimo_click = 0         # Tiempo de espera entre clics

dispositivos = AudioUtilities.GetSpeakers()
volumen = dispositivos.EndpointVolume  # <--- Corregido a 'volumen'

rangoVol = volumen.GetVolumeRange()
volMin = rangoVol[0]
volMax = rangoVol[1]

# =========================
# CÁMARA & MEDIAPIPE
# =========================

captura = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

mpDraw = mp.solutions.drawing_utils
anchoPantalla, altoPantalla = pyautogui.size()

# =========================
# CONTROL POR VOZ
# =========================

recognizer = sr.Recognizer()

def escuchar_comandos():
    global tracking_activo, modo

    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source)

            texto = recognizer.recognize_google(
                audio,
                language="es-ES"
            ).lower()

            print("Escuché:", texto)

            if "modo mouse" in texto:
                modo = "mouse"
                print("MODO MOUSE")

            elif "modo volumen" in texto:
                modo = "volumen"
                print("MODO VOLUMEN")

            if "desactiva" in texto:
                tracking_activo = False
                print("TRACKING DESACTIVADO")

            elif "activa" in texto:
                tracking_activo = True
                print("TRACKING ACTIVADO")
            
            if "abre juego" in texto:
                subprocess.Popen(
                    [
                        r"D:\Riot Games\Riot Client\RiotClientServices.exe",
                        "--launch-product=valorant",
                        "--launch-patchline=live"  
                    ]
                )    
                print("Abriendo Valorant...")

        except:
            pass

# Iniciar hilo de voz
hilo_voz = threading.Thread(target=escuchar_comandos)
hilo_voz.daemon = True
hilo_voz.start()

# =========================
# LOOP PRINCIPAL
# =========================

while True:
    success, img = captura.read()
    if not success:
        break

    # Espejo (opcional, facilita el control)
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = hands.process(imgRGB)

    alto, ancho, _ = img.shape

    if resultado.multi_hand_landmarks and tracking_activo:
        for handLms in resultado.multi_hand_landmarks:
            lista = []

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                lista.append((id, cx, cy))

            # Pulgar = 4, Índice = 8
            x1, y1 = lista[4][1], lista[4][2]
            x2, y2 = lista[8][1], lista[8][2]

            # Dibujar puntos y línea
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Distancia entre pulgar e índice
            distancia = math.hypot(x2 - x1, y2 - y1)

            # --- ACCIONES SEGÚN EL MODO ---
            if modo == "volumen":
                vol = np.interp(distancia, [20, 200], [volMin, volMax])
                volumen.SetMasterVolumeLevel(vol, None)

                # Dibujar barra de volumen
                barra = np.interp(distancia, [20, 200], [400, 150])
                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(img, (50, int(barra)), (85, 400), (0, 255, 0), cv2.FILLED)

            elif modo == "mouse":
                mouseX = np.interp(x2, [0, ancho], [0, anchoPantalla])
                mouseY = np.interp(y2, [0, alto], [0, altoPantalla])

                pyautogui.moveTo(mouseX, mouseY)

                # Click con tiempo de espera (0.5 segundos entre clics)
                tiempo_actual = time.time()
                if distancia < 35 and (tiempo_actual - ultimo_click > 0.5):
                    pyautogui.click()
                    ultimo_click = tiempo_actual

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # Interfaz en pantalla
    estado = "ACTIVO" if tracking_activo else "DESACTIVADO"
    
    cv2.putText(
        img,
        f"Tracking: {estado}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if tracking_activo else (0, 0, 255),
        3
    )

    cv2.putText(
        img,
        f"Modo: {modo}",
        (10, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        3
    )

    cv2.imshow("Control Inteligente", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

captura.release()
cv2.destroyAllWindows()