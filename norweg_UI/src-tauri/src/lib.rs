use std::fs;
use std::path::Path;
use base64::{Engine as _, engine::general_purpose};
// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

#[tauri::command]
fn get_images_list() -> Vec<serde_json::Value> {
    // Ścieżka względem norweg_UI/src-tauri
    let path = Path::new("../../img");
    let mut images = Vec::new();

    if let Ok(entries) = fs::read_dir(path) {
        for entry in entries {
            if let Ok(entry) = entry {
                let file_path = entry.path();
                let name = entry.file_name().to_string_lossy().into_owned();
                let lower_name = name.to_lowercase();

                if lower_name.ends_with(".png") || lower_name.ends_with(".jpg") || lower_name.ends_with(".jpeg") {
                    if let Ok(bytes) = fs::read(&file_path) {
                        let b64 = general_purpose::STANDARD.encode(bytes);
                        let mime = if lower_name.ends_with(".png") { "image/png" } else { "image/jpeg" };
                        images.push(serde_json::json!({
                            "name": name,
                            "data": format!("data:{};base64,{}", mime, b64)
                        }));
                    }
                }
            }
        }
    }
    images
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // TA LINIA JEST KLUCZOWA - Rejestruje funkcję w systemie Tauri
        .invoke_handler(tauri::generate_handler![get_images_list]) 
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}