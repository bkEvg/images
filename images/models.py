import os
from django.conf import settings
from django.db import models
from PIL import Image as p_image
import requests
import io
from django.core.exceptions import ValidationError


class Image(models.Model):
    """" Image model. """
    name = models.CharField(max_length=300, blank=True)
    url = models.URLField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    width = models.IntegerField(default=128)
    height = models.IntegerField(default=128)

    def __str__(self):
        """" Str representation. """
        return self.name


    def download_image(self):
        request = requests.get(str(self.url))
        # if url is accessible we download image
        if request.status_code == 200:
            image_name = str(self.url).split('/')[-1]
            if not self.name:
                self.name = image_name
            path = os.path.join(settings.MEDIA_ROOT, f'{image_name}')
            with open(f"{path}", 'wb') as f:
                f.write(request.content)

    def clean_name(self, data):
        """ Function that cleans image name out of paths """
        # if '/' in name this means that this is absolute path
        if '/' in data:
            # all we do is just split them and get last
            name = data.split('/')[-1]
            name = name.split('.')
            return {
                'name': name[0], 
                'format': name[-1]
            }
        else:
            # if we do not have it this means name already good to go
            name = data.split('.')
            return {
                'name': name[0], 
                'format': name[-1]
            }

    def resize_image(self, full_name):
        """ Resize image with Pillow """
        image = p_image.open(os.path.join(settings.MEDIA_ROOT, f'{full_name}')).resize((self.width, self.height))
        return image

    def save_converted_image(self, path_of_converted, child):
        """ Just saves converted image to db """
        converted_image, created = ConvertedImage.objects.get_or_create(image=path_of_converted, parent=child)

    def convert_image(self, name, format):
        full_name = name + '.' + format
        name_of_converted = name + f'__{self.width}x{self.height}.' + format
        path_of_converted = os.path.join(settings.MEDIA_ROOT, f'{name_of_converted}')
        # resize image
        image = p_image.open(os.path.join(settings.MEDIA_ROOT, f'{full_name}')).resize((self.width, self.height))
        # convert Image to byte arr because can not save Image type to ImageField
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=format if format != 'jpg' else 'jpeg')  # this shit is not working with jpg too lazy to figure it out
        img_byte_arr = img_byte_arr.getvalue()
        with open(f'{path_of_converted}', 'wb') as f:
            f.write(img_byte_arr)
        image = Image.objects.get(pk=self.pk)
        # save converted image to db
        self.save_converted_image(path_of_converted, image)


    def get_image(self):
        """ Different choices of uploading images """
        if self.url and self.picture:
            """ If both given """
            url_name = self.clean_name(self.url)['name']
            picture_name = self.clean_name(str(self.picture))['name']
            # if user added the same image to picture field and url field we only upload image from url, they are the same
            if url_name == picture_name:
                name = url_name
                format = self.clean_name(self.url)['format']
                self.convert_image(name, format)
            # but if names are different we resize both
            else:
                # resize image from url
                name = self.clean_name(self.url)['name']
                format = self.clean_name(self.url)['format']
                self.convert_image(name, format)
                # resize image from ImageField
                name = self.clean_name(str(self.picture))['name']
                format = self.clean_name(str(self.picture))['format']
                self.convert_image(name, format)

        elif self.url and not self.picture:
            """if only url field fiven"""
            self.download_image()

            # отделяем путь к картинке от имени, и имя отделяем от расширения чтобы добавить в название размеры
            name = self.clean_name(self.url)['name']
            format = self.clean_name(self.url)['format']
            # convert image and save to db
            self.convert_image(name, format)

        elif self.picture and not self.url:
            """ If only ImageField given """
            name = self.clean_name(str(self.picture))['name']
            format = self.clean_name(str(self.picture))['format']
            self.convert_image(name, format)

        elif not self.picture and not self.url:
            """ If nothing given """
            pass
    
    def save(self, *args, **kwargs):
        """" Save method """
        # set name as image has
        if self.url:
            self.name = str(self.url).split('/')[-1]
        elif self.picture:
            self.name = str(str(self.picture)).split('/')[-1]
        if self.url or (self.url and self.picture) or self.picture:
            super(Image, self).save(*args, **kwargs)
            self.get_image()


class ConvertedImage(models.Model):
    """ Model for converted images """
    image = models.ImageField()
    parent = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='child', null=True, blank=True, default=None)

    def __str__(self):
        return f'Converted image of {self.parent.name}'