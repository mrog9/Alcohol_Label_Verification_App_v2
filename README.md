First decision was what website host to use. I decided to use Render because it was known to be easy to set up web services with frontend and backend functionality.

Next, I had to anticipate what kind of labels, the web service needed to work for. At first I was trying to create a web service that could handle complex photos such as real photos of alcohol labels. For the more complicated labels, the easyocr python package was the only utility I found that would extract text. However, it was too bulky to set up environment with on Render (needed torch and torchvision).

I went back to the directions and realized that the web service just needed to work for simple labels such as the one given in the directions. Therefore, I decided to use the Pillow, Pytesseract, and Flask libraries. Pillow is a lightweight package that would process the uploaded image, pytesseract  would extract the text from that image, and flask would coordinate information being sent between the frontend (html page) and backend of the application.

I added bonus feature to this app by having the image upload into html page and rectangles outlining the headings in the image that are mismatched with the form labels. Furthermore, do make sure the website ran faster, I used javascript to pass information from html to app.py.

I made sure the app worked locally first and then pushed to github. To deploy on Render, a Dockerfile was created to help create the environment for my web service to operate in. A requirements.txt file included the python libraries used.

TO RUN LOCAL
--------------

1. Need to download tesseract for your specific computer and take note where it was downloaded
2. pip install flask pytesseract pillow
3. In utils.py, pytesseract.pytesseract.tesseract_cmd = "localPath/tesseract" needs to be added below package imports.


LIMITATIONS
--------------

This app works for specific types of images where the different parts of the labels are clearly laid out and follow a specific order and pattern. For real world labels, this app would not work. Easyocr package or another advanced ocr models would need to be used. Furthermore, opencv python package would allow more advanced preprocessing. However, these items are too "heavy" to use on free tier platforms so there would probably be a cost for using these utilities. 