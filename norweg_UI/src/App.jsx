import React, { useState, useEffect } from "react";
// Importy komponentów i widoków
import Navbar from "./components/Navbar";
import DictionaryView from "./views/DictionaryView";
import PhotoView from "./views/PhotoView";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000/api/v1";

function App() {
  // 1. STANY APLIKACJI
  const [view, setView] = useState("dictionary"); // Sterowanie widokiem
  const [searchTerm, setSearchTerm] = useState(""); // Tekst w wyszukiwarce
  const [selectedWord, setSelectedWord] = useState(null); // Aktualnie wyświetlane słowo
  const [history, setHistory] = useState([]); // Lista "Entries" po lewej
  const [isLoading, setIsLoading] = useState(false);

  // 2. LOGIKA WYSZUKIWANIA (Komunikacja z FastAPI)
  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!searchTerm.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/translate/${searchTerm.trim()}`);
      if (!response.ok) throw new Error("Nie znaleziono słowa");
      
      const data = await response.json();
      
      // Ustawiamy wynik jako aktualnie wybrane słowo
      setSelectedWord(data);
      
      // Dodajemy do historii (Entries) - usuwamy duplikaty i bierzemy 15 ostatnich
      setHistory(prev => {
        const filtered = prev.filter(item => item.word !== data.word);
        const newHistory = [data, ...filtered].slice(0, 15);
        // Zapisujemy w pamięci podręcznej przeglądarki (opcjonalnie)
        localStorage.setItem("word_history", JSON.stringify(newHistory));
        return newHistory;
      });
      
      setSearchTerm(""); // Czyścimy pasek wyszukiwania po znalezieniu
    } catch (error) {
      console.error("Błąd wyszukiwania:", error);
      alert("Nie udało się połączyć z API lub słowo nie istnieje.");
    } finally {
      setIsLoading(false);
    }
  };

  // Ładowanie historii z localStorage przy starcie aplikacji
  useEffect(() => {
    const saved = localStorage.getItem("word_history");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setHistory(parsed);
        if (parsed.length > 0) setSelectedWord(parsed[0]);
      } catch (e) {
        console.error("Błąd ładowania historii");
      }
    }
  }, []);

  return (
    <div className="bg-light min-vh-100">
      {/* NAGŁÓWEK - Wspólny dla całej aplikacji */}
      <Navbar 
        view={view} 
        setView={setView} 
        searchTerm={searchTerm} 
        setSearchTerm={setSearchTerm}
        onSearch={handleSearch}
        isLoading={isLoading}
      />

      <div className="container-fluid mt-4 pb-5">
        {/* DYNAMICZNA TREŚĆ - Zmienia się zależnie od stanu 'view' */}
        
        {view === "dictionary" && (
          <DictionaryView 
            entries={history} 
            selectedWord={selectedWord} 
            onSelect={setSelectedWord} 
          />
        )}
        
        {view === "photos" && (
          <PhotoView 
            apiBase={API_BASE}
          />
        )}

        {/* Tutaj możesz w przyszłości dodać kolejne widoki, np. Ustawienia */}
        {view === "settings" && (
          <div className="card p-4">
            <h3>Ustawienia</h3>
            <p>Tu będziesz mógł skonfigurować np. adres serwera FastAPI.</p>
          </div>
        )}
      </div>

      {/* OPCJONALNIE: Stopka lub status bar */}
      <footer className="fixed-bottom bg-white border-top p-2 text-center text-muted small">
        FastAPI Status: <span className="text-success">Connected</span> | Mode: Gemini 3 Flash Powered
      </footer>
    </div>
  );
}

export default App;