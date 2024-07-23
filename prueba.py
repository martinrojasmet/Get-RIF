# def run(playwright: Playwright) -> None:
#     # Go to page
#     browser = playwright.chromium.launch(headless=False)

#     if os.path.exists("utils/cookies.json"):
#         context.add_cookies(json.loads(Path("utils/cookies.json").read_text()))
#     else:
#         context = browser.new_context()

#     page = context.new_page()
#     page.goto(base_url + "BuscaRif.jsp")

#     # Fill Form
#     page.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill("V280529539")
#     page.get_by_role("textbox", name="Ingrese su número de Cédula o").fill("28052953")

#     # Download Image
#     url = page.get_by_role("img").get_attribute('src').screenshot({ path: 'captcha.jpg' })


#     # url = base_url + url
#     # file = requests.get(url)
#     # with open('tmp/captcha.jpg', 'wb') as f:
#     #     f.write(file.content)
#     # page.screenshot(path="tmp/seniat.png")

#     # Modify Image
#     image = cv2.imread("tmp/captcha.jpg", 0)
#     image = cv2.blur(image, (2, 3))
#     ret, image = cv2.threshold(image, 128, 200, cv2.THRESH_BINARY)
#     cv2.imwrite("tmp/captcha-fixed.jpg", image)

#     # Read Image
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext('tmp/captcha-fixed.jpg', detail=0)
#     print(result[0])

#     # page.locator("#codigo").fill(result)
#     # page.screenshot(path="tmp/seniat.png")
#     # # page.once("dialog", lambda dialog: dialog.dismiss())
#     # page.get_by_role("button", name="Buscar").click()
#     # page.pause()

#     context.close()
#     browser.close()

# with sync_playwright() as playwright:
#     run(playwright)


import re
from playwright.sync_api import Playwright, sync_playwright, expect
import easyocr
import requests
import cv2
import pytesseract
import numpy as np

def show(image):
    cv2.imshow("1", np.array(image))
    cv2.waitKey(0)

# # Modify Image
# imagen = cv2.imread("tmp/captcha.jpg", 0)

# # # Leemos la imagen en modo escala de grises
# # imagen = cv2.imread('imagen.jpg', cv2.IMREAD_GRAYSCALE)

# # Normalizamos los valores de los píxeles
# # imagen = cv2.normalize(imagen, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# # Aplicamos un desenfoque no nítido para mejorar la nitidez
# # imagen = cv2.GaussianBlur(imagen, (7, 3), 1)

# # Ajustamos el contraste
# # imagen = cv2.addWeighted(imagen, 1.0, imagen, 0.0, 0)

# # Calculamos el umbral para la binarización
# umbral = 0.5 * 255

# # Convertimos la imagen a binaria
# imagen = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)[1]

# # Aplicamos un desenfoque adaptativo
# imagen = cv2.medianBlur(imagen, 5)

# # Reducimos el número de colores a 8
# imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
# # imagen = cv2.reduceColors(imagen, 8)


# cv2.imwrite("tmp/captcha-fixed.jpg", imagen)

# Modify Image
image = cv2.imread("tmp/captcha.jpg", 0)
# image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
# image = cv2.blur(image, (1, 3))
# image = cv2.medianBlur(image, 3)
image = cv2.GaussianBlur(image,(1,3),0)
umbral = 0.5 * 255
ret, image = cv2.threshold(image, umbral, 255, cv2.THRESH_BINARY)
image = cv2.dilate(image, np.ones((2, 2), np.uint8))
image = cv2.bitwise_not(image)
# # image = cv2.erode(image, np.ones((2, 2), np.uint8))
cv2.imwrite("tmp/captcha-fixed.jpg", image)

# Read Image
reader = easyocr.Reader(['en'])
result = reader.readtext('tmp/captcha-fixed.jpg', detail=0)
print(result[0])
