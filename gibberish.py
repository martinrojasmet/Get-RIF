# # from playwright.sync_api import sync_playwright

# # playwright = sync_playwright().start()

# # browser = playwright.chromium.launch()
# # page = browser.new_page()
# # page.goto("http://contribuyente.seniat.gob.ve/BuscaRif/BuscaRif.jsp")
# # page.screenshot(path="images/example.png")
# # browser.close()

# # playwright.stop()

# # # import re
# # # from playwright.sync_api import Page, expect

# # # def test_has_title(page: Page):
# # #     page.goto("https://playwright.dev/")

# # #     # Expect a title "to contain" a substring.
# # #     expect(page).to_have_title(re.compile("Playwright"))

# # # def test_get_started_link(page: Page):
# # #     page.goto("https://playwright.dev/")

# # #     # Click the get started link.
# # #     page.get_by_role("link", name="Get started").click()

# # #     # Expects page to have a heading with the name of Installation.
# # #     expect(page.get_by_role("heading", name="Installation")).to_be_visible()

# import re
# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://www.google.com/")
#     page.get_by_label("Buscar", exact=True).click()
#     page.get_by_label("Buscar", exact=True).fill("seniat")
#     page.goto("https://declaraciones.seniat.gob.ve/index.htm")
#     page.goto("https://declaraciones.seniat.gob.ve/portal/page/portal/PORTAL_SENIAT")
#     page.goto("https://www.google.com/search?q=seniat&sca_esv=2a19a3414e05e997&source=hp&ei=qYeeZqzrLJC_kPIPoMaH6AY&iflsig=AL9hbdgAAAAAZp6VuTsWTxLK__PrftqDFoMs70qbq0G_&ved=0ahUKEwjs47bMh7uHAxWQH0QIHSDjAW0Q4dUDCA0&uact=5&oq=seniat&gs_lp=Egdnd3Mtd2l6IgZzZW5pYXQyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyCxAuGIAEGMcBGK8BMggQABiABBixAzIFEAAYgAQyCxAuGIAEGMcBGK8BMgUQABiABDIIEAAYgAQYsQMyCBAAGIAEGLEDSPIUUJEHWPoTcAJ4AJABAJgBXaABygSqAQE3uAEDyAEA-AEBmAIJoAL7BKgCCsICEBAuGAMY5QIY6gIYjAMYjwHCAhAQABgDGOUCGOoCGIwDGI8BwgIOEC4YgAQYsQMY0QMYxwHCAgsQABiABBixAxiDAcICCxAuGIAEGLEDGIMBwgIOEAAYgAQYsQMYgwEYigXCAgUQLhiABMICChAAGIAEGLEDGArCAg0QLhiABBjHARgKGK8BwgIHEAAYgAQYCpgDCJIHAzguMaAHoEI&sclient=gws-wiz")
#     expect(page.get_by_role("link", name="Consulta de RIF")).to_be_visible()
#     page.get_by_role("link", name="Consulta de RIF").click()
#     with page.expect_popup() as page1_info:
#         page.get_by_role("link", name="Consulta de RIF").click()
#     page1 = page1_info.value
#     page1.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill("123")
#     page1.get_by_role("textbox", name="Ingrese su número de Cédula o").click()
#     page1.get_by_role("textbox", name="Ingrese su número de Cédula o").fill("12")
#     page1.get_by_role("img").click()
#     page1.locator("#codigo").click()
#     page1.close()
#     page1.get_by_role("button", name="Cancelar").click()
#     with page.expect_popup() as page2_info:
#         page.get_by_role("link", name="Consulta de RIF").click()
#     page2 = page2_info.value
#     page2.once("dialog", lambda dialog: dialog.dismiss())
#     page2.get_by_role("button", name="Buscar").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)


# get_by_role("button", name="Buscar")

# ----------------------------------

# # # import easyocr

# # # reader = easyocr.Reader(['en'])
# # # result = reader.readtext('images/captcha.jpg')
# # # print(result)

# import cv2
# import numpy as np
# import easyocr

# # Method 1
# image = cv2.imread("images/captcha.jpg", 0)

# image = cv2.blur(image, (2, 3))

# ret, image = cv2.threshold(image, 128, 200, cv2.THRESH_BINARY)

# cv2.imwrite("images/captcha-fixed.jpg", image)

# reader = easyocr.Reader(['en'])
# result = reader.readtext('images/captcha-fixed.jpg', detail=0)
# print(result[0])


# # cv2.imshow("Grayscale (Method 1)", image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


import re
from playwright.sync_api import Playwright, sync_playwright, expect
import easyocr
import requests
import cv2

base_url = "http://contribuyente.seniat.gob.ve/BuscaRif/"

def run(playwright: Playwright) -> None:
    # Go to page
    browser = playwright.chromium.launch(headless=True)

    # if os.path.exists("utils/cookies.json"):
    #     context.add_cookies(json.loads(Path("utils/cookies.json").read_text()))
    # else:
    context = browser.new_context()
    context.set_default_timeout(15000)
    cookies = context.cookies()
    # Path("utils/cookies.json").write_text(json.dumps(cookies))

    page = context.new_page()
    page.goto(base_url + "BuscaRif.jsp")

    # Fill Form
    page.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill("V280529539")
    page.get_by_role("textbox", name="Ingrese su número de Cédula o").fill("28052953")

    # Download Image
    page.get_by_role("img").screenshot(path="tmp/captcha.jpg")

    # Modify Image
    image = cv2.imread("tmp/captcha.jpg", 0)
    image = cv2.blur(image, (2, 3))
    ret, image = cv2.threshold(image, 128, 200, cv2.THRESH_BINARY)
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
    image = cv2.blur(image, (1, 3))
    # image = cv2.medianBlur(image, 5)
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

