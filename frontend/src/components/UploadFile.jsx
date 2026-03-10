import React, { useState } from 'react';
import axios from 'axios';

const UploadFile = ({ onAnalysisComplete }) => {
    const [file, setFile] = useState(null);
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError('');

        // Read file contents to display later
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => setCode(e.target.result);
            reader.readAsText(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a Python file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setError('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            // Include code in the report so we can highlight it
            const reportWithCode = {
                ...response.data,
                sourceCode: code
            };
            onAnalysisComplete(reportWithCode);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred during analysis.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h3>Upload Python Source Code</h3>
            <div style={{ marginBottom: '15px' }}>
                <input
                    type="file"
                    accept=".py"
                    onChange={handleFileChange}
                />
            </div>

            <button
                onClick={handleUpload}
                disabled={loading || !file}
                style={{
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    padding: '10px 15px',
                    borderRadius: '4px',
                    cursor: loading || !file ? 'not-allowed' : 'pointer'
                }}
            >
                {loading ? 'Analyzing...' : 'Analyze Code'}
            </button>

            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </div>
    );
};

export default UploadFile;
