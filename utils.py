import os
import subprocess
import ollama
import json
import re

class StructureError(Exception):
    """
    Raised when the dictionary does not match the expected schema.
    {word: [{oversettelse: pl_word, betydning: meaning_in_pl}, ...], ...}
    """
    pass

def straighten_image(folder:str, image:str):
    """
    Function that will straighten the image for better LLM reading.
    Args:
        image (str): Name of the image.
        folder (str): Folder that image should be located after straightening.
    """

    # Check if needed
    if image.endswith("_thresh.png"):
        return
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


def straighten_img_path(folder_path: str, image_path: str) -> str:
    """
    Returns relative path of straighten image.

    Args:
        image (str): Image name
        folder (str): Folder name

    Returns relative path of straighten image
    """
    if image_path.endswith("_thresh.png"):
        return os.path.join(folder_path, image_path)
    name, ext = image_path.split(".")
    new_name = name + "_thresh." + ext

    return os.path.join(folder_path, new_name) 


def handle_json_response(prompt) -> dict:
    response = ollama.chat(model="gpt-oss:20b", messages=[
        {"role": "user", "content": prompt}
    ],
    keep_alive=False)
    
    # Parse data into json
    try:
        # Ensure that JSON can be parsed with some specific characters for Markdown
        clean_json = re.sub(r"^```json\s*|\s*```$", "", response["message"]["content"].strip())
        data = json.loads(clean_json)
    except Exception as e:
        print("Error during parsing to JSON. \nWiadomość:\n", response["message"]["content"])
        print(f"Error: {e}")
        return {"error": "Error occured during analyzing text."}
    
    return data


# Needed for further database creation
def validate_dict(prop: dict) -> None:
    """
    Validate that a dictionary follows the expected structure.

    Structure expected:
    {
      <word>: [
        {"oversettelse": <str>, "betydning": <str>},
        ...
      ],
      ...
    }

    Rules enforced:
    - Top-level object must be a dict.
    - Dict must not have more than 3 top-level keys.
    - Each value must be a list.
    - Each list element must be a dict.
    - Each inner dict must have both required keys:
      "oversettelse" and "betydning".
    """
    if not isinstance(prop, dict):
        raise StructureError(f"Expected dict not {type(prop)}.")

    # Can be problematic, but with LLM responses it usually 
    # indicates something went wrong.
    keys = prop.keys()
    if len(keys) > 3:
        raise StructureError("Too many keys in dictionary.")
    
    # Check for proper inner structure
    for l in prop.values():
        if not isinstance(l, list):
            raise StructureError(f"Values should be represented within a list not {type(l)}")
        
        # Check if list represent proper transaltion and meaning structure.
        for item in l:
            if not isinstance(item, dict):
                raise StructureError(f"All transaltions and meaning should be in dict not {type(item)}.")
            
            item_keys = item.keys()
            if ("oversettelse" not in item_keys) or ("betydning" not in item_keys):
                raise StructureError(f"Missing proper key pair.\nExpected: [oversettelse, betydning], given {item_keys}.") 
    return



if __name__ == "__main__":
    straighten_image("test.png", "img")