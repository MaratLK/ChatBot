from PIL import Image

# Открыть изображение
image = Image.open("валерич.JPG")

# Изменить размер до 640x360
resized_image = image.resize((330, 320))

# Сохранить изображение с новым размером
resized_image.save("resized_image2.jpg")
