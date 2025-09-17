import os
import subprocess

def straighten_image(folder, image):
    """
    Function that will straighten the image for better LLM reading.
    Args:
        image (str): Name of the image.
        folder (str): Folder that image should be located after straightening.
    """
    # print("jestem tutaj")
    # Commands
    args = ["page-dewarp", image] # It assumes for now its all in img folder - Maybe wont change XD ****
    try:
        # Capture output can be usefull for debugging, doesn't affect working as much 
        result = subprocess.run(
            args=args,
            cwd=folder, # It assumes for now its all in img folder - Maybe wont change XD ****
            capture_output=True,
        )
        # print(result.stdout) 


    except Exception as e:
        print(f"Type {type(e)}")
        print(f"Error: {e}")
        print(subprocess.run(args=["dir"], cwd=folder, shell=True))

    
    finally:
        pass # Maybe something in the future


def straighten_img_path(folder: str, image: str) -> str:
    """
    Returns relative path of straighten image.

    Args:
        image (str): Image name
        folder (str): Folder name

    Returns relative path of straighten image
    """

    name, ext = image.split(".")
    new_name = name + "_thresh." + ext

    return os.path.join(folder, new_name) 



if __name__ == "__main__":
    straighten_image("test.png", "img")