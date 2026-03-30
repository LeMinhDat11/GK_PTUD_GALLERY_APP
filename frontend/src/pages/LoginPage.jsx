import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.username || !form.password) { setError('Please fill in all fields'); return }
    setLoading(true); setError('')
    try {
      await login(form)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.left}>
        <div style={styles.decoration}>
          <div style={styles.decGrid}>
            {Array.from({ length: 9 }).map((_, i) => (
              <div key={i} style={{ ...styles.decCell, animationDelay: `${i * 0.12}s` }} />
            ))}
          </div>
          <div style={styles.decQuote}>
            <div style={styles.quoteText}>
              "A photograph is a secret about a secret."
            </div>
            <div style={styles.quoteAuthor}>— Diane Arbus</div>
          </div>
        </div>
      </div>

      <div style={styles.right}>
        <div style={styles.formWrap}>
          <div style={styles.brand}>
            <span style={{ color: 'var(--accent)', marginRight: '0.5rem' }}>✦</span>
            <span style={styles.brandName}>Lumière</span>
          </div>

          <h1 style={styles.heading}>Welcome back</h1>
          <p style={styles.sub}>Sign in to your gallery</p>

          <form onSubmit={handleSubmit} style={styles.form}>
            <div className="form-group">
              <label className="form-label">Username</label>
              <input
                value={form.username}
                onChange={set('username')}
                placeholder="your_username"
                autoComplete="username"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                type="password"
                value={form.password}
                onChange={set('password')}
                placeholder="••••••••"
                autoComplete="current-password"
              />
            </div>

            {error && <div className="form-error">{error}</div>}

            <button
              type="submit"
              className="btn-primary"
              style={{ width: '100%', marginTop: '0.5rem' }}
              disabled={loading}
            >
              {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : 'Sign In'}
            </button>
          </form>

          <div style={styles.footer}>
            Don't have an account?{' '}
            <Link to="/register">Create one</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: {
    display: 'flex',
    minHeight: '100vh',
  },
  left: {
    flex: 1,
    background: 'var(--surface)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    overflow: 'hidden',
  },
  decoration: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '3rem',
    padding: '2rem',
  },
  decGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '8px',
    width: '240px',
  },
  decCell: {
    height: '76px',
    background: 'var(--surface2)',
    borderRadius: '4px',
    animation: 'fadeIn 0.6s ease forwards',
    opacity: 0,
  },
  decQuote: {
    textAlign: 'center',
    maxWidth: '300px',
  },
  quoteText: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.125rem',
    fontStyle: 'italic',
    color: 'var(--text-muted)',
    lineHeight: 1.6,
    marginBottom: '0.75rem',
  },
  quoteAuthor: {
    fontSize: '0.75rem',
    textTransform: 'uppercase',
    letterSpacing: '0.12em',
    color: 'var(--text-dim)',
  },
  right: {
    width: '440px',
    flexShrink: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderLeft: '1px solid var(--border)',
  },
  formWrap: {
    width: '100%',
    maxWidth: '340px',
    padding: '2rem',
    animation: 'fadeIn 0.5s ease',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '2.5rem',
  },
  brandName: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.5rem',
    fontWeight: 300,
    letterSpacing: '0.06em',
  },
  heading: {
    fontSize: '2rem',
    fontWeight: 300,
    marginBottom: '0.5rem',
  },
  sub: {
    color: 'var(--text-muted)',
    fontSize: '0.875rem',
    marginBottom: '2rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.125rem',
  },
  footer: {
    marginTop: '1.75rem',
    fontSize: '0.8125rem',
    color: 'var(--text-muted)',
    textAlign: 'center',
  },
}
