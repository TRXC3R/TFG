import os
from typing import List
from PIL import Image
from layer import Layer


class AvatarGenerator:
    def __init__(self, images_path: str):
        self.layers : List[Layer] = self.load_images_layers(images_path)
        self.background_color = (255,255,255)
        self.output_path_string: str = "./output"
        os.makedirs(self.output_path_string, exist_ok=True)


    def load_images_layers(self, images_path: str):
        subdirs = sorted(os.listdir(images_path))
        print(f"Found subdirectories: {subdirs}")
        layers: List[Layer] = []
        for subdir in subdirs:
            layer_path = os.path.join(images_path, subdir)
            layer = Layer(layer_path)
            layers.append(layer)
            print(layer_path)

        layers[3].rarity = 0.15 #Probability to generate accesory is 15%
        return layers
    
    def save_image(self, image: Image.Image):
        image_file_name = "avatar.png"
        image_save_path = os.path.join(self.output_path_string, image_file_name)
        image.save(image_save_path)
    
    def save_multiple_image(self, image: Image.Image, i: int = 0):
        image_index = str(i).zfill(4) # Pad with leading zeros
        image_file_name = f"avatar_{image_index}.png"
        image_save_path = os.path.join(self.output_path_string, image_file_name)
        image.save(image_save_path)

    def render_avatar_image(self, image_path_sequence: List[str]):
        image= Image.new("RGBA", (24 , 24), self.background_color ) #A stands for Alpha channel (blank, transparency)
        for image_path in image_path_sequence:
            layer_image = Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image
    
    def generate_image_sequence(self):
        image_path_sequence = []
        for layer in self.layers:
            if layer.should_generate():
                image_path = layer.get_random_image_path()
                image_path_sequence.append(image_path) 
        return image_path_sequence
    
    def generate_avatar(self):
        print("AvatarGenerator: Generating Avatar!")
        image_path_sequence = self.generate_image_sequence()    
        print(image_path_sequence) 
        image = self.render_avatar_image(image_path_sequence) 
        #image.show() 
        self.save_image(image)

    def generate_multiple_avatars(self, n: int = 1):
        print("AvatarGenerator: Generating Avatar!")
        for i in range(n):
            image_path_sequence = self.generate_image_sequence()    
            print(image_path_sequence) 
            image = self.render_avatar_image(image_path_sequence) 
            #image.show() 
            self.save_multiple_image(image, i)