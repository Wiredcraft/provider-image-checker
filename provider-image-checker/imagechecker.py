from config import get_config
from imagelist import ImageList
import json, os.path

class ImageChecker(object):
    """
    Downloads a list of images and image id's for all providers,
    and writes it to a JSON file.
    """
    def __init__(self):
        self.config = get_config()
        self.providers = self.config.get_providers()
        self.image_lists = self.get_image_lists()

    """
    Loads the image lists for each provider.
    """
    def get_image_lists(self):
        image_lists = {}
        for provider in self.providers:
            image_lists[provider] = ImageList(provider).images
        return image_lists

    """ 
    Writes all image names and id's to a json file, 
    sorted by provider.
    """
    def write_to_file(self):
        filename = self.config.get_filename()
        out = open(filename, 'w')
        json_string = json.dumps(self.image_lists, indent=4)
        out.write(json_string)
        out.close()

ImageWatcher().write_to_file()