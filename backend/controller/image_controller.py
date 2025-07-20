from PIL import Image as PILImage
import io
from datetime import datetime
from models.image import UploadedImage
from werkzeug.utils import secure_filename

from middleware.image_middleware import generate_caption,get_clip_embedding ,enrich_metadata,reverse_image_search, detect_objects

def save_image(file, caption):
    filename = secure_filename(file.filename)
    content_type = file.content_type

    # Read image from memory stream
    image_stream = io.BytesIO(file.read())
    image_stream.seek(0)

    with PILImage.open(image_stream) as img:
        width, height = img.size

        caption = generate_caption(img)
        objects = detect_objects(img)  
        embedding = get_clip_embedding(img)  
        reverse = reverse_image_search(img)  
        metadata = enrich_metadata(caption, objects)  
   
     
    # Rewind stream to beginning and store binary
    image_stream.seek(0)
    image_doc = UploadedImage(
        filename=filename,
        caption=caption,
        objects_detected=objects,
        embedding=embedding,
        reverse_search=reverse,
        metadata=metadata,
        content_type=content_type,
        width=width,
        height=height,
        data=image_stream.read()
    )
    image_doc.save()
    return image_doc

def get_all_images():
    return UploadedImage.objects()

def get_image_by_id(image_id):
    return UploadedImage.objects(id=image_id).first()

def update_image_caption(image_id, new_caption):
    image = UploadedImage.objects(id=image_id).first()
    if image:
        image.caption = new_caption
        image.updated_at = datetime.utcnow()
        image.save()
    return image

def delete_image(image_id):
    image = UploadedImage.objects(id=image_id).first()
    if image:
        image.delete()
        return True
    return False
