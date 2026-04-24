import React from "react";

const Navbar = ({ view, setView, onSearch, searchTerm, setSearchTerm }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm sticky-top px-3">
      <div className="container-fluid">
        <span className="navbar-brand fw-bold cursor-pointer" onClick={() => setView("dictionary")}>
          Nor→Pol
        </span>
        
        <div className="d-flex gap-2 ms-3">
          <button 
            className={`btn btn-sm ${view === 'dictionary' ? 'btn-primary' : 'btn-light'}`}
            onClick={() => setView("dictionary")}
          >Słownik</button>
          <button 
            className={`btn btn-sm ${view === 'photos' ? 'btn-primary' : 'btn-light'}`}
            onClick={() => setView("photos")}
          >Zdjęcia</button>
        </div>

        <form className="d-flex mx-auto flex-grow-1 mx-4" style={{maxWidth: '500px'}} onSubmit={onSearch}>
          <input 
            className="form-control" 
            placeholder="Szukaj słowa..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </form>

        <button className="btn btn-sm btn-outline-secondary">Ustawienia</button>
      </div>
    </nav>
  );
};

export default Navbar;