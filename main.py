import streamlit as st #streamlitの基本的な使い方
import json
import requests
import io
from PIL import Image
from PIL import ImageDraw


st.title('顔認識アプリ')

subscription_key = "0d04763be5e24e03bd9cc17ff5aaa032"
assert subscription_key

face_api_url = "https://19991130shoto.cognitiveservices.azure.com/face/v1.0/detect"


#画像の読み込み
uploaded_file = st.file_uploader("Choose an image...", type = "jpg")
#画像の記述
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format = "JPEG")
        bynary_img = output.getvalue()

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "returnFaceId": "true",
        "returnFaceAttributes": "age, gender, headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion, accessories, blur, exposure, noise"
    }

    response = requests.post(face_api_url, params = params, headers = headers, data = bynary_img)#四つ目は今回はjson = {"url": image_url}ではない
    results = response.json()

    for result in results:
        rect = result['faceRectangle']

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill = None, outline = 'green', width = 5)

    st.image(img, caption = "Uploaded Image.", use_column_width = True)





