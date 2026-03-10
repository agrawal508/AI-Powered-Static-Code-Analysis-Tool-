import React from 'react';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import python from 'react-syntax-highlighter/dist/esm/languages/hljs/python';
import docco from 'react-syntax-highlighter/dist/esm/styles/hljs/docco';

SyntaxHighlighter.registerLanguage('python', python);

const ReportView = ({ report }) => {
    if (!report) return null;

    const { files_scanned, issues_found, issues, report_generated_at, sourceCode } = report;

    // Get line numbers containing issues
    const issueLines = issues.map(issue => issue.line);

    return (
        <div>
            <h3>Security Analysis Report</h3>
            <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
                <div style={{ padding: '10px', backgroundColor: '#e9ecef', borderRadius: '4px' }}>
                    <strong>Files Scanned:</strong> {files_scanned}
                </div>
                <div style={{ padding: '10px', backgroundColor: issues_found > 0 ? '#f8d7da' : '#d4edda', borderRadius: '4px' }}>
                    <strong>Issues Found:</strong> {issues_found}
                </div>
                <div style={{ padding: '10px', backgroundColor: '#e9ecef', borderRadius: '4px' }}>
                    <strong>Generated:</strong> {new Date(report_generated_at).toLocaleString()}
                </div>
            </div>

            {issues.length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                    <h4>Detected Vulnerabilities</h4>
                    <ul style={{ listStyleType: 'none', padding: 0 }}>
                        {issues.map((issue, index) => (
                            <li key={index} style={{ padding: '10px', borderBottom: '1px solid #dee2e6', display: 'flex', gap: '15px' }}>
                                <span style={{ fontWeight: 'bold', color: issue.severity === 'Critical' ? '#dc3545' : '#fd7e14' }}>
                                    [{issue.severity}]
                                </span>
                                <span><strong>{issue.type}</strong> at line {issue.line}</span>
                                <span style={{ color: '#6c757d', fontStyle: 'italic' }}>({issue.file}) - {issue.message || ''}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {sourceCode && (
                <div>
                    <h4>Source Code Viewer</h4>
                    <SyntaxHighlighter
                        language="python"
                        style={docco}
                        showLineNumbers={true}
                        wrapLines={true}
                        lineProps={(lineNumber) => {
                            let style = { display: "block" };
                            if (issueLines.includes(lineNumber)) {
                                style.backgroundColor = "#ffcccc";
                                style.fontWeight = "bold";
                            }
                            return { style };
                        }}
                    >
                        {sourceCode}
                    </SyntaxHighlighter>
                </div>
            )}
        </div>
    );
};

export default ReportView;
