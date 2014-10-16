#!/usr/bin/python

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

    def get_image_lists(self):
        """
        Loads the image lists for each provider.
        """
        image_lists = {}
        for provider in self.providers:
            image_lists[provider] = ImageList(provider).images
        return image_lists

    def write_to_file(self):
        """ 
        Writes all image names and id's to a json file, 
        sorted by provider.
        """
        filename = self.config.get_filename()
        out = open(os.path.join(os.path.dirname(__file__), filename), 'w')
        json_string = json.dumps(self.image_lists, indent=4)
        out.write(json_string)
        out.close()

def main():
    ImageChecker().write_to_file()

if __name__ == "__main__":
    main()