import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.username || !form.email || !form.password) { setError('All fields are required'); return }
    if (form.password.length < 6) { setError('Password must be at least 6 characters'); return }
    if (form.password !== form.confirm) { setError('Passwords do not match'); return }
    setLoading(true); setError('')
    try {
      await register({ username: form.username, email: form.email, password: form.password })
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.left}>
        <div style={styles.decoration}>
          <div style={styles.bigLetter}>L</div>
          <div style={styles.decLines}>
            {['Your photos.', 'Your stories.', 'Your gallery.'].map((t, i) => (
              <div key={i} style={{ ...styles.decLine, animationDelay: `${i * 0.15}s` }}>{t}</div>
            ))}
          </div>
        </div>
      </div>

      <div style={styles.right}>
        <div style={styles.formWrap}>
          <div style={styles.brand}>
            <span style={{ color: 'var(--accent)', marginRight: '0.5rem' }}>✦</span>
            <span style={styles.brandName}>Lumière</span>
          </div>

          <h1 style={styles.heading}>Create account</h1>
          <p style={styles.sub}>Build your personal gallery</p>

          <form onSubmit={handleSubmit} style={styles.form}>
            <div className="form-group">
              <label className="form-label">Username</label>
              <input value={form.username} onChange={set('username')} placeholder="your_username" autoComplete="username" />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input type="email" value={form.email} onChange={set('email')} placeholder="you@example.com" autoComplete="email" />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input type="password" value={form.password} onChange={set('password')} placeholder="Min. 6 characters" autoComplete="new-password" />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm Password</label>
              <input type="password" value={form.confirm} onChange={set('confirm')} placeholder="••••••••" autoComplete="new-password" />
            </div>

            {error && <div className="form-error">{error}</div>}

            <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '0.5rem' }} disabled={loading}>
              {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : 'Create Account'}
            </button>
          </form>

          <div style={styles.footer}>
            Already have an account?{' '}
            <Link to="/login">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: { display: 'flex', minHeight: '100vh' },
  left: {
    flex: 1,
    background: 'var(--surface)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    position: 'relative',
  },
  decoration: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '2.5rem',
  },
  bigLetter: {
    fontFamily: 'var(--font-serif)',
    fontSize: 'clamp(8rem, 18vw, 16rem)',
    fontWeight: 300,
    color: 'var(--border-light)',
    lineHeight: 1,
    userSelect: 'none',
    letterSpacing: '-0.04em',
  },
  decLines: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    textAlign: 'center',
  },
  decLine: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.25rem',
    fontStyle: 'italic',
    color: 'var(--text-muted)',
    animation: 'fadeIn 0.6s ease forwards',
    opacity: 0,
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
  brand: { display: 'flex', alignItems: 'center', marginBottom: '2.5rem' },
  brandName: {
    fontFamily: 'var(--font-serif)',
    fontSize: '1.5rem',
    fontWeight: 300,
    letterSpacing: '0.06em',
  },
  heading: { fontSize: '2rem', fontWeight: 300, marginBottom: '0.5rem' },
  sub: { color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '2rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  footer: { marginTop: '1.75rem', fontSize: '0.8125rem', color: 'var(--text-muted)', textAlign: 'center' },
}
