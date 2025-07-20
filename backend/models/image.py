from mongoengine import Document, StringField, BinaryField, IntField, DateTimeField, ListField, DictField
from datetime import datetime

class UploadedImage(Document):
    filename = StringField(required=True)
    caption = StringField()
    objects_detected = ListField(StringField())  # For object detection
    embedding = ListField()                      # For semantic embedding
    reverse_search = DictField()                 # For reverse image search results
    metadata = DictField()                       # For metadata enrichment
    content_type = StringField()
    width = IntField()
    height = IntField()
    data = BinaryField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
