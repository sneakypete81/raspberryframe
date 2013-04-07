import os
import random
import logging

logger = logging.getLogger("Raspberry Frame")

class Provider:
    def __init__(self, width, height, cache_path, cache_size_mb):
        self.width = width
        self.height = height
        self.cache_path = cache_path
        self.cache_size_mb = cache_size_mb
        self.shuffled_photos = []
        self.current_photo_number = 0

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self._randomise()

    def get_photo_count(self):
        """Returns the number of photos available to display"""
        raise NotImplementedError("This method must be implemented in the provider class")

    def get_photo_object(self, photo_index):
        """Given a photo index, return a unique object for that photo"""
        raise NotImplementedError("This method must be implemented in the provider class")

    def get_photo_id(self, photo_object):
        """Given a photo object, return a unique ID for that photo"""
        raise NotImplementedError("This method must be implemented in the provider class")

    def get_photo_file(self, photo_object):
        """Given a photo object, return a file handle for the photo"""
        raise NotImplementedError("This method must be implemented in the provider class")

    def _randomise(self):
        self.current_photo_number = 0
        self.shuffled_photos = range(self.get_photo_count())
        random.shuffle(self.shuffled_photos)

    def get_photo_cached(self, photo_object):
        # TODO: Check hash, if there's an API for this
        photo_id = self.get_photo_id(photo_object)
        cache_file = os.path.join(self.cache_path, photo_id)

        if os.path.exists(cache_file):
            logger.info("Loading photo from cache...")
            photo_file = cache_file
        else:
            logger.info("Downloading photo...")
            # Save a copy of the photo
            photo_file = self.get_photo_file(photo_object)
            with open(cache_file, "wb") as f:
                f.write(photo_file.read())
            photo_file.seek(0)

        self.trim_cache()
        return photo_file

    def trim_cache(self):
        """ Delete photos from the cache until it's below the maximum size """
        files = [os.path.join(self.cache_path, f) for f in os.listdir(self.cache_path)]
        cache_bytes = sum([os.path.getsize(f) for f in files])
        while cache_bytes > self.cache_size_mb * 1024 * 1024:
            logger.info("Trimming cache...")
            filepath = files.pop(0)
            cache_bytes = cache_bytes - os.path.getsize(filepath)
            os.remove(filepath)

    def random_photo(self):
        photo_index = self.shuffled_photos[self.current_photo_number]
        photo_object = self.get_photo_object(photo_index)

        self.current_photo_number += 1

        # Re-randomise if necessary
        if (self.current_photo_number >= len(self.shuffled_photos) or
            self.get_photo_count != len(self.shuffled_photos)):
            self._randomise()

        return self.get_photo_cached(photo_object)