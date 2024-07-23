import re
from playwright.sync_api import Playwright, sync_playwright, expect
import easyocr
import requests
import cv2
import pytesseract
import numpy as np

base_url = "http://contribuyente.seniat.gob.ve/BuscaRif/"

def run(playwright: Playwright) -> None:
    # Go to page
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    context.set_default_timeout(15000)
    cookies = context.cookies()

    page = context.new_page()
    page.goto(base_url + "BuscaRif.jsp")

    # Fill Form
    page.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill("V280529539")
    page.get_by_role("textbox", name="Ingrese su número de Cédula o").fill("28052953")

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

    # Fill Captcha
    page.locator("#codigo").fill(result[0])

    # Screenshot of the page
    page.screenshot(path="tmp/seniat.png")

    # # page.once("dialog", lambda dialog: dialog.dismiss())
    # page.get_by_role("button", name="Buscar").click()
    # page.pause()

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
