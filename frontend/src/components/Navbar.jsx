import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar({ onUploadClick }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header style={styles.header}>
      <div style={styles.inner}>
        {/* Logo */}
        <div style={styles.logo} onClick={() => navigate('/')}>
          <span style={styles.logoIcon}>✦</span>
          <span style={styles.logoText}>Lumière</span>
        </div>

        {/* Center tagline */}
        <div style={styles.tagline}>Personal Gallery</div>

        {/* Right actions */}
        <div style={styles.actions}>
          <button className="btn-primary" onClick={onUploadClick} style={styles.uploadBtn}>
            + Upload
          </button>
          <div style={styles.userMenu} onClick={() => setMenuOpen(p => !p)}>
            <div style={styles.avatar}>
              {user?.username?.[0]?.toUpperCase()}
            </div>
            {menuOpen && (
              <div style={styles.dropdown}>
                <div style={styles.dropdownUser}>
                  <div style={styles.dropdownName}>{user?.username}</div>
                  <div style={styles.dropdownEmail}>{user?.email}</div>
                </div>
                <div style={styles.dropdownDivider} />
                <button style={styles.dropdownItem} onClick={handleLogout}>
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

const styles = {
  header: {
    position: 'sticky',
    top: 0,
    zIndex: 50,
    background: 'rgba(10,10,10,0.92)',
    backdropFilter: 'blur(12px)',
    borderBottom: '1px solid var(--border)',
  },
  inner: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0 2rem',
    height: '60px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    cursor: 'pointer',
    userSelect: 'none',
  },
  logoIcon: {
    color: 'var(--accent)',
    fontSize: '0.875rem',
  },
  logoText: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.375rem',
    fontWeight: 300,
    letterSpacing: '0.06em',
    color: 'var(--text)',
  },
  tagline: {
    position: 'absolute',
    left: '50%',
    transform: 'translateX(-50%)',
    fontSize: '0.6875rem',
    textTransform: 'uppercase',
    letterSpacing: '0.18em',
    color: 'var(--text-dim)',
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  uploadBtn: {
    padding: '0.5rem 1.25rem',
    fontSize: '0.75rem',
  },
  userMenu: {
    position: 'relative',
    cursor: 'pointer',
  },
  avatar: {
    width: '32px',
    height: '32px',
    borderRadius: '50%',
    background: 'var(--accent-dim)',
    border: '1px solid var(--accent)',
    color: 'var(--accent)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '0.75rem',
    fontWeight: 500,
    letterSpacing: '0.05em',
  },
  dropdown: {
    position: 'absolute',
    top: 'calc(100% + 0.75rem)',
    right: 0,
    background: 'var(--surface)',
    border: '1px solid var(--border-light)',
    borderRadius: 'var(--radius-lg)',
    minWidth: '200px',
    overflow: 'hidden',
    boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
  },
  dropdownUser: {
    padding: '1rem',
  },
  dropdownName: {
    fontSize: '0.875rem',
    color: 'var(--text)',
    fontWeight: 400,
  },
  dropdownEmail: {
    fontSize: '0.75rem',
    color: 'var(--text-muted)',
    marginTop: '0.125rem',
  },
  dropdownDivider: {
    height: '1px',
    background: 'var(--border)',
  },
  dropdownItem: {
    display: 'block',
    width: '100%',
    padding: '0.75rem 1rem',
    background: 'none',
    border: 'none',
    color: 'var(--danger)',
    textAlign: 'left',
    fontSize: '0.8125rem',
    cursor: 'pointer',
    transition: 'background var(--transition)',
    fontFamily: 'var(--font-sans)',
    letterSpacing: '0.02em',
  },
}
