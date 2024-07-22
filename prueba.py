def run(playwright: Playwright) -> None:
    # Go to page
    browser = playwright.chromium.launch(headless=False)

    if os.path.exists("utils/cookies.json"):
        context.add_cookies(json.loads(Path("utils/cookies.json").read_text()))
    else:
        context = browser.new_context()

    page = context.new_page()
    page.goto(base_url + "BuscaRif.jsp")

    # Fill Form
    page.get_by_role("textbox", name="Ingrese su número de Rif, seg").fill("V280529539")
    page.get_by_role("textbox", name="Ingrese su número de Cédula o").fill("28052953")

    # Download Image
    url = page.get_by_role("img").get_attribute('src').screenshot({ path: 'captcha.jpg' })


    # url = base_url + url
    # file = requests.get(url)
    # with open('tmp/captcha.jpg', 'wb') as f:
    #     f.write(file.content)
    # page.screenshot(path="tmp/seniat.png")

    # Modify Image
    image = cv2.imread("tmp/captcha.jpg", 0)
    image = cv2.blur(image, (2, 3))
    ret, image = cv2.threshold(image, 128, 200, cv2.THRESH_BINARY)
    cv2.imwrite("tmp/captcha-fixed.jpg", image)

    # Read Image
    reader = easyocr.Reader(['en'])
    result = reader.readtext('tmp/captcha-fixed.jpg', detail=0)
    print(result[0])

    # page.locator("#codigo").fill(result)
    # page.screenshot(path="tmp/seniat.png")
    # # page.once("dialog", lambda dialog: dialog.dismiss())
    # page.get_by_role("button", name="Buscar").click()
    # page.pause()

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)