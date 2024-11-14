from PIL import Image

# Открыть изображение
image = Image.open("валерич360.JPG")

# Изменить размер до 640x360
resized_image = image.resize((640, 360))

# Сохранить изображение с новым размером
resized_image.save("resized_image.jpg")
