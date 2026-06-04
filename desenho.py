import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

success, img = cap.read()

altura, largura, _ = img.shape

canvas = np.zeros((altura, largura, 3), dtype=np.uint8)

mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65
)

mpDraw = mp.solutions.drawing_utils

cv2.namedWindow("Air Draw PRO", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Air Draw PRO", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

xp = 0
yp = 0

cor_desenho = (255, 0, 255)

espessura_desenho = 8
raio_borracha = 45

def dedos_levantados(lmList, mao_direita):

    dedos = []

    if mao_direita:
        if lmList[4][1] < lmList[3][1]: dedos.append(1)
        else: dedos.append(0)
    else:
        if lmList[4][1] > lmList[3][1]: dedos.append(1)
        else: dedos.append(0)

    pontas = [8, 12, 16, 20]

    for ponta in pontas:
        if lmList[ponta][2] < lmList[ponta - 2][2]:
            dedos.append(1)
        else:
            dedos.append(0)

    return dedos

while True:

    success, img = cap.read()

    if not success:
        continue

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    estado_atual = "PARADO"

    if results.multi_hand_landmarks:

        for idx, handLms in enumerate(results.multi_hand_landmarks):

            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

            lado_rotulo = results.multi_handedness[idx].classification[0].label
            mao_direita = True if lado_rotulo == "Right" else False

            lmList = []
            for id, lm in enumerate(handLms.landmark):
                cx = int(lm.x * largura)
                cy = int(lm.y * altura)
                lmList.append((id, cx, cy))

            dedos = dedos_levantados(lmList, mao_direita)

            if mao_direita:
                x1, y1 = lmList[8][1], lmList[8][2] 

                if dedos == [0, 1, 0, 0, 0]:
                    estado_atual = "DESENHANDO"
                    cv2.circle(img, (x1, y1), 15, cor_desenho, cv2.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    cv2.line(canvas, (xp, yp), (x1, y1), cor_desenho, espessura_desenho, cv2.LINE_AA)
                    xp, yp = x1, y1
                
                elif dedos == [1, 1, 1, 1, 1]:
                    estado_atual = "LIMPANDO TUDO"
                    canvas = np.zeros((altura, largura, 3), dtype=np.uint8)
                    xp, yp = 0, 0
                else:
                    xp, yp = 0, 0

            else:
                x_box, y_box = lmList[9][1], lmList[9][2]

                if sum(dedos) > 0:
                    estado_atual = "APAGANDO"
                    
                    cv2.circle(img, (x_box, y_box), raio_borracha, (0, 255, 255), 2)

                    y_min = max(0, y_box - raio_borracha)
                    y_max = min(altura, y_box + raio_borracha)
                    x_min = max(0, x_box - raio_borracha)
                    x_max = min(largura, x_box + raio_borracha)
                    
                    canvas[y_min:y_max, x_min:x_max] = 0

    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, imgInv = cv2.threshold(
        imgGray,
        1,
        255,
        cv2.THRESH_BINARY_INV
    )

    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)

    img = cv2.bitwise_or(img, canvas)

    cv2.rectangle(img, (0, 0), (largura, 90), (35, 35, 35), cv2.FILLED)

    cv2.putText(img, f"STATUS: {estado_atual}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(img, f"DIREITA (Desenha/Limpa) | ESQUERDA (Apagador)", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Air Draw ", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()