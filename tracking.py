import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils

estilo_pontos = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
estilo_linhas = mpDraw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1)

DICIONARIO_GESTOS = {
    (1, 1, 1, 1, 1): "mao aberta",
    (0, 0, 0, 0, 0): "mao fechada",
    (1, 0, 0, 0, 1): "hang loose",
    (1, 0, 0, 0, 0): "joinha"
}

pTime, cTime = 0, 0

print("Iniciando o rastreamento... Olhe para a câmera do notebook!")
print("Pressione a tecla 'ESC' na janela de vídeo para encerrar.")

with mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands, \
     mPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

    while True:
        sucesso, img = cap.read()
        if not sucesso:
            print("Erro ao acessar a webcam do notebook.")
            continue
        
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results_hands = hands.process(imgRGB)
        results_pose = pose.process(imgRGB)
        
        gesto_atual = "Nenhum"
        comando_corpo = "Padrao"

        if results_pose.pose_landmarks:
            mpDraw.draw_landmarks(img, results_pose.pose_landmarks, mPose.POSE_CONNECTIONS, estilo_pontos, estilo_linhas)
            
            pontos_corpo = results_pose.pose_landmarks.landmark
            if pontos_corpo[15].y < pontos_corpo[11].y or pontos_corpo[16].y < pontos_corpo[12].y:
                comando_corpo = "BRACO LEVANTADO"

        if results_hands.multi_hand_landmarks:
            for idx, handLms in enumerate(results_hands.multi_hand_landmarks):
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, estilo_pontos, estilo_linhas)
                
                lado_detectado = results_hands.multi_handedness[idx].classification[0].label
                mao_direita = True if lado_detectado == "Left" else False
                
                pontas_id = [8, 12, 16, 20]
                dedos_abertos = []
                
                x_indicador = handLms.landmark[5].x
                x_minimo = handLms.landmark[17].x
                palma_de_frente = not (x_indicador > x_minimo if mao_direita else x_indicador < x_minimo)
                
                polegar_aberto = 0
                if mao_direita:
                    if palma_de_frente and handLms.landmark[4].x < handLms.landmark[3].x: polegar_aberto = 1
                    elif not palma_de_frente and handLms.landmark[4].x > handLms.landmark[3].x: polegar_aberto = 1
                else:
                    if palma_de_frente and handLms.landmark[4].x > handLms.landmark[3].x: polegar_aberto = 1
                    elif not palma_de_frente and handLms.landmark[4].x < handLms.landmark[3].x: polegar_aberto = 1
                        
                dedos_abertos.append(polegar_aberto)
                
                for id_ponta in pontas_id:
                    if handLms.landmark[id_ponta].y < handLms.landmark[id_ponta - 3].y:
                        dedos_abertos.append(1)
                    else:
                        dedos_abertos.append(0)
                
                chave_gesto = tuple(dedos_abertos)
                gesto_atual = DICIONARIO_GESTOS.get(chave_gesto, f"{dedos_abertos.count(1)} dedos")

        cv2.putText(img, f"GESTO: {str(gesto_atual).upper()}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cor_postura = (0, 255, 0) if comando_corpo == "BRACO LEVANTADO" else (255, 255, 255)
        cv2.putText(img, f"POSTURA: {comando_corpo}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_postura, 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (10, 40), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)

        cv2.imshow("Tracking de Gestos e Corpo - MediaPipe Puro", img)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
print("Sistema encerrado com sucesso!")
        