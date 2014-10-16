#!/usr/bin/python

from config import get_config
from imagelist import ImageList
import json
import os.path
import datetime

class ImageChecker(object):
    """
    Downloads a list of images and image id's for all providers,
    and writes it to a JSON file.
    """
    def __init__(self):
        self.config = get_config()
        self.providers = self.config.get_providers()
        self.image_lists = self.get_image_lists()
        self.old_image_lists = self.get_old_image_lists()

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
        out = open(filename, 'w')
        json_string = json.dumps(self.image_lists, indent=4)
        out.write(json_string)
        out.close()

    def write_diff_to_file(self):
        """
        Writes the difference between the current list of images and 
        the previous list to a file, in case any changes have been detected.
        The file is a JSON file formatted as follows: 
        provider-name: {deleted: [image-id list], added: [image-id list], modified: [image-id list]}
        for each provider.
        The file will be saved in the directory specified in config.json as
        diff_directory.
        """
        diff = self.get_diff()
        if diff:
            filename_suffix = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            filename = "diff_" + filename_suffix + ".txt"
            filepath = os.path.join(self.config.get_diff_directory(), filename)
            out = open(filepath, 'w')
            json_string = json.dumps(diff, indent=4)
            out.write(json_string)
            out.close()    

    def get_old_image_lists(self):
        filename = self.config.get_filename()
        if not os.path.isfile(filename):
            return None
        f = open(filename)
        old_image_lists = json.load(f)
        f.close()        
        return old_image_lists

    def get_diff(self):
        """
        Get the difference between the current list of images and
        the previous list in the form of a dictionary.
        """
        if not self.old_image_lists:
            return None
        result = {}
        for provider in self.providers:
            provider_diff = self.get_provider_diff(provider)
            if provider_diff:
                result[provider] = provider_diff
        return result

    def get_provider_diff(self, provider):
        """
        Gets the difference between the current list of images and 
        the previous list for a single provider.
        """
        if not provider in self.old_image_lists or not provider in self.image_lists: 
            #This is a config diff, ignore
            return None 
        old_image_list = self.old_image_lists[provider]
        new_image_list = self.image_lists[provider]
        diff = {}
        deleted = self.list_deleted_images(old_image_list, new_image_list)
        added = self.list_added_images(old_image_list, new_image_list)
        modified = self.list_modified_images(old_image_list, new_image_list)
        if deleted:
            diff['deleted'] = deleted
        if added:
            diff['added'] = added
        if modified:
            diff['modified'] = modified
        return diff

    def list_deleted_images(self, old_image_list, new_image_list):
        result = []
        for image in old_image_list:
            if not image in new_image_list:
                result.append(image)
        return result

    def list_added_images(self, old_image_list, new_image_list):
        result = []
        for image in new_image_list:
            if not image in old_image_list:
                result.append(image)
        return result

    def list_modified_images(self, old_image_list, new_image_list):
        result = []
        for image in old_image_list:
            if image in new_image_list:
                if old_image_list[image] != new_image_list[image]:
                    result.append(image)
        return result


def main():
    imagechecker = ImageChecker()
    imagechecker.write_diff_to_file()
    imagechecker.write_to_file()


if __name__ == "__main__":
    main()