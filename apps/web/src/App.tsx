import React, { useState, useEffect } from 'react'

interface HealthStatus {
  status: string
  service: string
  version: string
  demo_scenario: {
    equipment: string
    failure_mode: string
    primary_question: string
  }
}

interface EvalQuestion {
  id: string
  type: string
  question: string
  expected_answer_summary: string
  expected_source_document: string
  expected_page_or_region: string
  safety_notes: string
  expected_confidence_level: string
}

export default function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [evals, setEvals] = useState<EvalQuestion[]>([])
  const [seedFiles, setSeedFiles] = useState<string[]>([])
  const [uploadedFile, setUploadedFile] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  const API_BASE = import.meta.env.VITE_API_BASE || ''

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => console.error('API Health check failed:', err))

    fetch(`${API_BASE}/api/v1/seed-corpus`)
      .then((res) => res.json())
      .then((data) => setSeedFiles(data.files || []))
      .catch((err) => console.error('Failed to load seed corpus:', err))

    fetch(`${API_BASE}/api/v1/evaluations`)
      .then((res) => res.json())
      .then((data) => setEvals(data.questions || []))
      .catch((err) => console.error('Failed to load evals:', err))
  }, [])

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploadedFile(file.name)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await fetch(`${API_BASE}/api/v1/upload`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      console.log('Upload result:', data)
      // refresh seed list
      fetch(`${API_BASE}/api/v1/seed-corpus`)
        .then((r) => r.json())
        .then((d) => setSeedFiles(d.files || []))
    } catch (err) {
      console.error('Upload failed:', err)
    }
  }

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/v1/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await res.json()
      setAnswer(data)
    } catch (err) {
      console.error('Query failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Multimodal Maintenance Intelligence Agent</h1>
          <span className={`badge ${health?.status === 'ok' ? 'badge-success' : ''}`}>
            Backend: {health?.status || 'Connecting...'}
          </span>
        </div>
        <p style={{ color: '#6c757d', margin: '4px 0 0 0' }}>
          Day 1 Skeleton — Grounded Technical Troubleshooting with Citation Provenance
        </p>
      </header>

      <div className="grid">
        {/* Scenario Info */}
        <div className="card">
          <h2>Demo Scenario</h2>
          <p><strong>Equipment:</strong> {health?.demo_scenario.equipment || 'Industrial Pump Motor'}</p>
          <p><strong>Failure Mode:</strong> {health?.demo_scenario.failure_mode || 'Motor does not start after overload reset'}</p>
          <p><strong>Primary Question:</strong></p>
          <blockquote style={{ background: '#e9ecef', padding: '10px', borderRadius: '4px', fontStyle: 'italic' }}>
            "{health?.demo_scenario.primary_question || 'The motor does not start after overload reset. What should I check next?'}"
          </blockquote>
          <button
            className="btn"
            style={{ marginTop: '10px' }}
            onClick={() => setQuery(health?.demo_scenario.primary_question || '')}
          >
            Load Primary Question
          </button>
        </div>

        {/* Upload Document Placeholder */}
        <div className="card">
          <h2>Upload Maintenance Document</h2>
          <p style={{ fontSize: '14px', color: '#6c757d' }}>
            Upload PDFs, scanned procedures, wiring schematics, or table matrices (Day 1 Upload Placeholder).
          </p>
          <div className="upload-zone" onClick={() => document.getElementById('file-input')?.click()}>
            <input
              id="file-input"
              type="file"
              style={{ display: 'none' }}
              onChange={handleFileUpload}
            />
            <p style={{ margin: 0, fontWeight: 'bold' }}>
              {uploadedFile ? `Selected: ${uploadedFile}` : 'Click to select or drop manual/schematic file'}
            </p>
            <span style={{ fontSize: '12px', color: '#6c757d' }}>Supported: .pdf, .svg, .png, .md, .txt</span>
          </div>
          {uploadedFile && (
            <div style={{ marginTop: '10px', color: '#0f5132', fontSize: '14px' }}>
              ✓ Document registered for ingestion pipeline.
            </div>
          )}
        </div>
      </div>

      {/* Query Console */}
      <div className="card">
        <h2>Technician Query Console</h2>
        <form onSubmit={handleQuery} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a technical troubleshooting question..."
            style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid #ced4da' }}
          />
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Searching...' : 'Ask Assistant'}
          </button>
        </form>

        {answer && (
          <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #dee2e6' }}>
            <h3>Grounded Answer</h3>
            <p style={{ whiteSpace: 'pre-line' }}>{answer.answer_text}</p>

            {answer.citations && answer.citations.length > 0 && (
              <div style={{ marginTop: '12px' }}>
                <h4>Citations & Provenance:</h4>
                {answer.citations.map((c: any, idx: number) => (
                  <div key={idx} className="citation-tag">
                    📄 <strong>{c.document_title}</strong> (Page {c.page}) — Confidence: {(c.confidence * 100).toFixed(0)}%
                  </div>
                ))}
              </div>
            )}

            {answer.safety_warnings && answer.safety_warnings.length > 0 && (
              <div className="warning-box">
                <strong>⚠️ Safety Warnings:</strong>
                <ul style={{ margin: '4px 0 0 20px', padding: 0 }}>
                  {answer.safety_warnings.map((w: string, idx: number) => (
                    <li key={idx}>{w}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Seed Corpus & Evaluation Set Inspector */}
      <div className="grid">
        <div className="card">
          <h2>Seed Corpus Files ({seedFiles.length})</h2>
          <ul style={{ paddingLeft: '20px' }}>
            {seedFiles.map((file, idx) => (
              <li key={idx}><code>data/seed/{file}</code></li>
            ))}
          </ul>
        </div>

        <div className="card">
          <h2>Verified Evaluation Set ({evals.length})</h2>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {evals.map((eq) => (
              <div key={eq.id} style={{ marginBottom: '10px', borderBottom: '1px solid #f1f3f5', paddingBottom: '6px' }}>
                <span className={`badge ${eq.type === 'positive' ? 'badge-success' : ''}`}>
                  {eq.id} ({eq.type})
                </span>
                <div style={{ fontSize: '13px', fontWeight: 'bold', marginTop: '4px' }}>{eq.question}</div>
                <div style={{ fontSize: '12px', color: '#6c757d' }}>Source: {eq.expected_source_document} ({eq.expected_page_or_region})</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
