from avatar_generator import AvatarGenerator

def generate_avatar():
    generator = AvatarGenerator("./images")
    #generator.generate_avatar()
    generator.generate_multiple_avatars(10)

if __name__ == "__main__":
    generate_avatar()
    
