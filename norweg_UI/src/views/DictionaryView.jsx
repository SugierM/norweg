import React from "react";
import Sidebar from "../components/Sidebar";

const DictionaryView = ({ entries, selectedWord, onSelect }) => {
  return (
    <div className="row gx-3">
      {/* SIDEBAR - Przekazujemy listę i funkcję wyboru */}
      <Sidebar 
        entries={entries} 
        selectedWord={selectedWord} 
        onSelect={onSelect} 
      />

      {/* GŁÓWNA TREŚĆ - Szczegóły słowa */}
      <main className="col-12 col-md-8 col-lg-9">
        <div className="card shadow-sm border-0">
          <div className="card-body p-4">
            {selectedWord ? (
              <>
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <nav aria-label="breadcrumb">
                      <ol className="breadcrumb mb-2">
                        <li className="breadcrumb-item">
                          <a href="#" className="text-decoration-none">Home</a>
                        </li>
                        <li className="breadcrumb-item active">
                          {selectedWord.word}
                        </li>
                      </ol>
                    </nav>
                    
                    <h1 className="display-5 fw-bold mb-0" id="norword">
                      {selectedWord.word}
                    </h1>
                    
                    <div className="fs-2 fw-bold text-primary mb-1" id="pl-translation">
                      {selectedWord.translations?.map(t => t.target_word).join(", ")}
                    </div>
                    
                    <div className="text-muted" id="en-translation">
                      English: <span className="fw-medium">{selectedWord.english_link || "—"}</span>
                    </div>
                  </div>

                  <div className="text-end">
                    <span className="badge bg-success text-uppercase px-3 py-2">
                      {selectedWord.pos}
                    </span>
                    <div className="mt-4 d-flex gap-2 justify-content-end">
                      <button className="btn btn-outline-secondary btn-sm" title="Copy">
                        <i className="fa fa-copy"></i>
                      </button>
                      <button className="btn btn-outline-secondary btn-sm" title="Speak">
                        <i className="fa fa-volume-up"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <hr className="my-4 text-muted opacity-25" />

                <section id="lemma-section">
                  <h6 className="text-muted text-uppercase small fw-bold mb-3">Same lemma</h6>
                  <div className="d-flex flex-wrap gap-2 mb-4">
                    <span className="lemma-chip border px-3 py-1 rounded-pill bg-light">
                      {selectedWord.lemma || selectedWord.word}
                    </span>
                  </div>

                  <h6 className="text-muted text-uppercase small fw-bold mb-2">Notes / metadata</h6>
                  <p className="text-muted small bg-light p-2 rounded">
                    ID: {selectedWord.id} | Lemma: {selectedWord.lemma} | Lang: {selectedWord.language_code}
                  </p>
                </section>

                <hr className="my-4 text-muted opacity-25" />

                <section>
                  <h6 className="text-muted text-uppercase small fw-bold mb-2">Context / Example</h6>
                  <p className="fst-italic text-secondary fs-5">
                    {selectedWord.example || "No example available for this entry."}
                  </p>
                </section>
              </>
            ) : (
              <div className="text-center py-5">
                <i className="fa fa-search fa-3x text-light mb-3"></i>
                <p className="text-muted">Wyszukaj słowo u góry lub wybierz z listy po lewej.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default DictionaryView;