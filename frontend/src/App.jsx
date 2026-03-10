import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>AI-Powered Static Code Analysis Tool</h1>
            </header>
            <main>
                <Dashboard />
            </main>
        </div>
    );
}

export default App;
