from PIL import Image
import sys
import pyocr
import pyocr.builders
import cv2
import requests

#grayscale
img_pass = r'jpgディレクトリまでのパス'
img = cv2.imread(img_pass)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(r'ファイルを作成したい場所までのパス\grayscale.jpg', gray)
img_grayscale_pass = r'grayscale.jpgディレクトリまでのパス\grayscale.jpg'

#judge
pyocr.tesseract.TESSERACT_CMD = r'Tesseract-OCRまでのパス\Tesseract-OCR\tesseract.exe'
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]

result = tool.image_to_string(
    Image.open(img_grayscale_pass),
    lang="jpn+eng",
    builder=pyocr.builders.TextBuilder()
)
#確認用
print(result)
#ISBNという文字列の位置を探す
index = result.find("ISBN")
result_list = list(result) #文字列を1文字ずつ配列に代入
isbn_list = []
for i in range(index+4,index+21):
    isbn_list.append(result_list[i])

isbn_number = ''.join(isbn_list)
#ISBN番号確認
print(isbn_number)

#GoogleBooksAPI
url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
def main(isbn):
    req_url = url + isbn
    response = requests.get(req_url)
    return response.text

if __name__ == "__main__":
    while True:
        print(main(input("ISBN >>>") + isbn_number))
        break
