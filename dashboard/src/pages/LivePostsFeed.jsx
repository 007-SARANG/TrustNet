import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Avatar,
  IconButton,
  Link,
  Grid,
  Divider,
  Badge,
  TextField,
  Button,
  CircularProgress,
  Alert,
  CardMedia,
  Paper
} from '@mui/material'
import InstagramIcon from '@mui/icons-material/Instagram'
import TwitterIcon from '@mui/icons-material/Twitter'
import RedditIcon from '@mui/icons-material/Reddit'
import YouTubeIcon from '@mui/icons-material/YouTube'
import OpenInNewIcon from '@mui/icons-material/OpenInNew'
import ThumbUpIcon from '@mui/icons-material/ThumbUp'
import CommentIcon from '@mui/icons-material/Comment'
import ShareIcon from '@mui/icons-material/Share'
import WarningIcon from '@mui/icons-material/Warning'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import BlockIcon from '@mui/icons-material/Block'
import ImageSearchIcon from '@mui/icons-material/ImageSearch'
import { useSocket } from '../contexts/SocketContext'

// Instagram Mismatch Detector Component
const InstagramMismatchDetector = () => {
  const [imageUrl, setImageUrl] = useState('')
  const [caption, setCaption] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const analyzePost = async () => {
    if (!imageUrl || !caption) {
      setError('Please provide both image URL and caption')
      return
    }

    setAnalyzing(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/analyze-instagram-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_url: imageUrl,
          caption: caption
        })
      })

      const data = await response.json()
      
      if (response.ok) {
        setResult(data.analysis)
      } else {
        // Handle error - convert object to string if needed
        const errorMsg = typeof data.detail === 'string' 
          ? data.detail 
          : JSON.stringify(data.detail) || 'Analysis failed'
        setError(errorMsg)
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to backend. Make sure quick_start.py is running.')
    } finally {
      setAnalyzing(false)
    }
  }

  const loadDemoExample = (type) => {
    if (type === 'match') {
      setImageUrl('https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400')
      setCaption('Beautiful starry night sky with Milky Way galaxy visible')
    } else if (type === 'mismatch') {
      setImageUrl('https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400')
      setCaption('New BMW M5 2024 unveiled! Amazing luxury sports car with 600HP engine')
    }
  }

  const getActionColor = (action) => {
    switch (action) {
      case 'block': return 'error'
      case 'review': return 'warning'
      case 'allow': return 'success'
      default: return 'default'
    }
  }

  const getActionIcon = (action) => {
    switch (action) {
      case 'block': return <BlockIcon />
      case 'review': return <WarningIcon />
      case 'allow': return <CheckCircleIcon />
      default: return null
    }
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <InstagramIcon fontSize="large" sx={{ color: '#E1306C' }} />
          Instagram Mismatch Detector
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Detect misinformation by analyzing if Instagram images match their captions using AI
        </Typography>
      </Box>

      {/* Input Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analyze Instagram Post
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
            <Button 
              size="small" 
              variant="outlined" 
              onClick={() => loadDemoExample('match')}
            >
              Load Match Example
            </Button>
            <Button 
              size="small" 
              variant="outlined" 
              color="error"
              onClick={() => loadDemoExample('mismatch')}
            >
              Load Mismatch Example (Cat + BMW)
            </Button>
          </Box>

          <TextField
            fullWidth
            label="Image URL"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="https://example.com/image.jpg"
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            label="Caption"
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            placeholder="Post caption text..."
            multiline
            rows={3}
            sx={{ mb: 2 }}
          />

          <Button
            variant="contained"
            onClick={analyzePost}
            disabled={analyzing || !imageUrl || !caption}
            startIcon={analyzing ? <CircularProgress size={20} /> : <ImageSearchIcon />}
            fullWidth
          >
            {analyzing ? 'Analyzing...' : 'Analyze Image-Caption Match'}
          </Button>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <Grid container spacing={3}>
          {/* Image Preview */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardMedia
                component="img"
                height="300"
                image={imageUrl}
                alt="Instagram post"
                sx={{ objectFit: 'cover' }}
              />
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Caption
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {caption}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Analysis Results */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Analysis Results
                </Typography>

                {/* Image-Caption Match */}
                <Paper sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Image-Caption Match
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                    <Typography variant="h4">
                      {(result.image_caption_match?.similarity * 100).toFixed(1)}%
                    </Typography>
                    <Chip
                      label={result.image_caption_match?.matches ? 'MATCHES' : 'MISMATCH'}
                      color={result.image_caption_match?.matches ? 'success' : 'error'}
                      icon={result.image_caption_match?.matches ? <CheckCircleIcon /> : <BlockIcon />}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {result.image_caption_match?.reasoning}
                  </Typography>
                  
                  {!result.image_caption_match?.matches && (
                    <Alert severity="error" sx={{ mt: 1 }}>
                      <Typography variant="caption">
                        <strong>Mismatch Type:</strong> {result.image_caption_match?.mismatch_type || 'Content mismatch'}
                      </Typography>
                    </Alert>
                  )}
                </Paper>

                {/* Prevention Action */}
                <Paper sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Moderation Action
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Chip
                      label={result.prevention?.action?.toUpperCase()}
                      color={getActionColor(result.prevention?.action)}
                      icon={getActionIcon(result.prevention?.action)}
                      size="large"
                    />
                    {result.prevention?.flagged && (
                      <Chip label="FLAGGED" color="error" size="small" />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Confidence: {(result.prevention?.confidence * 100).toFixed(1)}%
                  </Typography>
                </Paper>

                {/* Rules Triggered */}
                {result.prevention?.rules_triggered?.length > 0 && (
                  <Paper sx={{ p: 2, mb: 2, bgcolor: 'background.default' }}>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Rules Triggered
                    </Typography>
                    {result.prevention.rules_triggered.map((rule, idx) => (
                      <Alert 
                        key={idx} 
                        severity={rule.action === 'block' ? 'error' : 'warning'}
                        sx={{ mb: 1 }}
                      >
                        <Typography variant="body2">
                          <strong>Rule {rule.rule_id}:</strong> {rule.reason}
                        </Typography>
                      </Alert>
                    ))}
                  </Paper>
                )}

                {/* Classification */}
                <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Content Classification
                  </Typography>
                  <Typography variant="body2">
                    <strong>Category:</strong> {result.classification?.category}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Informative:</strong> {result.classification?.is_informative ? 'Yes' : 'No'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Confidence:</strong> {(result.classification?.confidence * 100).toFixed(1)}%
                  </Typography>
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Info Box */}
      <Card sx={{ mt: 3, bgcolor: 'info.main', color: 'info.contrastText' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            🔬 How It Works
          </Typography>
          <Typography variant="body2" paragraph>
            1. <strong>CLIP AI Model</strong> analyzes the image content and caption text
          </Typography>
          <Typography variant="body2" paragraph>
            2. Calculates semantic similarity score (0-100%)
          </Typography>
          <Typography variant="body2" paragraph>
            3. Applies decision rules:
          </Typography>
          <Box sx={{ pl: 2 }}>
            <Typography variant="body2">• &gt;65%: ✅ ALLOW (Strong match)</Typography>
            <Typography variant="body2">• 30-65%: ⚠️ REVIEW (Moderate match)</Typography>
            <Typography variant="body2">• &lt;30%: 🚨 BLOCK (Mismatch - potential misinformation!)</Typography>
          </Box>
          <Typography variant="body2" sx={{ mt: 2 }}>
            <strong>Example:</strong> Image of cat + Caption about BMW car = BLOCKED!
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}

const LivePostsFeed = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('feed') // 'feed' or 'instagram'
  const { socket } = useSocket()

  // Fetch recent posts on mount
  useEffect(() => {
    const fetchRecentPosts = async () => {
      try {
        console.log('Fetching recent posts from API...')
        const response = await fetch('http://localhost:8000/api/recent-posts')
        if (response.ok) {
          const data = await response.json()
          console.log('Loaded recent posts:', data.posts?.length || 0)
          setPosts(data.posts || [])
        }
      } catch (error) {
        console.error('Error fetching recent posts:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchRecentPosts()
  }, [])

  // Setup WebSocket listener
  useEffect(() => {
    console.log('LivePostsFeed mounted, socket:', socket)
    console.log('Socket connected?', socket?.connected)
    
    if (socket) {
      console.log('Setting up new_post listener...')
      
      // Listen for new posts
      socket.on('new_post', (post) => {
        console.log('🎉 NEW POST RECEIVED:', post)
        setPosts((prevPosts) => {
          console.log('Adding to posts array, current count:', prevPosts.length)
          return [post, ...prevPosts].slice(0, 50)
        })
      })
      
      // Test connection
      socket.emit('ping', 'hello from dashboard')
      console.log('Sent ping to server')

      return () => {
        console.log('Cleaning up new_post listener')
        socket.off('new_post')
      }
    } else {
      console.warn('Socket not available!')
    }
  }, [socket])

  const getPlatformIcon = (platform) => {
    switch (platform?.toLowerCase()) {
      case 'instagram':
        return <InstagramIcon sx={{ color: '#E1306C' }} />
      case 'twitter':
        return <TwitterIcon sx={{ color: '#1DA1F2' }} />
      case 'reddit':
        return <RedditIcon sx={{ color: '#FF4500' }} />
      case 'youtube':
        return <YouTubeIcon sx={{ color: '#FF0000' }} />
      default:
        return null
    }
  }

  const getRiskColor = (riskScore) => {
    if (riskScore >= 0.7) return 'error'
    if (riskScore >= 0.4) return 'warning'
    return 'success'
  }

  const getRiskLabel = (riskScore) => {
    if (riskScore >= 0.7) return 'HIGH RISK'
    if (riskScore >= 0.4) return 'MODERATE'
    return 'LOW RISK'
  }

  const testConnection = async () => {
    try {
      console.log('Testing backend connection...')
      const response = await fetch('http://localhost:8000/api/test-post')
      const data = await response.json()
      console.log('Test response:', data)
      alert('Test post sent! Check console and posts below.')
    } catch (error) {
      console.error('Test failed:', error)
      alert('Error: ' + error.message)
    }
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Tab Navigation */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, borderBottom: 1, borderColor: 'divider', pb: 1 }}>
        <Button
          variant={activeTab === 'feed' ? 'contained' : 'text'}
          onClick={() => setActiveTab('feed')}
          size="large"
        >
          📡 Live Feed
        </Button>
        <Button
          variant={activeTab === 'instagram' ? 'contained' : 'text'}
          onClick={() => setActiveTab('instagram')}
          startIcon={<InstagramIcon />}
          size="large"
        >
          Instagram Detector
        </Button>
      </Box>

      {/* Content */}
      {activeTab === 'instagram' ? (
        <InstagramMismatchDetector />
      ) : (
        <>
          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                📡 Live Posts Feed
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Real-time social media posts being analyzed for misinformation
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <button 
                onClick={testConnection}
                style={{ 
                  padding: '8px 16px', 
                  background: '#1976d2', 
                  color: 'white', 
                  border: 'none', 
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                🧪 Test Connection
              </button>
              <Chip
                label={`${posts.length} Posts`}
                color="primary"
                sx={{ fontSize: '1rem', px: 2, py: 2.5 }}
              />
            </Box>
          </Box>

      {loading ? (
        <Card sx={{ p: 4, textAlign: 'center', bgcolor: 'background.paper' }}>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
            ⏳ Loading recent posts...
          </Typography>
        </Card>
      ) : posts.length === 0 ? (
        <Card sx={{ p: 4, textAlign: 'center', bgcolor: 'background.paper' }}>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
            🔍 Waiting for posts...
          </Typography>
          <Typography variant="body2" color="text.secondary">
            RSS feeds are collecting posts. New posts will appear here automatically.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            See <strong>REQUIRED_APIS.md</strong> for setup instructions.
          </Typography>
        </Card>
      ) : (
        <Grid container spacing={2}>
          {posts.map((post, index) => (
            <Grid item xs={12} key={`${post.platform}-${index}`}>
              <Card
                sx={{
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  },
                  borderLeft: `4px solid ${
                    post.classification === 'FAKE' ? '#ef4444' : '#10b981'
                  }`,
                }}
              >
                <CardContent>
                  {/* Header */}
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                      {getPlatformIcon(post.platform)}
                    </Avatar>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                        @{post.author}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {post.platform?.toUpperCase()} • Just now
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                      <Chip
                        icon={
                          post.classification === 'FAKE' ? (
                            <WarningIcon />
                          ) : (
                            <CheckCircleIcon />
                          )
                        }
                        label={post.classification}
                        color={post.classification === 'FAKE' ? 'error' : 'success'}
                        size="small"
                      />
                      <Chip
                        label={getRiskLabel(post.risk_score || 0)}
                        color={getRiskColor(post.risk_score || 0)}
                        size="small"
                        variant="outlined"
                      />
                      {post.url && (
                        <IconButton
                          size="small"
                          component={Link}
                          href={post.url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <OpenInNewIcon fontSize="small" />
                        </IconButton>
                      )}
                    </Box>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Content */}
                  <Typography
                    variant="body1"
                    sx={{ mb: 2, whiteSpace: 'pre-wrap', lineHeight: 1.6 }}
                  >
                    {post.content}
                  </Typography>

                  {/* AI Analysis Details */}
                  {post.ai_reasoning && (
                    <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(25, 118, 210, 0.08)', borderRadius: 1 }}>
                      <Typography variant="subtitle2" color="primary" gutterBottom sx={{ fontWeight: 'bold' }}>
                        🤖 AI Analysis
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {post.ai_reasoning}
                      </Typography>
                    </Box>
                  )}

                  {/* Key Claims */}
                  {post.key_claims && post.key_claims.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        📋 Key Claims Identified:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                        {post.key_claims.map((claim, i) => (
                          <Chip
                            key={i}
                            label={claim}
                            size="small"
                            variant="outlined"
                            sx={{ fontSize: '0.75rem' }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}

                  {/* Fact Checks */}
                  {post.fact_checks && post.fact_checks.length > 0 && (
                    <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(76, 175, 80, 0.08)', borderRadius: 1 }}>
                      <Typography variant="subtitle2" color="success.main" gutterBottom sx={{ fontWeight: 'bold' }}>
                        ✅ Fact Check Results
                      </Typography>
                      {post.fact_checks.map((fc, i) => (
                        <Box key={i} sx={{ mt: 1 }}>
                          <Typography variant="body2" fontWeight="bold">
                            {fc.claim}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Rating: <strong>{fc.rating}</strong> (Source: {fc.source})
                          </Typography>
                        </Box>
                      ))}
                    </Box>
                  )}

                  {/* Source Credibility Badge */}
                  {post.source_credibility !== undefined && (
                    <Box sx={{ mt: 2 }}>
                      <Chip
                        label={`Source Credibility: ${Math.round(post.source_credibility)}%`}
                        color={post.source_credibility >= 80 ? 'success' : post.source_credibility >= 60 ? 'warning' : 'error'}
                        size="small"
                        sx={{ fontWeight: 'bold' }}
                      />
                    </Box>
                  )}

                  {/* Metrics */}
                  {post.metrics && (
                    <Box sx={{ display: 'flex', gap: 3, mt: 2 }}>
                      {post.metrics.likes !== undefined && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          <ThumbUpIcon fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {post.metrics.likes.toLocaleString()}
                          </Typography>
                        </Box>
                      )}
                      {post.metrics.retweets !== undefined && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          <ShareIcon fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {post.metrics.retweets.toLocaleString()}
                          </Typography>
                        </Box>
                      )}
                      {post.metrics.num_comments !== undefined && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          <CommentIcon fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {post.metrics.num_comments.toLocaleString()}
                          </Typography>
                        </Box>
                      )}
                      {post.metrics.score !== undefined && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          <Typography variant="body2" color="text.secondary">
                            Score: {post.metrics.score.toLocaleString()}
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  )}

                  {/* Risk Score Bar */}
                  <Box sx={{ mt: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="caption" color="text.secondary">
                        Risk Score
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {((post.risk_score || 0) * 100).toFixed(0)}%
                      </Typography>
                    </Box>
                    <Box
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        bgcolor: 'grey.200',
                        overflow: 'hidden',
                      }}
                    >
                      <Box
                        sx={{
                          height: '100%',
                          width: `${(post.risk_score || 0) * 100}%`,
                          bgcolor:
                            post.risk_score >= 0.7
                              ? 'error.main'
                              : post.risk_score >= 0.4
                              ? 'warning.main'
                              : 'success.main',
                          transition: 'width 0.5s',
                        }}
                      />
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      </>
    )}
    </Box>
  )
}

export default LivePostsFeed
