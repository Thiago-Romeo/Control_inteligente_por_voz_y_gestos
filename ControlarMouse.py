import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np

# ==========================================
# VARIABLES
# ==========================================

ultimo_click = 0

mouseX_anterior = 0
mouseY_anterior = 0

# ==========================================
# CAMARA
# ==========================================

captura = cv2.VideoCapture(0)

mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,   # Más liviano y rápido
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================================
# PANTALLA
# ==========================================

anchoPantalla, altoPantalla = pyautogui.size()

# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    success, img = captura.read()

    if not success:
        break

    # Espejo
    img = cv2.flip(img, 1)

    # ==========================================
    # RGB
    # ==========================================

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resultado = hands.process(imgRGB)

    # ==========================================
    # MANOS
    # ==========================================

    if resultado.multi_hand_landmarks:

        for handLms, handType in zip(
            resultado.multi_hand_landmarks,
            resultado.multi_handedness
        ):

            tipoMano = handType.classification[0].label

            alto, ancho, _ = img.shape

            # ======================================
            # SOLO PULGAR E INDICE
            # ======================================

            pulgar = handLms.landmark[4]
            indice = handLms.landmark[8]

            x1 = int(pulgar.x * ancho)
            y1 = int(pulgar.y * alto)

            x2 = int(indice.x * ancho)
            y2 = int(indice.y * alto)

            # ======================================
            # DIBUJAR SOLO 2 PUNTOS
            # ======================================

            cv2.circle(
                img,
                (x1, y1),
                10,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.circle(
                img,
                (x2, y2),
                10,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (255, 0, 255),
                3
            )

            # ======================================
            # DISTANCIA
            # ======================================

            distancia = math.hypot(
                x2 - x1,
                y2 - y1
            )

            # ======================================
            # MANO DERECHA = MOVER MOUSE
            # ======================================

            if tipoMano == "Right":

                mouseX = np.interp(
                    x2,
                    [0, ancho],
                    [0, anchoPantalla]
                )

                mouseY = np.interp(
                    y2,
                    [0, alto],
                    [0, altoPantalla]
                )

                # ==================================
                # SUAVIZADO
                # ==================================

                suavizado = 5

                mouseX_suave = (
                    mouseX_anterior +
                    (mouseX - mouseX_anterior) / suavizado
                )

                mouseY_suave = (
                    mouseY_anterior +
                    (mouseY - mouseY_anterior) / suavizado
                )

                pyautogui.moveTo(
                    mouseX_suave,
                    mouseY_suave
                )

                mouseX_anterior = mouseX_suave
                mouseY_anterior = mouseY_suave

                cv2.putText(
                    img,
                    "MOUSE",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            # ======================================
            # MANO IZQUIERDA = CLICK
            # ======================================

            elif tipoMano == "Left":

                tiempo_actual = time.time()

                # Click solo cuando junta dedos
                if (
                    distancia < 35 and
                    tiempo_actual - ultimo_click > 0.7
                ):

                    pyautogui.click()

                    ultimo_click = tiempo_actual

                cv2.putText(
                    img,
                    "CLICK",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3
                )

    # ==========================================
    # MOSTRAR
    # ==========================================

    cv2.imshow(
        "Mouse con Manos",
        img
    )

    # ESC = salir
    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==========================================
# SALIDA
# ==========================================

captura.release()

cv2.destroyAllWindows()