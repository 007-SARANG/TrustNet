import React, { useState, useEffect } from 'react'
import { Grid, Card, CardContent, Typography, Box, LinearProgress, Chip } from '@mui/material'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import WarningIcon from '@mui/icons-material/Warning'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import BugReportIcon from '@mui/icons-material/BugReport'
import { useSocket } from '../contexts/SocketContext'
import axios from 'axios'

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444']

const Dashboard = () => {
  const [stats, setStats] = useState({
    posts_analyzed: 0,
    fake_detected: 0,
    interventions: 0,
    success_rate: 0,
  })
  const [agentStatus, setAgentStatus] = useState([
    { name: 'Scout', status: 'active', processed: 0 },
    { name: 'Analyst', status: 'active', processed: 0 },
    { name: 'Investigator', status: 'active', processed: 0 },
    { name: 'Predictor', status: 'active', processed: 0 },
    { name: 'Strategist', status: 'active', processed: 0 },
    { name: 'Executor', status: 'active', processed: 0 },
  ])
  const { messages } = useSocket()

  useEffect(() => {
    // Fetch initial stats
    fetchStats()
    const interval = setInterval(fetchStats, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/metrics')
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  // Sample data for charts
  const detectionTrend = [
    { time: '00:00', fake: 12, real: 145 },
    { time: '04:00', fake: 8, real: 132 },
    { time: '08:00', fake: 23, real: 289 },
    { time: '12:00', fake: 45, real: 412 },
    { time: '16:00', fake: 67, real: 523 },
    { time: '20:00', fake: 34, real: 367 },
  ]

  const interventionTypes = [
    { name: 'Bot Throttling', value: 45 },
    { name: 'Fact-Check', value: 32 },
    { name: 'Platform Report', value: 18 },
    { name: 'Counter Narrative', value: 12 },
    { name: 'Monitor Only', value: 8 },
  ]

  const topicDistribution = [
    { name: 'Health', value: 35 },
    { name: 'Politics', value: 28 },
    { name: 'Technology', value: 15 },
    { name: 'Climate', value: 12 },
    { name: 'Other', value: 10 },
  ]

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 700 }}>
        Real-Time Dashboard
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card className="card metric-card">
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography className="metric-label">Posts Analyzed</Typography>
                  <Typography className="metric-value">{stats.posts_analyzed.toLocaleString()}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                    <Typography variant="caption" sx={{ color: '#10b981' }}>+12.5%</Typography>
                  </Box>
                </Box>
                <TrendingUpIcon sx={{ fontSize: 40, color: '#3b82f6', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="card metric-card">
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography className="metric-label">Fake Detected</Typography>
                  <Typography className="metric-value">{stats.fake_detected}</Typography>
                  <Typography variant="caption" sx={{ color: '#f59e0b' }}>
                    {((stats.fake_detected / stats.posts_analyzed) * 100).toFixed(1)}% of total
                  </Typography>
                </Box>
                <WarningIcon sx={{ fontSize: 40, color: '#f59e0b', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="card metric-card">
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography className="metric-label">Interventions</Typography>
                  <Typography className="metric-value">{stats.interventions}</Typography>
                  <Typography variant="caption" sx={{ color: '#8b5cf6' }}>
                    Active monitoring
                  </Typography>
                </Box>
                <CheckCircleIcon sx={{ fontSize: 40, color: '#8b5cf6', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card className="card metric-card">
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography className="metric-label">Success Rate</Typography>
                  <Typography className="metric-value">{(stats.success_rate * 100).toFixed(1)}%</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={stats.success_rate * 100} 
                    sx={{ mt: 1, backgroundColor: 'rgba(16, 185, 129, 0.2)' }}
                  />
                </Box>
                <BugReportIcon sx={{ fontSize: 40, color: '#10b981', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Agent Status */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Agent Status
              </Typography>
              {agentStatus.map((agent) => (
                <Box key={agent.name} className="agent-status active">
                  <Box className="pulse" />
                  <Typography sx={{ fontWeight: 600, flex: 1 }}>{agent.name} Agent</Typography>
                  <Chip label="Active" size="small" sx={{ backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981' }} />
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Recent Activity
              </Typography>
              <Box sx={{ maxHeight: 280, overflow: 'auto' }}>
                {messages.slice(0, 5).map((msg, idx) => (
                  <Box key={idx} className="activity-item">
                    <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                      {msg.type || 'Agent Update'}
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#9ca3af' }}>
                      {new Date().toLocaleTimeString()}
                    </Typography>
                  </Box>
                ))}
                {messages.length === 0 && (
                  <Typography variant="body2" sx={{ color: '#9ca3af', textAlign: 'center', py: 4 }}>
                    No recent activity
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Detection Trend (24h)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={detectionTrend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(59, 130, 246, 0.1)" />
                  <XAxis dataKey="time" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #3b82f6' }} />
                  <Legend />
                  <Line type="monotone" dataKey="fake" stroke="#ef4444" strokeWidth={2} name="Fake" />
                  <Line type="monotone" dataKey="real" stroke="#10b981" strokeWidth={2} name="Real" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Topic Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={topicDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {topicDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Intervention Types
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={interventionTypes}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(59, 130, 246, 0.1)" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #3b82f6' }} />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard
