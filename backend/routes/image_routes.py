from flask import Blueprint, request, jsonify, send_file
from controllers.image_controller import (
    save_image, get_all_images, get_image_by_id,
    update_image_caption, delete_image
)
import io

image_bp = Blueprint('images', __name__)

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400

    image = save_image(file, None)  # No caption from user
    return jsonify({
        'id': str(image.id),
        'filename': image.filename,
        'caption': image.caption,
        'objects_detected': image.objects_detected,
        'embedding': image.embedding,
        'reverse_search': image.reverse_search,
        'metadata': image.metadata,
        'width': image.width,
        'height': image.height,
        'created_at': image.created_at
    }), 201

@image_bp.route('/', methods=['GET'])
def list_images():
    images = get_all_images()
    return jsonify([
        {
            'id': str(img.id),
            'filename': img.filename,
            'caption': img.caption,
            'objects_detected': img.objects_detected,
            'embedding': img.embedding,
            'reverse_search': img.reverse_search,
            'metadata': img.metadata,
            'width': img.width,
            'height': img.height,
            'created_at': img.created_at
        }
        for img in images
    ])

@image_bp.route('/<string:image_id>', methods=['GET'])
def get_image(image_id):
    img = get_image_by_id(image_id)
    if not img:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify({
        'id': str(img.id),
        'filename': img.filename,
        'caption': img.caption,
        'objects_detected': img.objects_detected,
        'embedding': img.embedding,
        'reverse_search': img.reverse_search,
        'metadata': img.metadata,
        'width': img.width,
        'height': img.height,
        'created_at': img.created_at
    })

@image_bp.route('/<string:image_id>', methods=['PUT'])
def update_caption(image_id):
    new_caption = request.json.get('caption')
    img = update_image_caption(image_id, new_caption)
    if not img:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify({'message': 'Caption updated', 'caption': img.caption})

@image_bp.route('/<string:image_id>', methods=['DELETE'])
def remove_image(image_id):
    success = delete_image(image_id)
    if not success:
        return jsonify({'error': 'Image not found'}), 404
    return jsonify({'message': 'Image deleted'})

@image_bp.route('/<string:image_id>/raw', methods=['GET'])
def get_image_raw(image_id):
    img = get_image_by_id(image_id)
    if not img:
        return jsonify({'error': 'Image not found'}), 404
    return send_file(
        io.BytesIO(img.data),
        mimetype=img.content_type,
        as_attachment=False,
        download_name=img.filename
    )
