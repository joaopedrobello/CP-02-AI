import cv2
from easyocr import Reader
from deep_translator import GoogleTranslator

reader = Reader(['en'], gpu=True)
cap = cv2.VideoCapture("video.mp4")
threshold = 0.6

while True:
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
        #break
    
    frame = cv2.resize(frame, (960, 540))
    
    cv2.imshow("Video", frame)

    text = ''
    translate = ''

    results = reader.readtext(frame)

    print(results)

    for result in results:
        text = text + result[1] + ' '

        translate_text = GoogleTranslator(source='auto', target='pt').translate(result[1])

        translate = translate + translate_text + ' '
        
        top_left = tuple(result[0][0]) 
        bottom_right = tuple(result[0][2])
        
        try:
            if result[2] >= threshold:
                frame = cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2) 
                # frame = cv2.putText(frame, result[1], (top_left[0], top_left[1])
                #                     , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                frame = cv2.putText(frame, translate_text, (top_left[0], top_left[1])
                                    , cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        except Exception as e:
            print(e)

    text = text[:-1]
    translate = translate[:-1]

    print(f'Texto video normal: {text}')
    print(f'Texto video traduzido: {translate}')

    cv2.imshow("Video Traduzido", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()