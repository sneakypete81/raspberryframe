import urllib2
import random
from cStringIO import StringIO
import openphoto
import keys

class OpenPhotoFrame:
    def __init__(self, width, height):
        self.openphoto = openphoto.OpenPhoto(keys.host, *keys.auth)
        self.num_photos = None
        self.width = width
        self.height = height

        self._update_num_photos()

    def _update_num_photos(self):
        self.num_photos = self.openphoto.photos.list(pageSize=1)[0].totalPages

    def get_image(self, photo):
        url = photo.get_fields()["path%dx%d" % (self.width, self.height)]
        return StringIO(urllib2.urlopen(url).read())

    def random_image(self):
        page = random.randint(1, self.num_photos)
        print "Preparing image..."
        photo = self.openphoto.photos.list(pageSize=1, page=page, 
                                           returnSizes="%sx%s" % (self.width, self.height))[0]
        # Update the number of photos, if necessary
        if photo.totalPages != self.num_photos:
            self._update_num_photos()

        print "Loading image..."
        return self.get_image(photo)
