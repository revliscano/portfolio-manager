import re
import os
from shutil import rmtree

from django.conf import settings
from mixer.backend.django import Mixer


def create_object(model, *, data=None, commit=True):
    if data is None:
        data = {}
    mixer = Mixer(commit=commit)
    return mixer.blend(model, **data)


def create_three_objects_of(model, common_data=None):
    mixer = Mixer()
    return mixer.cycle(count=3).blend(model, **common_data)


class ImagesEraser:
    def __init__(self, directory_name):
        self.directory = self.get_image_directory(directory_name)

    def get_image_directory(self, directory_name):
        return os.path.join(
            settings.MEDIA_ROOT,
            directory_name
        )

    def remove_images_created_for_tests(self):
        image_directory_files = self.get_files_in_image_directory()
        for image in image_directory_files:
            self.erase(image)

    def get_files_in_image_directory(self):
        return os.listdir(
            self.directory
        )

    def remove_whole_directory(self):
        rmtree(self.directory)

    def erase(self, image):
        regex_pattern_for_test_images = r"image(?:_\w+)?\.gif"
        if re.match(regex_pattern_for_test_images, image):
            os.remove(os.path.join(self.directory, image))
