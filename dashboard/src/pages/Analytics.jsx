import React from 'react'
import { Grid, Card, CardContent, Typography, Box } from '@mui/material'
import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const Analytics = () => {
  // Sample data
  const performanceData = [
    { date: 'Mon', accuracy: 68, precision: 72, recall: 65 },
    { date: 'Tue', accuracy: 70, precision: 73, recall: 67 },
    { date: 'Wed', accuracy: 69, precision: 71, recall: 68 },
    { date: 'Thu', accuracy: 71, precision: 74, recall: 69 },
    { date: 'Fri', accuracy: 72, precision: 75, recall: 70 },
    { date: 'Sat', accuracy: 73, precision: 76, recall: 71 },
    { date: 'Sun', accuracy: 74, precision: 77, recall: 72 },
  ]

  const interventionSuccess = [
    { type: 'Throttle Bots', success: 92 },
    { type: 'Fact-Check', success: 88 },
    { type: 'Platform Report', success: 65 },
    { type: 'Counter Narrative', success: 95 },
    { type: 'Alert Influencers', success: 78 },
  ]

  const processingTime = [
    { agent: 'Scout', time: 50 },
    { agent: 'Analyst', time: 150 },
    { agent: 'Investigator', time: 100 },
    { agent: 'Predictor', time: 200 },
    { agent: 'Strategist', time: 100 },
    { agent: 'Executor', time: 250 },
  ]

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 700 }}>
        Analytics & Performance
      </Typography>

      <Grid container spacing={3}>
        {/* Model Performance */}
        <Grid item xs={12}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Model Performance Trends
              </Typography>
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(59, 130, 246, 0.1)" />
                  <XAxis dataKey="date" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" domain={[60, 80]} />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #3b82f6' }} />
                  <Legend />
                  <Line type="monotone" dataKey="accuracy" stroke="#3b82f6" strokeWidth={2} name="Accuracy %" />
                  <Line type="monotone" dataKey="precision" stroke="#8b5cf6" strokeWidth={2} name="Precision %" />
                  <Line type="monotone" dataKey="recall" stroke="#10b981" strokeWidth={2} name="Recall %" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Intervention Success Rate */}
        <Grid item xs={12} md={6}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Intervention Success Rates
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={interventionSuccess} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(59, 130, 246, 0.1)" />
                  <XAxis type="number" domain={[0, 100]} stroke="#9ca3af" />
                  <YAxis type="category" dataKey="type" stroke="#9ca3af" width={120} />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #3b82f6' }} />
                  <Bar dataKey="success" fill="#10b981" name="Success %" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Processing Time */}
        <Grid item xs={12} md={6}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Agent Processing Time (ms)
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={processingTime}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(59, 130, 246, 0.1)" />
                  <XAxis dataKey="agent" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #3b82f6' }} />
                  <Bar dataKey="time" fill="#3b82f6" name="Time (ms)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Key Metrics Summary */}
        <Grid item xs={12}>
          <Card className="card">
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Performance Summary
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(59, 130, 246, 0.1)', borderRadius: 2 }}>
                    <Typography variant="h4" sx={{ color: '#3b82f6', fontWeight: 700 }}>72%</Typography>
                    <Typography variant="body2" sx={{ color: '#9ca3af' }}>Detection Accuracy</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(139, 92, 246, 0.1)', borderRadius: 2 }}>
                    <Typography variant="h4" sx={{ color: '#8b5cf6', fontWeight: 700 }}>87%</Typography>
                    <Typography variant="body2" sx={{ color: '#9ca3af' }}>Prediction Accuracy</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(16, 185, 129, 0.1)', borderRadius: 2 }}>
                    <Typography variant="h4" sx={{ color: '#10b981', fontWeight: 700 }}>95%</Typography>
                    <Typography variant="body2" sx={{ color: '#9ca3af' }}>Intervention Success</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(245, 158, 11, 0.1)', borderRadius: 2 }}>
                    <Typography variant="h4" sx={{ color: '#f59e0b', fontWeight: 700 }}>250ms</Typography>
                    <Typography variant="body2" sx={{ color: '#9ca3af' }}>Avg Processing Time</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Analytics
