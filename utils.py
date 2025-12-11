import pytesseract
from pytesseract import Output
import io
from PIL import Image, ImageDraw
import os
from flask import request


# deleting any files previously saved

def delete_any_files(folder):

    with os.scandir(folder) as entries:
        if any(entries):
            for e in entries:
                os.remove(e.path())


# this method is to make sure the form fields are not empty. It goes through 
# each field and adds to the comment string if it is empty and returns the string.

def validate_form_input(b, p, a, n, f):

    comment_dict = dict()

    if not b:

        comment_dict["brand"] = "Brand name was not given.\n"

    if not p:

        comment_dict["product"] = "Product type was not given.\n"

    if not a:

        comment_dict["alcohol"] = "Alcohol percentage was not given.\n"

    if not n:

        comment_dict["contents"] = "Net contents were not given.\n"

    if not f:

        comment_dict["file"] = "A file was not uploaded."

    return comment_dict



# this method recieves the uploaded file, reads it and then sends to pillow object
# to process it. It is put in a "try" so that if it fails for it not being in the
# correct format then a comment will be added telling the user it has to be in a certain format.
# if its successful, then the image is converted to gray scale and is upscaled before 
# pytesseract extracts text from the image. The text and comment is then returned.

def preprocess_image(file_obj):

    fail_flag = False
    comment = ""
    img = None

    try:

        img_bytes = file_obj.read()
        img = Image.open(io.BytesIO(img_bytes))

    except Exception as e:

        comment = "Make sure image is in either jpg, png, gif, bmp, tiff, webp, ico format."
        fail_flag = True

    if not fail_flag:

        # img = img.convert("L")  # grayscale
        img = img.resize((img.width * 2, img.height * 2))  # upscale

    return comment, img



# this method extracts the text and rectangles for each segment of text
# i stored the each word and the dims of the box that contained
# that word

def get_rectangles_text(img):

    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    data_list = {'dims':[], 'text':[]}

    for i in range(len(data['level'])):

        if data['level'][i] == 5:  # word-level

            if data['text'][i].strip():

                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                data_list['dims'].append([x, y, w, h])
                data_list['text'].append(data['text'][i].strip())

    return data_list


# from the object created from the method above, I put each word
# in the label heading it should be in. had to make a few assumptions
# to how it categorized in each heading


def extract_objs_from_text(data_list):

    word_list = data_list['text']

    brand_words_on_label = []
    prod_words_on_label = []
    alc_percent = ""
    net_contents = ""

    j = 0
    

    for i in range(len(word_list)):

        if word_list[i].isupper():

            brand_words_on_label.append(word_list[i])

        else:

            j = i
            break

    brand_on_label = " ".join(brand_words_on_label).lower()

    for i in range(j, len(word_list)):

        if "%" not in word_list[i]:

            prod_words_on_label.append(word_list[i])

        else:

            j=i
            break

    prod_on_label = " ".join(prod_words_on_label).lower()

    for c in word_list[j]:

        if c.isnumeric():

            alc_percent += c

    alc_percent += '%'

    for i in range(j+1, len(word_list)):

        if 'L' in word_list[i]:

            net_contents = word_list[i-1] + word_list[i]

    net_contents = net_contents.lower()

    return brand_on_label, prod_on_label, alc_percent, net_contents


# this method forms the complete box of each label heading (of each line)
# that doesnt match the form heading

def highlight_image(fail_pos_list, img, data_list, label_segs):

    draw = ImageDraw.Draw(img)

    for i in fail_pos_list:

        tot_w = 0
        x, y, w, h= 0,0,0,0
        first_flag = True
        cnt = 0

        print(i)
        print(label_segs[i])

        for j in range(len(data_list['text'])):

            if data_list['text'][j].lower() in label_segs[i]:

                if first_flag:

                    x, y, w, h = data_list['dims'][j][0], data_list['dims'][j][1], data_list['dims'][j][2], data_list['dims'][j][3]
                    first_flag = False

                else:

                    w = data_list['dims'][j][2] + 5

                cnt += 1

                tot_w += w

        draw.rectangle([x, y, x + tot_w + cnt*6, y + h], outline="red", width=2)

    return img


# this method actually validates the label with the form information.
# i used a few of the above methods in this method. i found the retangles 
# for each word. categorized each word in the appropriate heading. 
#highlighted the heading which didnt match the form heading.


def validate_label(file_obj, b, p, a, n):

    comment, img = preprocess_image(file_obj)
    fail_pos_list = []
    label_segs = []
    data_list = None

    if not comment:

        data_list = get_rectangles_text(img)

        if not data_list['text']:

            comment += "Take clearer picture. No text could be recognized."

        else:

            bl, pl, al, nl = extract_objs_from_text(data_list)
            label_segs = [bl, pl, al, nl]

            if not b == bl:

                comment += "Brand on form does NOT match brand on label.\n"
                fail_pos_list.append(0)

            if not p == pl:

                comment += "Product on form does NOT match product on label.\n"
                fail_pos_list.append(1)

            if not a == al:

                comment += "Alcohol percentage on form does NOT match percentage on label.\n"
                fail_pos_list.append(2)

            if not n == nl:

                comment += "Net contents on form does NOT match net contents on label.\n"
                fail_pos_list.append(3)

            img = highlight_image(fail_pos_list, img, data_list, label_segs)
    

    return comment, data_list, img


# this method gets all necessary comments by going through form headings first, then
# getting text through image, and then validating labels.


def getComments():

    text = ""
    comment = ""
    img = None
    comment_dict = {"missing_headers": None,
                "comments_after_submit":"",
                "success":""}
    data_list = None

    brand = request.form['brand'].lower()
    prod = request.form['product'].lower()
    alc = request.form['content'].lower().replace(" ","")
    net = request.form['net'].lower().replace(" ","")
    file = request.files["file"]

    comment_dict['missing_headers'] = validate_form_input(brand, prod, alc, net, file)

    if not comment_dict['missing_headers']:

        comment, data_list, img = validate_label(file, brand, prod, alc, net)

        if data_list:

            if data_list['text']:

                text = " ".join(data_list['text'])
            
        if not comment:
            comment_dict["success"] = "SUCCESS!"
        else:
            comment_dict["comments_after_submit"] = comment

    return comment_dict, file, img, text

# saving the image so it can be used in html script

def save_image(app, file_obj, img):

    filepath = None

    if img:

        raw_path = os.path.join(app.config['UPLOAD_FOLDER'], file_obj.filename)
        img.save(raw_path)
        filepath = raw_path.replace('static/', "")
        filepath = filepath.replace("\\", "/")

    return filepath
