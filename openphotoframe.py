import os
import urllib2
import random
import logging
from cStringIO import StringIO
import openphoto
import keys

logger = logging.getLogger("Raspberry Frame")

class OpenPhotoFrame:
    def __init__(self, width, height, cache_path, cache_size_mb):
        self.openphoto = openphoto.OpenPhoto(keys.host, *keys.auth)
        self.width = width
        self.height = height
        self.cache_path = cache_path
        self.cache_size_mb = cache_size_mb
        self.shuffled_photos = []
        self.current_photo_index = 0

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self._randomise()

    def _randomise(self):
        self.current_photo_index = 0
        num_photos = self.openphoto.photos.list(pageSize=1)[0].totalPages
        self.shuffled_photos = range(num_photos)
        random.shuffle(self.shuffled_photos)

    def get_image(self, photo):
        url = photo.get_fields()["path%dx%d" % (self.width, self.height)]
        return StringIO(urllib2.urlopen(url).read())

    def get_image_cached(self, photo):
        # TODO: Check hash, once there's an OpenPhoto API for this
        cache_file = os.path.join(self.cache_path, photo.id)
        if os.path.exists(cache_file):
            logger.info("Loading image from cache...")
            image = cache_file
        else:
            logger.info("Downloading image...")
            # Save a copy of the image
            image = self.get_image(photo)
            with open(cache_file, "wb") as f:
                f.write(image.read())
            image.seek(0)

        self.trim_cache()
        return image

    def trim_cache(self):
        """ Delete photos from the cache until it's below the maximum size """
        files = [os.path.join(self.cache_path, f) for f in os.listdir(self.cache_path)]
        cache_bytes = sum([os.path.getsize(f) for f in files])
        while cache_bytes > self.cache_size_mb * 1024 * 1024:
            logger.info("Trimming cache...")
            filepath = files.pop(0)
            cache_bytes = cache_bytes - os.path.getsize(filepath)
            os.remove(filepath)

    def random_image(self):
        page = self.shuffled_photos[self.current_photo_index]
        photo = self.openphoto.photos.list(pageSize=1, page=page,
                                           returnSizes="%sx%s" % (self.width, self.height))[0]
        self.current_photo_index += 1

        # Re-randomise if necessary
        if (self.current_photo_index >= len(self.shuffled_photos) or
            photo.totalPages != len(self.shuffled_photos)):
            self._randomise()

        return self.get_image_cached(photo)
