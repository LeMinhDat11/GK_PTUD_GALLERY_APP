import { useState, useEffect, useCallback } from 'react'
import { photoAPI } from '../api'
import Navbar from '../components/Navbar'
import PhotoCard from '../components/PhotoCard'
import UploadModal from '../components/UploadModal'
import { useAuth } from '../context/AuthContext'

export default function GalleryPage() {
  const { user } = useAuth()
  const [photos, setPhotos] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')
  const [showUpload, setShowUpload] = useState(false)
  const [view, setView] = useState('grid') // 'grid' | 'large'

  const fetchPhotos = useCallback(async (q = '') => {
    setLoading(true)
    try {
      const { data } = await photoAPI.list(q)
      setPhotos(data)
    } catch {
      // silent
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchPhotos() }, [fetchPhotos])

  // Debounce search
  useEffect(() => {
    const t = setTimeout(() => {
      setSearch(searchInput)
      fetchPhotos(searchInput)
    }, 350)
    return () => clearTimeout(t)
  }, [searchInput])

  const handleUploadSuccess = (photo) => {
    setPhotos(prev => [photo, ...prev])
  }

  const handleDelete = (id) => {
    setPhotos(prev => prev.filter(p => p.id !== id))
  }

  const handleUpdate = (updated) => {
    setPhotos(prev => prev.map(p => p.id === updated.id ? updated : p))
  }

  const isEmpty = !loading && photos.length === 0

  return (
    <div style={styles.page}>
      <Navbar onUploadClick={() => setShowUpload(true)} />

      <main style={styles.main}>
        {/* Stats bar */}
        <div style={styles.statsBar}>
          <div style={styles.statsLeft}>
            <span style={styles.greeting}>
              {greeting()}, <span style={{ color: 'var(--accent)' }}>{user?.username}</span>
            </span>
            {!loading && (
              <span style={styles.count}>
                {photos.length} {photos.length === 1 ? 'photo' : 'photos'}
                {search && ` · "${search}"`}
              </span>
            )}
          </div>
          <div style={styles.statsRight}>
            {/* Search */}
            <div style={styles.searchWrap}>
              <span style={styles.searchIcon}>⌕</span>
              <input
                value={searchInput}
                onChange={e => setSearchInput(e.target.value)}
                placeholder="Search by name..."
                style={styles.searchInput}
              />
              {searchInput && (
                <button style={styles.clearBtn} onClick={() => setSearchInput('')}>×</button>
              )}
            </div>
            {/* View toggle */}
            <div style={styles.viewToggle}>
              <button
                style={{ ...styles.viewBtn, ...(view === 'grid' ? styles.viewBtnActive : {}) }}
                onClick={() => setView('grid')}
                title="Grid view"
              >⊞</button>
              <button
                style={{ ...styles.viewBtn, ...(view === 'large' ? styles.viewBtnActive : {}) }}
                onClick={() => setView('large')}
                title="Large view"
              >⊟</button>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div style={styles.divider} />

        {/* Content */}
        {loading ? (
          <div style={styles.center}>
            <span className="spinner" style={{ width: 28, height: 28 }} />
          </div>
        ) : isEmpty ? (
          <div style={styles.empty}>
            {search ? (
              <>
                <div style={styles.emptyIcon}>◎</div>
                <div style={styles.emptyTitle}>No results for "{search}"</div>
                <div style={styles.emptySub}>Try a different search term</div>
                <button className="btn-ghost" style={{ marginTop: '1.5rem' }} onClick={() => setSearchInput('')}>
                  Clear search
                </button>
              </>
            ) : (
              <>
                <div style={styles.emptyIcon}>✦</div>
                <div style={styles.emptyTitle}>Your gallery is empty</div>
                <div style={styles.emptySub}>Upload your first photo to get started</div>
                <button className="btn-primary" style={{ marginTop: '1.5rem' }} onClick={() => setShowUpload(true)}>
                  Upload Photo
                </button>
              </>
            )}
          </div>
        ) : (
          <div style={view === 'grid' ? styles.grid : styles.gridLarge}>
            {photos.map((photo, i) => (
              <div key={photo.id} style={{ animationDelay: `${Math.min(i * 0.04, 0.4)}s` }}>
                <PhotoCard photo={photo} onDelete={handleDelete} onUpdate={handleUpdate} />
              </div>
            ))}
          </div>
        )}
      </main>

      {showUpload && (
        <UploadModal
          onClose={() => setShowUpload(false)}
          onSuccess={handleUploadSuccess}
        />
      )}
    </div>
  )
}

function greeting() {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 18) return 'Good afternoon'
  return 'Good evening'
}

const styles = {
  page: { minHeight: '100vh', display: 'flex', flexDirection: 'column' },
  main: {
    flex: 1,
    maxWidth: '1400px',
    margin: '0 auto',
    width: '100%',
    padding: '2.5rem 2rem 4rem',
  },
  statsBar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    flexWrap: 'wrap',
    gap: '1rem',
  },
  statsLeft: {
    display: 'flex',
    alignItems: 'baseline',
    gap: '1.25rem',
  },
  greeting: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.75rem',
    fontWeight: 300,
  },
  count: {
    fontSize: '0.8125rem',
    color: 'var(--text-dim)',
    letterSpacing: '0.04em',
  },
  statsRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
  },
  searchWrap: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  searchIcon: {
    position: 'absolute',
    left: '0.75rem',
    color: 'var(--text-dim)',
    fontSize: '1rem',
    pointerEvents: 'none',
    lineHeight: 1,
  },
  searchInput: {
    width: '220px',
    paddingLeft: '2rem',
    paddingRight: '2rem',
    height: '36px',
    fontSize: '0.8125rem',
    background: 'var(--surface)',
    border: '1px solid var(--border)',
  },
  clearBtn: {
    position: 'absolute',
    right: '0.5rem',
    background: 'none',
    border: 'none',
    color: 'var(--text-dim)',
    cursor: 'pointer',
    fontSize: '1rem',
    lineHeight: 1,
    padding: '0.125rem',
    fontFamily: 'var(--font-sans)',
  },
  viewToggle: {
    display: 'flex',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    overflow: 'hidden',
  },
  viewBtn: {
    background: 'var(--surface)',
    border: 'none',
    color: 'var(--text-muted)',
    padding: '0.375rem 0.625rem',
    cursor: 'pointer',
    fontSize: '1rem',
    transition: 'all var(--transition)',
    fontFamily: 'var(--font-sans)',
  },
  viewBtnActive: {
    background: 'var(--surface2)',
    color: 'var(--text)',
  },
  divider: {
    height: '1px',
    background: 'var(--border)',
    margin: '1.5rem 0 2rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
    gap: '1.25rem',
  },
  gridLarge: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
    gap: '1.5rem',
  },
  center: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '40vh',
  },
  empty: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '40vh',
    textAlign: 'center',
  },
  emptyIcon: {
    fontSize: '2.5rem',
    color: 'var(--text-dim)',
    marginBottom: '1.25rem',
  },
  emptyTitle: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.5rem',
    fontWeight: 300,
    color: 'var(--text-muted)',
    marginBottom: '0.5rem',
  },
  emptySub: {
    fontSize: '0.875rem',
    color: 'var(--text-dim)',
  },
}
