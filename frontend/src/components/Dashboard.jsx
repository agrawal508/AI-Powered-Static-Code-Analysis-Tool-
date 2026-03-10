import React, { useState } from 'react';
import UploadFile from './UploadFile';
import ReportView from './ReportView';

const Dashboard = () => {
    const [report, setReport] = useState(null);

    const handleAnalysisComplete = (data) => {
        setReport(data);
    };

    return (
        <div style={{ textAlign: 'left', marginTop: '20px' }}>
            <h2>Dashboard</h2>
            <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
                <div style={{ flex: 1, backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                    <UploadFile onAnalysisComplete={handleAnalysisComplete} />
                </div>
                {report && (
                    <div style={{ flex: 2, backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                        <ReportView report={report} />
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
