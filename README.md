# gRIF
In Venezuela, individuals and companies with economic activity are assigned a unique identification number (RIF). Retrieving tax contribution records for these entities requires manual queries through the SENIAT website, a time-consuming process when handling multiple entries. gRIF (short for "get RIF") was created to automate this after a request from a relative to simplify bulk queries for frequent users.

This tool combines Playwright (for browser automation), EasyOCR (for CAPTCHA solving), and Tkinter (for interface design) to enable efficient mass queries via a desktop interface. Designed for Venezuelan users in mind, gRIF is handled with a common and familiar tool in Excel, also allowing the seamless copy-paste between spreadsheets, reducing the repetitive and manual effort involved.

![gRIF](https://github.com/martinrojasmet/gRIF/tree/main/utils/gRIF.png)

**Requirements**
- pandas
- re
- playwright
- easyocr
- requests
- cv2
- numpy
- openpyxl
- notifypy
