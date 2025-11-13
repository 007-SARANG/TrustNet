import React from 'react'
import { Box, Card, CardContent, Typography, Chip, Avatar } from '@mui/material'
import { useSocket } from '../contexts/SocketContext'
import WarningIcon from '@mui/icons-material/Warning'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import InfoIcon from '@mui/icons-material/Info'

const ActivityFeed = () => {
  const { messages } = useSocket()

  const getIcon = (type) => {
    switch (type) {
      case 'warning':
        return <WarningIcon sx={{ color: '#f59e0b' }} />
      case 'success':
        return <CheckCircleIcon sx={{ color: '#10b981' }} />
      default:
        return <InfoIcon sx={{ color: '#3b82f6' }} />
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'HIGH':
        return '#ef4444'
      case 'MEDIUM':
        return '#f59e0b'
      case 'LOW':
        return '#10b981'
      default:
        return '#3b82f6'
    }
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 700 }}>
        Live Activity Feed
      </Typography>

      <Card className="card">
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
            <Chip label="All" color="primary" />
            <Chip label="Flagged" variant="outlined" />
            <Chip label="Interventions" variant="outlined" />
            <Chip label="Completed" variant="outlined" />
          </Box>

          {messages.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <Typography variant="body1" sx={{ color: '#9ca3af', mb: 2 }}>
                No activity yet
              </Typography>
              <Typography variant="body2" sx={{ color: '#6b7280' }}>
                Start the system to see real-time updates
              </Typography>
            </Box>
          ) : (
            <Box>
              {messages.map((msg, idx) => (
                <Box
                  key={idx}
                  className="activity-item"
                  sx={{
                    display: 'flex',
                    gap: 2,
                    alignItems: 'flex-start',
                  }}
                >
                  <Avatar sx={{ bgcolor: 'rgba(59, 130, 246, 0.2)' }}>
                    {getIcon(msg.type)}
                  </Avatar>
                  <Box sx={{ flex: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="h6" sx={{ fontSize: '1rem', fontWeight: 600 }}>
                        {msg.agent || 'System'} Agent
                      </Typography>
                      <Chip
                        label={msg.priority || 'INFO'}
                        size="small"
                        sx={{
                          backgroundColor: `${getPriorityColor(msg.priority)}20`,
                          color: getPriorityColor(msg.priority),
                          fontSize: '0.7rem',
                        }}
                      />
                    </Box>
                    <Typography variant="body2" sx={{ color: '#d1d5db', mb: 1 }}>
                      {msg.message || JSON.stringify(msg)}
                    </Typography>
                    <Typography variant="caption" sx={{ color: '#6b7280' }}>
                      {new Date().toLocaleString()}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  )
}

export default ActivityFeed
