from rembg import remove
import cv2
import mediapipe as mp
from PIL import Image
import time

sem_fundo = 'sem_fundo.png'

def extrair_fundo(input, output):
    input = Image.open(input)
    saida = remove(input).save(output)


def cortar_imagem(input, ouput):
  mp_face_detection = mp.solutions.face_detection
  mp_drawing = mp.solutions.drawing_utils

  # For static images:
  IMAGE_FILES = [input]
  with mp_face_detection.FaceDetection(
      model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
      image = Image.open(file)
      saida = remove(image).save('sbg'+file)
      image = cv2.imread(file)
      # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
      results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      # Draw face detections of each face.
      if not results.detections:
        continue
      annotated_image = image.copy()
      for detection in results.detections:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
        

        altura = int(h*0.90)
        h = altura + h
        y-=(int(altura/2))

        altura_div_largura = h/w

        #print(detection)
        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        img = Image.open(file)
        cropped_image = img.crop((x, y, x+w, y+h))
        cropped_image = cropped_image.resize((270, int(270*altura_div_largura)))
        #cropped_image.show()
        cropped_image.save('output.png')

        #mp_drawing.draw_detection(annotated_image, detection)
      #cv2.imwrite('testando' + str(idx) + '.png', annotated_image)


def colar_no_banner(path_banner, path_asset, coordenadas):
  banner = Image.open(path_banner)
  asset = Image.open(path_asset)
  Image.Image.paste(banner, asset, coordenadas, mask=asset)
  banner.save(path_banner)


fotos_lista = ['input1.jpg', 'input2.jpg', 'input3.jpg']

init = time.time()
for index, foto in enumerate(fotos_lista):
  print(f'Executando {foto}')
  extrair_fundo(foto, sem_fundo)
  cortar_imagem(sem_fundo, 'output.png')
  colar_no_banner('ex_banner.png', 'output.png', (0+(270*index), 133))

end = time.time()

print(f'Tempo de execução = {end-init} segundos')

