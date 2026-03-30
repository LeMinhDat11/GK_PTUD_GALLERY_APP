import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { photoAPI } from '../api'

export default function PhotoCard({ photo, onDelete, onUpdate }) {
  const navigate = useNavigate()
  const [hover, setHover] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [editing, setEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(photo.title)
  const [saving, setSaving] = useState(false)

  const handleDelete = async (e) => {
    e.stopPropagation()
    if (!confirm(`Delete "${photo.title}"?`)) return
    setDeleting(true)
    try {
      await photoAPI.delete(photo.id)
      onDelete(photo.id)
    } catch {
      setDeleting(false)
    }
  }

  const handleEditSave = async (e) => {
    e.stopPropagation()
    if (!editTitle.trim()) return
    setSaving(true)
    try {
      const { data } = await photoAPI.update(photo.id, { title: editTitle.trim() })
      onUpdate(data)
      setEditing(false)
    } catch {
      // ignore
    } finally {
      setSaving(false)
    }
  }

  const formatDate = (iso) => new Date(iso).toLocaleDateString('vi-VN', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  })

  return (
    <div
      style={{ ...styles.card, ...(hover ? styles.cardHover : {}) }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => { setHover(false); setEditing(false); setEditTitle(photo.title) }}
      onClick={() => !editing && navigate(`/photo/${photo.id}`)}
    >
      {/* Image */}
      <div style={styles.imgWrap}>
        <img
          src={photo.image_url}
          alt={photo.title}
          style={styles.img}
          loading="lazy"
        />
        {/* Overlay on hover */}
        <div style={{ ...styles.overlay, opacity: hover ? 1 : 0 }}>
          <button
            style={styles.deleteBtn}
            onClick={handleDelete}
            disabled={deleting}
            title="Delete"
          >
            {deleting ? '...' : '✕'}
          </button>
        </div>
      </div>

      {/* Info */}
      <div style={styles.info}>
        {editing ? (
          <div style={styles.editRow} onClick={e => e.stopPropagation()}>
            <input
              value={editTitle}
              onChange={e => setEditTitle(e.target.value)}
              style={styles.editInput}
              onKeyDown={e => {
                if (e.key === 'Enter') handleEditSave(e)
                if (e.key === 'Escape') { setEditing(false); setEditTitle(photo.title) }
              }}
              autoFocus
            />
            <button style={styles.saveBtn} onClick={handleEditSave} disabled={saving}>✓</button>
          </div>
        ) : (
          <div style={styles.titleRow}>
            <span style={styles.title} title={photo.title}>{photo.title}</span>
            {hover && (
              <button
                style={styles.editBtn}
                onClick={e => { e.stopPropagation(); setEditing(true) }}
                title="Edit title"
              >
                ✎
              </button>
            )}
          </div>
        )}
        <div style={styles.date}>{formatDate(photo.uploaded_at)}</div>
      </div>
    </div>
  )
}

const styles = {
  card: {
    background: 'var(--surface)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius-lg)',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'all 0.25s ease',
    animation: 'fadeIn 0.4s ease forwards',
  },
  cardHover: {
    border: '1px solid var(--border-light)',
    transform: 'translateY(-2px)',
    boxShadow: '0 12px 40px rgba(0,0,0,0.4)',
  },
  imgWrap: {
    position: 'relative',
    aspectRatio: '4/3',
    overflow: 'hidden',
    background: 'var(--surface2)',
  },
  img: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    display: 'block',
    transition: 'transform 0.4s ease',
  },
  overlay: {
    position: 'absolute',
    inset: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'flex-start',
    justifyContent: 'flex-end',
    padding: '0.75rem',
    transition: 'opacity 0.2s ease',
  },
  deleteBtn: {
    background: 'rgba(192,90,90,0.85)',
    border: 'none',
    color: '#fff',
    width: '28px',
    height: '28px',
    borderRadius: '50%',
    cursor: 'pointer',
    fontSize: '0.75rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'var(--font-sans)',
    transition: 'background var(--transition)',
  },
  info: {
    padding: '0.875rem 1rem 1rem',
  },
  titleRow: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '0.5rem',
  },
  title: {
    fontSize: '0.875rem',
    color: 'var(--text)',
    fontWeight: 400,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    flex: 1,
  },
  editBtn: {
    background: 'none',
    border: 'none',
    color: 'var(--text-muted)',
    cursor: 'pointer',
    fontSize: '0.875rem',
    padding: '0 0.125rem',
    flexShrink: 0,
    fontFamily: 'var(--font-sans)',
  },
  editRow: {
    display: 'flex',
    gap: '0.375rem',
    alignItems: 'center',
  },
  editInput: {
    flex: 1,
    padding: '0.3rem 0.5rem',
    fontSize: '0.8125rem',
    height: '28px',
  },
  saveBtn: {
    background: 'var(--accent)',
    border: 'none',
    color: '#000',
    width: '28px',
    height: '28px',
    borderRadius: 'var(--radius)',
    cursor: 'pointer',
    fontSize: '0.875rem',
    flexShrink: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'var(--font-sans)',
  },
  date: {
    fontSize: '0.6875rem',
    color: 'var(--text-dim)',
    marginTop: '0.25rem',
    letterSpacing: '0.05em',
  },
}
