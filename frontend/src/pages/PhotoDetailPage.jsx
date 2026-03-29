import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { photoAPI } from '../api'

export default function PhotoDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [photo, setPhoto] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [editForm, setEditForm] = useState({ title: '', description: '' })
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    photoAPI.get(id)
      .then(({ data }) => {
        setPhoto(data)
        setEditForm({ title: data.title, description: data.description || '' })
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id])

  const handleSave = async () => {
    if (!editForm.title.trim()) { setError('Title is required'); return }
    setSaving(true); setError('')
    try {
      const { data } = await photoAPI.update(id, editForm)
      setPhoto(data)
      setEditForm({ title: data.title, description: data.description || '' })
      setEditing(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Update failed')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm(`Delete "${photo.title}"? This cannot be undone.`)) return
    setDeleting(true)
    try {
      await photoAPI.delete(id)
      navigate('/')
    } catch {
      setDeleting(false)
    }
  }

  const formatDate = (iso) => new Date(iso).toLocaleDateString('vi-VN', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <span className="spinner" style={{ width: 32, height: 32 }} />
    </div>
  )

  if (!photo) return null

  return (
    <div style={styles.page}>
      {/* Header */}
      <header style={styles.header}>
        <button className="btn-icon" onClick={() => navigate('/')} style={styles.backBtn} title="Back to gallery">
          ← Back
        </button>
        <div style={styles.headerActions}>
          {!editing ? (
            <>
              <button className="btn-ghost" onClick={() => setEditing(true)}>Edit</button>
              <button className="btn-danger" onClick={handleDelete} disabled={deleting}>
                {deleting ? 'Deleting…' : 'Delete'}
              </button>
            </>
          ) : (
            <>
              <button className="btn-ghost" onClick={() => { setEditing(false); setError(''); setEditForm({ title: photo.title, description: photo.description || '' }) }}>
                Cancel
              </button>
              <button className="btn-primary" onClick={handleSave} disabled={saving}>
                {saving ? <span className="spinner" style={{ width: 14, height: 14 }} /> : 'Save'}
              </button>
            </>
          )}
        </div>
      </header>

      {/* Content */}
      <div style={styles.content}>
        {/* Image panel */}
        <div style={styles.imagePanel}>
          <div style={styles.imageWrap}>
            <img src={photo.image_url} alt={photo.title} style={styles.image} />
          </div>
        </div>

        {/* Info panel */}
        <div style={styles.infoPanel}>
          <div style={styles.infoInner}>
            {editing ? (
              <div style={styles.editSection}>
                <div style={styles.editLabel}>Editing</div>
                <div className="form-group" style={{ marginTop: '1rem' }}>
                  <label className="form-label">Title</label>
                  <input
                    value={editForm.title}
                    onChange={e => setEditForm(f => ({ ...f, title: e.target.value }))}
                    placeholder="Photo title"
                    autoFocus
                  />
                </div>
                <div className="form-group" style={{ marginTop: '1rem' }}>
                  <label className="form-label">Description</label>
                  <textarea
                    value={editForm.description}
                    onChange={e => setEditForm(f => ({ ...f, description: e.target.value }))}
                    placeholder="Add a description..."
                    style={{ minHeight: '120px' }}
                  />
                </div>
                {error && <div className="form-error" style={{ marginTop: '0.75rem' }}>{error}</div>}
              </div>
            ) : (
              <>
                <h1 style={styles.title}>{photo.title}</h1>
                {photo.description && (
                  <p style={styles.description}>{photo.description}</p>
                )}
              </>
            )}

            <div style={styles.divider} />

            {/* Meta */}
            <div style={styles.meta}>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Uploaded</span>
                <span style={styles.metaValue}>{formatDate(photo.uploaded_at)}</span>
              </div>
              <div style={styles.metaItem}>
                <span style={styles.metaLabel}>Photo ID</span>
                <span style={styles.metaValue}>#{photo.id}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: 'var(--bg)',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '1rem 2rem',
    borderBottom: '1px solid var(--border)',
    background: 'rgba(10,10,10,0.92)',
    backdropFilter: 'blur(12px)',
    position: 'sticky',
    top: 0,
    zIndex: 10,
  },
  backBtn: {
    color: 'var(--text-muted)',
    cursor: 'pointer',
    background: 'none',
    border: 'none',
    fontSize: '0.875rem',
    letterSpacing: '0.04em',
    fontFamily: 'var(--font-sans)',
    padding: '0.5rem 0',
    transition: 'color var(--transition)',
  },
  headerActions: {
    display: 'flex',
    gap: '0.75rem',
  },
  content: {
    flex: 1,
    display: 'flex',
    maxHeight: 'calc(100vh - 61px)',
  },
  imagePanel: {
    flex: 1,
    background: '#050505',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '2rem',
    overflow: 'hidden',
  },
  imageWrap: {
    maxWidth: '100%',
    maxHeight: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    maxWidth: '100%',
    maxHeight: 'calc(100vh - 130px)',
    objectFit: 'contain',
    borderRadius: '4px',
    animation: 'fadeIn 0.4s ease',
    boxShadow: '0 20px 60px rgba(0,0,0,0.6)',
  },
  infoPanel: {
    width: '320px',
    flexShrink: 0,
    borderLeft: '1px solid var(--border)',
    overflowY: 'auto',
  },
  infoInner: {
    padding: '2rem 1.75rem',
    animation: 'fadeIn 0.4s ease',
  },
  editSection: {},
  editLabel: {
    fontSize: '0.6875rem',
    textTransform: 'uppercase',
    letterSpacing: '0.12em',
    color: 'var(--accent)',
  },
  title: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.75rem',
    fontWeight: 300,
    lineHeight: 1.3,
    color: 'var(--text)',
    marginBottom: '1rem',
  },
  description: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
    lineHeight: 1.7,
  },
  divider: {
    height: '1px',
    background: 'var(--border)',
    margin: '1.75rem 0',
  },
  meta: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  metaItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem',
  },
  metaLabel: {
    fontSize: '0.6875rem',
    textTransform: 'uppercase',
    letterSpacing: '0.1em',
    color: 'var(--text-dim)',
  },
  metaValue: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
  },
}
