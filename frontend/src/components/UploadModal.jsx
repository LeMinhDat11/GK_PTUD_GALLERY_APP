import { useState, useRef } from 'react'
import { photoAPI } from '../api'

export default function UploadModal({ onClose, onSuccess }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [dragging, setDragging] = useState(false)
  const fileRef = useRef()

  const handleFile = (f) => {
    if (!f) return
    if (!f.type.startsWith('image/')) { setError('Please select an image file'); return }
    if (f.size > 10 * 1024 * 1024) { setError('File must be under 10MB'); return }
    setFile(f)
    setError('')
    if (!title) setTitle(f.name.replace(/\.[^/.]+$/, ''))
    const reader = new FileReader()
    reader.onload = e => setPreview(e.target.result)
    reader.readAsDataURL(f)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleSubmit = async () => {
    if (!file) { setError('Please select an image'); return }
    if (!title.trim()) { setError('Title is required'); return }
    setLoading(true)
    setError('')
    try {
      const fd = new FormData()
      fd.append('title', title.trim())
      fd.append('description', description.trim())
      fd.append('file', file)
      const { data } = await photoAPI.upload(fd)
      onSuccess(data)
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal" style={{ maxWidth: '520px' }}>
        <div style={styles.header}>
          <h2 style={styles.title}>Upload Photo</h2>
          <button className="btn-icon" onClick={onClose} style={{ fontSize: '1.25rem' }}>×</button>
        </div>

        {/* Drop zone */}
        <div
          style={{ ...styles.dropzone, ...(dragging ? styles.dropzoneDrag : {}), ...(preview ? styles.dropzoneHasFile : {}) }}
          onClick={() => !preview && fileRef.current.click()}
          onDragOver={e => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          {preview ? (
            <div style={styles.previewWrap}>
              <img src={preview} alt="preview" style={styles.preview} />
              <button
                style={styles.changeBtn}
                onClick={e => { e.stopPropagation(); fileRef.current.click() }}
              >
                Change
              </button>
            </div>
          ) : (
            <div style={styles.dropContent}>
              <div style={styles.dropIcon}>⬆</div>
              <div style={styles.dropText}>Drop image here or <span style={{ color: 'var(--accent)' }}>browse</span></div>
              <div style={styles.dropSub}>PNG, JPG, GIF, WEBP · max 10MB</div>
            </div>
          )}
        </div>
        <input ref={fileRef} type="file" accept="image/*" hidden onChange={e => handleFile(e.target.files[0])} />

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.25rem' }}>
          <div className="form-group">
            <label className="form-label">Title *</label>
            <input
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="Photo title"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Optional description..."
              style={{ minHeight: '70px' }}
            />
          </div>
        </div>

        {error && <div className="form-error" style={{ marginTop: '0.75rem' }}>{error}</div>}

        <div style={styles.footer}>
          <button className="btn-ghost" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSubmit} disabled={loading}>
            {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : 'Upload Photo'}
          </button>
        </div>
      </div>
    </div>
  )
}

const styles = {
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '1.5rem',
  },
  title: {
    fontSize: '1.5rem',
    fontFamily: 'var(--font-serif)',
    fontWeight: 300,
  },
  dropzone: {
    border: '1px dashed var(--border-light)',
    borderRadius: 'var(--radius-lg)',
    cursor: 'pointer',
    transition: 'all var(--transition)',
    overflow: 'hidden',
    minHeight: '160px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  dropzoneDrag: {
    borderColor: 'var(--accent)',
    background: 'var(--accent-dim)',
  },
  dropzoneHasFile: {
    cursor: 'default',
    border: '1px solid var(--border)',
  },
  dropContent: {
    textAlign: 'center',
    padding: '2rem',
  },
  dropIcon: {
    fontSize: '2rem',
    color: 'var(--text-dim)',
    marginBottom: '0.75rem',
  },
  dropText: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
    marginBottom: '0.25rem',
  },
  dropSub: {
    fontSize: '0.75rem',
    color: 'var(--text-dim)',
  },
  previewWrap: {
    position: 'relative',
    width: '100%',
    maxHeight: '220px',
    overflow: 'hidden',
  },
  preview: {
    width: '100%',
    height: '220px',
    objectFit: 'cover',
    display: 'block',
  },
  changeBtn: {
    position: 'absolute',
    bottom: '0.75rem',
    right: '0.75rem',
    background: 'rgba(0,0,0,0.7)',
    color: '#fff',
    border: '1px solid rgba(255,255,255,0.2)',
    borderRadius: 'var(--radius)',
    padding: '0.35rem 0.75rem',
    fontSize: '0.75rem',
    cursor: 'pointer',
    fontFamily: 'var(--font-sans)',
    letterSpacing: '0.05em',
  },
  footer: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '0.75rem',
    marginTop: '1.5rem',
  },
}
