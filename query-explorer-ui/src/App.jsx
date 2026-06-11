import React, { useState, useEffect } from 'react';
import { Database, Folder, Table as TableIcon, Play, Loader, FileJson, UploadCloud, CheckCircle, AlertCircle, MessageSquare, Settings } from 'lucide-react';
import { TrinoService } from './services/TrinoService';
import { ClickHouseService } from './services/ClickHouseService';
import { LLMService } from './services/LLMService';
import './App.css';

const TreeNode = ({ node, level = 0, onSelectTable }) => {
  const [isOpen, setIsOpen] = useState(level === 0);
  const [children, setChildren] = useState(null);
  const [loading, setLoading] = useState(false);

  const toggleOpen = async () => {
    if (!isOpen && !children) {
      setLoading(true);
      try {
        if (node.type === 'catalog') {
          const schemas = await TrinoService.getSchemas(node.name);
          setChildren(schemas.map(s => ({ type: 'schema', name: s, catalog: node.name })));
        } else if (node.type === 'schema') {
          const tables = await TrinoService.getTables(node.catalog, node.name);
          setChildren(tables.map(t => ({ type: 'table', name: t, catalog: node.catalog, schema: node.name })));
        }
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }
    setIsOpen(!isOpen);
  };

  const handleSelect = () => {
    if (node.type === 'table') {
      onSelectTable(`${node.catalog}.${node.schema}.${node.name}`);
    } else {
      toggleOpen();
    }
  };

  return (
    <div className="tree-node">
      <div className="tree-item" onClick={handleSelect}>
        {node.type === 'catalog' && <Database size={16} />}
        {node.type === 'schema' && <Folder size={16} />}
        {node.type === 'table' && <TableIcon size={16} />}
        <span>{node.name}</span>
        {loading && <Loader size={12} className="spin" />}
      </div>
      {isOpen && children && (
        <div className="tree-children">
          {children.map((child, i) => (
            <TreeNode key={i} node={child} level={level + 1} onSelectTable={onSelectTable} />
          ))}
        </div>
      )}
    </div>
  );
};

function App() {
  const [catalogs, setCatalogs] = useState([]);
  const [query, setQuery] = useState('-- Write your federated SQL query here\n-- Example: SELECT * FROM clickhouse.default.ecommerce_sales LIMIT 10;');
  const [results, setResults] = useState({ columns: [], data: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('query'); // 'query', 'ingest', or 'chat'
  const [apiKey, setApiKey] = useState('');
  const [showSettings, setShowSettings] = useState(false);

  const loadCatalogs = () => {
    TrinoService.getCatalogs()
      .then(cats => setCatalogs(cats.map(c => ({ type: 'catalog', name: c }))))
      .catch(err => console.error("Could not fetch catalogs", err));
  };

  useEffect(() => {
    loadCatalogs();
  }, []);

  const runQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await TrinoService.executeQuery(query);
      setResults(res);
    } catch (err) {
      setError(err.message);
      setResults({ columns: [], data: [] });
    }
    setLoading(false);
  };

  const handleTableSelect = (fullTableName) => {
    setActiveTab('query');
    setQuery(`SELECT * FROM ${fullTableName} LIMIT 50;`);
  };

  const handleImportSuccess = () => {
    loadCatalogs();
  };

  return (
    <div className="app-layout">
      {/* Sidebar / Explorer */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <FileJson size={20} className="text-primary" />
          <span>Federated Explorer</span>
        </div>
        <div className="sidebar-content">
          {catalogs.map((catalog, i) => (
            <TreeNode key={i} node={catalog} onSelectTable={handleTableSelect} />
          ))}
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-area">
        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button 
            className={`tab-btn ${activeTab === 'query' ? 'active' : ''}`}
            onClick={() => setActiveTab('query')}
          >
            <Play size={14} />
            SQL Query Editor
          </button>
          <button 
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageSquare size={14} />
            AI Chat
          </button>
          <button 
            className={`tab-btn ${activeTab === 'ingest' ? 'active' : ''}`}
            onClick={() => setActiveTab('ingest')}
          >
            <UploadCloud size={14} />
            Upload S3 & ClickHouse
          </button>
          <div style={{ flex: 1 }}></div>
          <button 
            className={`tab-btn ${showSettings ? 'active' : ''}`}
            onClick={() => setShowSettings(!showSettings)}
            title="Settings"
          >
            <Settings size={14} />
          </button>
        </div>

        {showSettings && (
          <div className="settings-panel glass-panel" style={{ margin: '1rem', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <h3 style={{ marginTop: 0, marginBottom: '1rem', fontSize: '1rem' }}>Settings</h3>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>LLM API Key (OpenRouter/OpenAI compatible)</label>
              <input 
                type="password" 
                value={apiKey} 
                onChange={e => setApiKey(e.target.value)} 
                placeholder="sk-or-v1-..."
                style={{ 
                  width: '100%', 
                  padding: '0.75rem', 
                  borderRadius: '6px', 
                  border: '1px solid var(--border)',
                  background: 'var(--surface)',
                  color: 'var(--text)'
                }}
              />
            </div>
          </div>
        )}

        {activeTab === 'query' ? (
          <div className="tab-content query-tab">
            {/* Editor */}
            <section className="editor-section">
              <div className="editor-header">
                <span style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-secondary)' }}>SQL Editor</span>
                <button className="btn btn-primary" onClick={runQuery} disabled={loading}>
                  {loading ? <Loader size={16} className="spin" /> : <Play size={16} />}
                  Run Query
                </button>
              </div>
              <textarea
                className="sql-textarea"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                spellCheck="false"
              />
            </section>

            {/* Results */}
            <section className="results-section">
              <div className="results-header">
                <span>Results {results.data.length > 0 && `(${results.data.length} rows)`}</span>
              </div>
              <div className="table-container">
                {error ? (
                  <div className="error-message">Error: {error}</div>
                ) : (
                  <table className="results-table">
                    <thead>
                      <tr>
                        {results.columns.map((col, i) => (
                          <th key={i}>{col.name}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {results.data.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                          {row.map((cell, cellIndex) => (
                            <td key={cellIndex}>
                              {cell === null ? <em style={{opacity: 0.5}}>null</em> : String(cell)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
                {loading && (
                  <div className="loading-overlay">
                    <Loader size={32} className="spin" />
                    <span>Executing Query...</span>
                  </div>
                )}
                {!loading && !error && results.data.length === 0 && results.columns.length === 0 && (
                  <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                    Run a query to see results here.
                  </div>
                )}
              </div>
            </section>
          </div>
        ) : activeTab === 'chat' ? (
          <div className="tab-content chat-tab" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <ChatPanel apiKey={apiKey} />
          </div>
        ) : (
          <div className="tab-content ingest-tab">
            <IngestPanel onImportSuccess={handleImportSuccess} />
          </div>
        )}
      </main>
    </div>
  );
}

// IngestPanel Component
const IngestPanel = ({ onImportSuccess }) => {
  const [tableName, setTableName] = useState('');
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState({ step: 'idle', message: '' }); // 'idle', 'uploading', 'importing', 'success', 'error'
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    
    if (selectedFile && !tableName) {
      const suggestedName = selectedFile.name
        .split('.')[0]
        .toLowerCase()
        .replace(/[^a-z0-9]/g, '_');
      setTableName(suggestedName);
    }
  };

  const handleUploadAndImport = async (e) => {
    e.preventDefault();
    if (!file || !tableName.trim()) return;

    const validTableName = /^[a-z_][a-z0-9_]*$/.test(tableName);
    if (!validTableName) {
      setError("Table name must contain only lowercase letters, numbers, and underscores, and start with a letter.");
      return;
    }

    setStatus({ step: 'uploading', message: 'Uploading file to S3 (MinIO)...' });
    setError(null);

    try {
      // 1. Upload to MinIO
      const s3FileName = `${Date.now()}_${file.name.replace(/\s+/g, '_')}`;
      const uploadUrl = `/minio/warehouse/uploads/${s3FileName}`;
      
      const uploadResponse = await fetch(uploadUrl, {
        method: 'PUT',
        body: file
      });

      if (!uploadResponse.ok) {
        throw new Error(`S3 upload failed: ${uploadResponse.statusText}`);
      }

      // 2. Import into ClickHouse
      setStatus({ step: 'importing', message: 'Creating table and importing data into ClickHouse...' });

      const internalS3Url = `http://minio:9000/warehouse/uploads/${s3FileName}`;
      
      const createTableQuery = `
        CREATE TABLE default.${tableName}
        ENGINE = MergeTree()
        ORDER BY tuple()
        AS SELECT * FROM s3('${internalS3Url}', 'minioadmin', 'minioadmin', 'CSVWithNames')
      `;

      await ClickHouseService.executeQuery(createTableQuery);

      setStatus({ step: 'success', message: `Table "${tableName}" was successfully imported into ClickHouse!` });
      setTableName('');
      setFile(null);
      
      const fileInput = document.getElementById('csv-file-input');
      if (fileInput) fileInput.value = '';

      if (onImportSuccess) {
        onImportSuccess();
      }
    } catch (err) {
      console.error(err);
      setStatus({ step: 'error', message: '' });
      setError(err.message || 'An error occurred during import.');
    }
  };

  return (
    <div className="ingest-panel glass-panel">
      <h2>Import CSV Data to S3 & ClickHouse</h2>
      <p className="panel-desc">
        Upload any CSV file to your S3 storage (MinIO) and instantly register it as a new, fast table in ClickHouse. The table schema and column data types are automatically inferred from the CSV structure.
      </p>

      <form onSubmit={handleUploadAndImport} className="ingest-form">
        <div className="form-group">
          <label htmlFor="table-name-input">Table Name</label>
          <input
            id="table-name-input"
            type="text"
            placeholder="e.g. customer_transactions"
            value={tableName}
            onChange={(e) => setTableName(e.target.value.toLowerCase())}
            required
            disabled={status.step === 'uploading' || status.step === 'importing'}
          />
          <small className="help-text">Use only lowercase letters, numbers, and underscores.</small>
        </div>

        <div className="form-group">
          <label>Select CSV File</label>
          <div 
            className={`file-dropzone ${file ? 'has-file' : ''} ${status.step === 'uploading' || status.step === 'importing' ? 'disabled' : ''}`}
            onClick={() => {
              if (status.step !== 'uploading' && status.step !== 'importing') {
                document.getElementById('csv-file-input').click();
              }
            }}
          >
            <UploadCloud size={28} className="dropzone-icon" />
            {file ? (
              <div className="file-info">
                <span className="file-name">{file.name}</span>
                <span className="file-size">{(file.size / 1024).toFixed(2)} KB</span>
              </div>
            ) : (
              <div className="dropzone-text">
                <span className="dropzone-title">Choose CSV file or drag & drop here</span>
                <span className="dropzone-sub">Supported format: .csv</span>
              </div>
            )}
            <input
              id="csv-file-input"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              required
              style={{ display: 'none' }}
              disabled={status.step === 'uploading' || status.step === 'importing'}
            />
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary btn-large"
          disabled={!file || !tableName || status.step === 'uploading' || status.step === 'importing'}
        >
          {(status.step === 'uploading' || status.step === 'importing') ? (
            <>
              <Loader size={18} className="spin" />
              Processing...
            </>
          ) : (
            <>
              <UploadCloud size={18} />
              Upload & Import
            </>
          )}
        </button>
      </form>

      {(status.step === 'uploading' || status.step === 'importing') && (
        <div className="status-alert alert-info">
          <Loader size={20} className="spin" />
          <span>{status.message}</span>
        </div>
      )}

      {status.step === 'success' && (
        <div className="status-alert alert-success">
          <CheckCircle size={20} />
          <span>{status.message}</span>
        </div>
      )}

      {error && (
        <div className="status-alert alert-danger">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};

const ChatPanel = ({ apiKey }) => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I can help you query your Trino data. Ask me anything about your tables.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || !apiKey) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      // 1. Get Schema Context
      const catalogs = await TrinoService.getCatalogs();
      let schemaContext = '';
      for (const cat of catalogs.slice(0, 2)) {
        schemaContext += `Catalog: ${cat}\n`;
        const schemas = await TrinoService.getSchemas(cat);
        for (const sch of schemas.slice(0, 5)) {
          const tables = await TrinoService.getTables(cat, sch);
          schemaContext += `  Schema: ${sch}\n    Tables: ${tables.join(', ')}\n`;
        }
      }

      // 2. Generate Response
      const responseText = await LLMService.generateSQL(apiKey, schemaContext, userMessage);
      
      const sqlMatch = responseText.match(/```sql\n([\s\S]*?)```/i) || responseText.match(/```\n([\s\S]*?)```/i);
      
      if (sqlMatch) {
        const sql = sqlMatch[1].trim();
        const textBeforeOrAfter = responseText.replace(sqlMatch[0], '').trim();
        
        let content = textBeforeOrAfter ? `${textBeforeOrAfter}\n\n` : '';
        content += `Executing generated SQL:\n\`\`\`sql\n${sql}\n\`\`\``;
        
        setMessages(prev => [...prev, { role: 'assistant', content }]);

        // 3. Execute SQL
        const res = await TrinoService.executeQuery(sql);
        
        // 4. Render Results
        setMessages(prev => [...prev, { role: 'assistant', content: 'Query Results:', results: res }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: responseText }]);
      }

    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div className="chat-messages" style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`} style={{ display: 'flex', gap: '1rem', alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '80%' }}>
            {msg.role === 'assistant' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0 }}>
                <MessageSquare size={16} />
              </div>
            )}
            <div className="message-content" style={{ background: msg.role === 'user' ? 'var(--primary)' : 'var(--surface)', color: msg.role === 'user' ? 'white' : 'var(--text)', padding: '1rem', borderRadius: '12px', border: msg.role === 'assistant' ? '1px solid var(--border)' : 'none', display: 'flex', flexDirection: 'column' }}>
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.5, fontSize: '0.95rem' }}>
                {msg.content}
              </div>
              {msg.results && (
                <div className="table-container" style={{ marginTop: '1rem', maxHeight: '300px', background: 'var(--background)' }}>
                  <table className="results-table">
                    <thead>
                      <tr>
                        {msg.results.columns.map((col, idx) => (
                          <th key={idx}>{col.name}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {msg.results.data.slice(0, 50).map((row, rIdx) => (
                        <tr key={rIdx}>
                          {row.map((cell, cIdx) => (
                            <td key={cIdx}>{cell === null ? <em>null</em> : String(cell)}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
            {msg.role === 'user' && (
              <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)', flexShrink: 0 }}>
                You
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="chat-message assistant" style={{ display: 'flex', gap: '1rem', alignSelf: 'flex-start', maxWidth: '80%' }}>
             <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0 }}>
                <MessageSquare size={16} />
              </div>
            <div className="message-content" style={{ background: 'var(--surface)', color: 'var(--text)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Loader size={16} className="spin" />
              <span>Thinking and executing...</span>
            </div>
          </div>
        )}
      </div>
      <form className="chat-input-area" onSubmit={handleSend} style={{ padding: '1.5rem', borderTop: '1px solid var(--border)', display: 'flex', gap: '1rem', background: 'var(--surface)' }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={apiKey ? "Ask a question about your data..." : "Please set your API Key in Settings first"}
          disabled={!apiKey || loading}
          style={{ flex: 1, padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)', background: 'var(--background)', color: 'var(--text)', fontSize: '1rem' }}
        />
        <button type="submit" disabled={!apiKey || !input.trim() || loading} className="btn btn-primary" style={{ padding: '0 1.5rem' }}>
          <Play size={20} />
        </button>
      </form>
    </div>
  );
};

export default App;
