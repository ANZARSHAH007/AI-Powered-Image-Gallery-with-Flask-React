import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./Image.css";

const API_URL = `http://${window.location.hostname}:3000/api/images`;

function formatKeyValue(obj) {
  if (!obj || typeof obj !== "object") return "—";
  return (
    <ul className="kv-list">
      {Object.entries(obj).map(([k, v]) => (
        <li key={k}>
          <span className="kv-key">{k}:</span>{" "}
          <span className="kv-value">{typeof v === "object" ? JSON.stringify(v) : String(v)}</span>
        </li>
      ))}
    </ul>
  );
}

export default function ImageCrud() {
  const [images, setImages] = useState([]);
  const [file, setFile] = useState(null);
  const [newCaption, setNewCaption] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const fileInputRef = useRef();

  const fetchImages = async () => {
    try {
      const res = await axios.get(API_URL + "/");
      setImages(res.data);
    } catch (err) {
      console.error("Error fetching images:", err);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append("image", file);
    try {
      await axios.post(API_URL + "/upload", formData);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
      await fetchImages();
    } catch (err) {
      alert("Upload failed!");
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      await fetchImages();
    } catch (err) {
      alert("Delete failed!");
      console.error(err);
    }
  };

  const handleUpdate = async (id) => {
    try {
      await axios.put(`${API_URL}/${id}`, { caption: newCaption });
      setNewCaption("");
      setSelectedId(null);
      await fetchImages();
    } catch (err) {
      alert("Update failed!");
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h2>🖼️ AI Image Gallery</h2>
      <form className="upload-form" onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          onChange={e => setFile(e.target.files[0])}
          ref={fileInputRef}
        />
        <button type="submit">Upload</button>
      </form>
      <div className="gallery">
        {images.map(img => (
          <div key={img.id} className="card">
            <img
              src={`${API_URL}/${img.id}/raw`}
              alt={img.caption}
              className="image"
              onError={e => (e.target.style.display = "none")}
            />
            <div className="info">
              <div className="filename"> {img.filename}</div>
              <div className="caption"> <span className="meta-label">Caption:</span>{img.caption}</div>
              <div className="meta-row">
                <span className="meta-label">Objects:</span>
                <span>{img.objects_detected && img.objects_detected.length ? img.objects_detected.join(", ") : "—"}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">Embedding:</span>
                <span>
                  {Array.isArray(img.embedding) && img.embedding.length
                    ? img.embedding.slice(0, 5).map((v, i) => <span key={i}>{v.toFixed(2)}{i < 4 ? ", " : "..."}</span>)
                    : "—"}
                </span>
              </div>
              <div className="meta-row">
                <span className="meta-label">Reverse Search:</span>
                {formatKeyValue(img.reverse_search)}
              </div>
              <div className="meta-row">
                <span className="meta-label">Metadata:</span>
                {formatKeyValue(img.metadata)}
              </div>
              <div className="meta-row">
                <span className="meta-label">Size:</span>
                <span>{img.width} x {img.height}</span>
              </div>
              <div className="meta-row">
                <span className="meta-label">Created:</span>
                <span>{new Date(img.created_at).toLocaleString()}</span>
              </div>
              <div className="actions">
                <button onClick={() => handleDelete(img.id)}>Delete</button>
                <button onClick={() => setSelectedId(img.id)}>Edit Caption</button>
              </div>
              {selectedId === img.id && (
                <div className="edit-caption">
                  <input
                    type="text"
                    value={newCaption}
                    onChange={e => setNewCaption(e.target.value)}
                    placeholder="New caption"
                  />
                  <button onClick={() => handleUpdate(img.id)}>Save</button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}