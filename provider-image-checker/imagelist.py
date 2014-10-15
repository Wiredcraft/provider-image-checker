from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from config import get_config
import re

class ImageList(object):
    """
    Downloads a list of images from the selected provider and
    stores the filtered image list in a dictionary.
    """
    def __init__(self, provider):
        self.config = get_config()
        self.provider = provider
        self.images = self.get_filtered_image_list()

    """
    Downloads a list of all images from the provider
    """
    def get_image_list(self):
        provider = self.provider
        config = self.config
        cls = get_driver(provider)
        user_id = config.get_client_id(provider)
        key = config.get_api_key(provider)
        if user_id:
            driver = cls(user_id, key)
        else:
            driver = cls(key)
        return driver.list_images()

    """
    Downloads a list of all images from the provider,
    then filters them based on the regexes defined for 
    this provider in the configuration file.
    """
    def get_filtered_image_list(self):
        image_list = self.get_image_list()
        provider = self.provider
        images = {}
        for f in self.config.get_filters(provider):
            filtered_images = self._filter_list(image_list, f)
            for image in filtered_images:
                images[image.id] = image.name
        return images        

    def _filter_list(self, image_list, regex_string):
        """
        Filter a list of images
        """
        regex = re.compile(regex_string)
        return [image for image in image_list if regex.match(image.name)]




    
