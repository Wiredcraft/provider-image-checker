provider-image-checker
======================

Check images offered by various cloud providers and detect changes.

How to use
============

Make sure that Libcloud is installed
```bash
pip install apache-libcloud
```
Run imagechecker.py manually or add a cron job to run the script at regular intervals. When the script is run, it will download a list of images as specified in the file config.json. If the script has been run previously, it will then compare the new list to the previous one. If any changes have been detected, those changes will be saved to a timestamped diff file. The following changes are recorded in the diff file together with the image id's:
- *added:* The image been added to the provider since last time the script was run.
- *deleted:* The image has been deleted.
- *modified:* The image id still exists, but the image name has changed.

The diff file will be stored in the directory specified in config.json as *diff_directory*.

### Adding a provider

To add a provider to check for images, edit config.json to add the provider name as it appears in the list at https://libcloud.readthedocs.org/en/latest/apidocs/libcloud.compute.html?highlight=provider#libcloud.compute.providers.Provider.ABIQUO. Under each provider name you must also provide the following fields:
- *api_key*: Your api key from the specified provider.
- *client_id:* Your client id. Some providers do not use a client id. In that case use an empty string for this field.
- *filters:* A list of regular expressions to filter out the desired images.

### Additional options

*file_directory:* Change this field in config.json to specify where the downloaded image list wil be saved. The list is saved in JSON format, in a file named *images.json*.










