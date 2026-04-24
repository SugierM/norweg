import React, { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

const PhotoView = () => {
  const [images, setImages] = useState([]);
  const [selectedImg, setSelectedImg] = useState(null);

  useEffect(() => {
    invoke("get_images_list")
      .then((res) => setImages(res))
      .catch((err) => console.error(err));
  }, []);

  const handleProcess = async () => {
    if (!selectedImg) return;
    // Tutaj poleci Twój fetch do FastAPI
    console.log("Wysyłam do FastAPI:", selectedImg);
    await fetch("http://127.0.0.1:8000/api/v1/process-ocr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: selectedImg })
    });
    alert("Wysłano: " + selectedImg);
  };

  return (
    <div className="card shadow-sm p-4 border-0">
      <div className="d-flex justify-content-between mb-4 align-items-center">
        <h3 className="m-0">Podręcznik - Zdjęcia</h3>
        <button 
          className="btn btn-primary" 
          disabled={!selectedImg}
          onClick={handleProcess}
        >
          Wyodrębnij słowa z: {selectedImg || "..."}
        </button>
      </div>

      <div className="row row-cols-2 row-cols-md-4 g-3">
        {images.map((img) => (
          <div className="col" key={img.name}>
            <div 
              className={`card h-100 ${selectedImg === img.name ? 'border-primary shadow' : ''}`}
              onClick={() => setSelectedImg(img.name)}
              style={{ cursor: 'pointer', transition: 'all 0.2s' }}
            >
              <img 
                src={img.data} 
                className="card-img-top" 
                style={{ height: '180px', objectFit: 'cover' }} 
              />
              <div className={`card-footer small text-center ${selectedImg === img.name ? 'bg-primary text-white' : 'bg-light'}`}>
                {img.name}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PhotoView;