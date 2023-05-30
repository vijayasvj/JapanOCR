import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 

logo = Image.open(r"logo-1.png")
st.image(logo)
#title
st.title("Basic Japanese OCR - Extract Text from Images")

#subtitle
st.markdown("## Optical Character Recognition - Using `streamlit`")

st.markdown("")

#image uploader
image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])

def calculate_line_length(line):
    x1, y1, x2, y2 = line[0]
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return length

def find_background_lines(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.where(gray > 190 , 255, 0).astype(np.uint8)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

    # Apply Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=50)

    # Draw the detected lines on the image
    line_image = gray.copy()
    for line in lines:
        if calculate_line_length(line) > 0:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (255,255,255), 2)

    return line_image

def load_model(): 
    reader = ocr.Reader(['ja'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

if image is not None:

    input_image = Image.open(image) #read image
    st.image(input_image) #display image

    with st.spinner("🤖 AI is at Work! "):
        
        input_image = find_background_lines(np.array(input_image))
        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results


        for text in result:
            result_text.append(text[1])

        st.write(result_text)
    #st.success("Here you go!")
    st.balloons()
else:
    st.write("Upload an Image")

st.caption("Made with ❤️ by innovative minds of AnywareLabs")





