import React, { useState, useEffect } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ActivityFeed from './pages/ActivityFeed'
import NetworkView from './pages/NetworkView'
import Analytics from './pages/Analytics'
import LivePostsFeed from './pages/LivePostsFeed'
import SourceCredibility from './pages/SourceCredibility'
import { SocketProvider } from './contexts/SocketContext'
import './App.css'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3b82f6',
    },
    secondary: {
      main: '#8b5cf6',
    },
    success: {
      main: '#10b981',
    },
    warning: {
      main: '#f59e0b',
    },
    error: {
      main: '#ef4444',
    },
    background: {
      default: '#0a0e27',
      paper: '#1a1f3a',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
})

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <SocketProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/live" element={<LivePostsFeed />} />
              <Route path="/activity" element={<ActivityFeed />} />
              <Route path="/network" element={<NetworkView />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/sources" element={<SourceCredibility />} />
            </Routes>
          </Layout>
        </Router>
      </SocketProvider>
    </ThemeProvider>
  )
}

export default App
