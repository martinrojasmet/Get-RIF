import re
from playwright.sync_api import Playwright, sync_playwright, expect
import easyocr
import requests
import cv2
import numpy as np
import re

base_url = "http://contribuyente.seniat.gob.ve/BuscaRif/"

def run(playwright: Playwright) -> None:
    keepGoing = True
    retries = 1

    # Get the RIF and Cedula
    rif = input("Introduzca el RIF: ")
    cedula = input("Introduzca la Cedula: ")
    print("==============================")

    # Go to page
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    context.set_default_timeout(60000)
    cookies = context.cookies()

    page = context.new_page()
    page.goto(base_url + "BuscaRif.jsp")

    while(keepGoing):
        # Fill Form
        page.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill(rif)
        page.get_by_role("textbox", name="Ingrese su número de Cédula o").fill(cedula)

        # Download Image
        page.get_by_role("img").screenshot(path="tmp/captcha.jpg")

        # Modify Image
        image = cv2.imread("tmp/captcha.jpg", 0)
        image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        image = cv2.GaussianBlur(image,(1,3),0)
        umbral = 0.5 * 255
        ret, image = cv2.threshold(image, umbral, 255, cv2.THRESH_BINARY)
        image = cv2.dilate(image, np.ones((2, 2), np.uint8))
        image = cv2.bitwise_not(image)
        cv2.imwrite("tmp/captcha-fixed.jpg", image)

        # Read Image
        reader = easyocr.Reader(['en'])
        result = reader.readtext('tmp/captcha-fixed.jpg', detail=0)

        # Screenshot of the captcha saved
        page.get_by_role("img").screenshot(path=f"utils/captcha_images/{result[0]}_NEW.jpg")

        # Fill Captcha
        page.locator("#codigo").fill(result[0])

        # Screenshot of the page
        page.screenshot(path="tmp/seniat.png")

        # Submit
        page.get_by_role("button", name="Buscar").click()

        keepGoing = page.get_by_text("EL código no coincide con la").is_visible()

        if (keepGoing):
            # Print error message
            print(f"Error en el intento número {retries}")
            retries += 1
        else:
            # Save screenshot of the final page
            page.screenshot(path="tmp/seniat_final.png")

            # Get the text of the page
            name = page.get_by_text(rif).inner_text()
            text = page.get_by_text("Actividad Económica:").inner_text()

            # Get the percentage of retention
            retention_percentage = re.search(r'retención del (\d+)%', text)

            print("==============================")
            print()

            # Print the name of the company/person
            print(f"Nombre: {name}")
            print()

            # Print if the person is a special contributor
            if("Contribuyente Ordinario del IVA" in text):
                print("Es contribuyente ordinario del IVA")

            # Print if the person is a formal contributor
            if("Contribuyente Formal del IVA" in text):
                print("Es contribuyente formal del IVA")

            # Print if the person is an agent of retention
            if("Agente de Retención del IVA" in text):
                print("Es agente de retención del IVA")

            # Print the percentage of retention
            print()
            if(retention_percentage):
                print(f"Porcentaje de retención: {retention_percentage.group(1)}%")
            else:
                print("No requiere retención")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)