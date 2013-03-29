import os
import urllib2
import random
from cStringIO import StringIO
import openphoto
import keys

class OpenPhotoFrame:
    def __init__(self, width, height, cache_path, cache_size_mb):
        self.openphoto = openphoto.OpenPhoto(keys.host, *keys.auth)
        self.num_photos = None
        self.width = width
        self.height = height
        self.cache_path = cache_path
        self.cache_size_mb = cache_size_mb

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self._update_num_photos()

    def _update_num_photos(self):
        self.num_photos = self.openphoto.photos.list(pageSize=1)[0].totalPages

    def get_image(self, photo):
        url = photo.get_fields()["path%dx%d" % (self.width, self.height)]
        return StringIO(urllib2.urlopen(url).read())

    def get_image_cached(self, photo):
        # TODO: Check hash, once there's an OpenPhoto API for this
        cache_file = os.path.join(self.cache_path, photo.id)
        if os.path.exists(cache_file):
            print "Loading image from cache..."
            image = cache_file
        else:
            print "Downloading image..."
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
            print "Trimming cache..."
            filepath = files.pop(0)
            cache_bytes = cache_bytes - os.path.getsize(filepath)
            os.remove(filepath)

    def random_image(self):
        page = random.randint(1, self.num_photos)
        print "Preparing image..."
        photo = self.openphoto.photos.list(pageSize=1, page=page, 
                                           returnSizes="%sx%s" % (self.width, self.height))[0]
        # Update the number of photos, if necessary
        if photo.totalPages != self.num_photos:
            self._update_num_photos()

        return self.get_image_cached(photo)
