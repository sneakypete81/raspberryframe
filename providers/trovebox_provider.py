import urllib2
import logging
from cStringIO import StringIO
from provider import Provider
import trovebox

logger = logging.getLogger("Raspberry Frame")

class Trovebox(Provider):
    def __init__(self, *args, **kwds):
        self._trovebox = trovebox.Trovebox()
        self._photo_count = None
        Provider.__init__(self, *args, **kwds)

    def get_photo_count(self):
        """Returns the number of photos available to display"""
        # Only do an API call if we don't know what the photo count is
        if self._photo_count is None:
            self._photo_count = self._trovebox.photos.list(pageSize=1)[0].totalPages
        return self._photo_count

    def get_photo_object(self, photo_index):
        """Given a photo index, return a unique object for that photo"""
        returnSizes = "%sx%s" % (self.width, self.height)
        photo_object = self._trovebox.photos.list(pageSize=1,
                                                  page=photo_index + 1, # First page is p1
                                                  returnSizes=returnSizes)[0]
        # Keep the photo count up to date, to save API calls
        self._photo_count = photo_object.totalPages
        return photo_object

    def get_photo_id(self, photo_object):
        """Given a photo object, return a unique ID for that photo"""
        return photo_object.id

    def get_photo_file(self, photo_object):
        """Given a photo object, return a file handle for the photo"""
        url = photo_object.get_fields()["path%dx%d" % (self.width, self.height)]
        return StringIO(urllib2.urlopen(url).read())

    def get_description(self, photo_object):
        if photo_object.description:
            return photo_object.description
        else:
            return photo_object.filenameOriginal

    def get_tags(self, photo_object):
        return photo_object.tags

    def add_tag(self, photo_object, tag):
        photo_object.update(tagsAdd=tag)

    def remove_tag(self, photo_object, tag):
        photo_object.update(tagsRemove=tag)
