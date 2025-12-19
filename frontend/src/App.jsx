import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Haniphei.ai</h1>
      </header>
      <main>
        <div>
          <h2>Upload a document</h2>
          <input type="file" />
        </div>
        <div>
          <h2>Or paste text</h2>
          <textarea rows="10" cols="50"></textarea>
        </div>
        <button>Scan</button>
      </main>
    </div>
  );
}

export default App;
