import React from 'react'
import { motion } from 'framer-motion'
import { Brain, Zap } from 'lucide-react'

const Header = ({ docCount }) => {
  return (
    <header style={styles.header}>
      <div style={styles.inner}>
        <motion.div
          style={styles.brand}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div style={styles.iconWrap}>
            <Brain size={20} color="#00d4ff" />
            <div style={styles.iconPulse} />
          </div>
          <div>
            <h1 style={styles.title}>Docutrust<span style={styles.titleAccent}>_AI</span></h1>
            <p style={styles.subtitle}>RAG-Powered Document Intelligence</p>
          </div>
        </motion.div>

        <motion.div
          style={styles.stats}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div style={styles.statBadge}>
            <Zap size={12} color="#00e5a0" />
            <span style={styles.statLabel}>Groq LLM</span>
          </div>
          <div style={styles.divider} />
          <div style={styles.statBadge}>
            <span style={styles.docCount}>{docCount}</span>
            <span style={styles.statLabel}>docs indexed</span>
          </div>
        </motion.div>
      </div>
    </header>
  )
}

const styles = {
  header: {
    borderBottom: '1px solid #1e2d3d',
    background: 'rgba(8, 12, 16, 0.9)',
    backdropFilter: 'blur(20px)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  inner: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0 2rem',
    height: '64px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    gap: '14px',
  },
  iconWrap: {
    width: '40px',
    height: '40px',
    background: 'rgba(0, 212, 255, 0.08)',
    border: '1px solid rgba(0, 212, 255, 0.2)',
    borderRadius: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  iconPulse: {
    position: 'absolute',
    inset: '-2px',
    borderRadius: '12px',
    border: '1px solid rgba(0, 212, 255, 0.3)',
    animation: 'pulse 2s ease-in-out infinite',
  },
  title: {
    fontFamily: "'Syne', sans-serif",
    fontSize: '17px',
    fontWeight: 800,
    letterSpacing: '0.12em',
    color: '#e2e8f0',
    lineHeight: 1,
  },
  titleAccent: {
    color: '#00d4ff',
  },
  subtitle: {
    fontFamily: "'DM Mono', monospace",
    fontSize: '10px',
    color: '#4a5568',
    letterSpacing: '0.05em',
    marginTop: '3px',
  },
  stats: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  statBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    padding: '5px 12px',
    background: 'rgba(255,255,255,0.03)',
    border: '1px solid #1e2d3d',
    borderRadius: '20px',
  },
  statLabel: {
    fontFamily: "'DM Mono', monospace",
    fontSize: '11px',
    color: '#94a3b8',
    letterSpacing: '0.05em',
  },
  docCount: {
    fontFamily: "'Syne', sans-serif",
    fontSize: '14px',
    fontWeight: 700,
    color: '#00d4ff',
  },
  divider: {
    width: '1px',
    height: '20px',
    background: '#1e2d3d',
  },
}

export default Header
