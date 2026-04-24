import React from "react";
const Sidebar = ({ entries, selectedWord, onSelect }) => (
  <aside className="col-12 col-md-4 col-lg-3">
    <div className="card shadow-sm border-0 mb-3">
      <div className="card-header bg-white fw-bold border-bottom">Entries</div>
      <div className="list-group list-group-flush" style={{maxHeight: '70vh', overflowY: 'auto'}}>
        {entries.map((item, idx) => (
          <button 
            key={idx} 
            className={`list-group-item list-group-item-action ${selectedWord?.id === item.id ? 'active' : ''}`}
            onClick={() => onSelect(item)}
          >
            <div className="fw-bold">{item.word}</div>
            <small className="text-muted">{item.translations?.[0]?.target_word}</small>
          </button>
        ))}
      </div>
    </div>
  </aside>
);
export default Sidebar;