import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Error
} from '@mui/icons-material';

const SourceCredibility = () => {
  const [sources, setSources] = useState([]);
  const [trendingTopics, setTrendingTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      // Fetch source credibility
      const sourcesRes = await fetch('http://localhost:8000/api/source-credibility');
      const sourcesData = await sourcesRes.json();
      setSources(sourcesData.sources || []);

      // Fetch trending topics
      const topicsRes = await fetch('http://localhost:8000/api/trending-topics');
      const topicsData = await topicsRes.json();
      setTrendingTopics(topicsData.topics || []);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const getCredibilityColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const getCredibilityIcon = (score) => {
    if (score >= 80) return <CheckCircle color="success" />;
    if (score >= 60) return <Warning color="warning" />;
    return <Error color="error" />;
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>Loading...</Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        📊 Source Credibility & Trends
      </Typography>

      <Grid container spacing={3}>
        {/* Source Credibility Section */}
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
              🏆 News Source Credibility Scores
            </Typography>
            
            <List>
              {sources.slice(0, 10).map((source, index) => (
                <React.Fragment key={source.name}>
                  <ListItem>
                    <Box sx={{ width: '100%' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        {getCredibilityIcon(source.score)}
                        <Typography variant="subtitle1" sx={{ ml: 1, flex: 1 }}>
                          {source.name}
                        </Typography>
                        <Chip
                          label={`${Math.round(source.score)}%`}
                          color={getCredibilityColor(source.score)}
                          size="small"
                        />
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={source.score}
                          color={getCredibilityColor(source.score)}
                          sx={{ flex: 1, height: 8, borderRadius: 4 }}
                        />
                      </Box>
                      <Box sx={{ display: 'flex', gap: 2, fontSize: '0.85rem', color: 'text.secondary' }}>
                        <span>Total: {source.total_posts}</span>
                        <span style={{ color: source.fake_posts > 0 ? '#f44336' : '#4caf50' }}>
                          Fake: {source.fake_posts}
                        </span>
                      </Box>
                    </Box>
                  </ListItem>
                  {index < sources.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Trending Topics Section */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
              🔥 Trending Topics
            </Typography>
            
            <List>
              {trendingTopics.map((topic, index) => (
                <React.Fragment key={topic.topic}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TrendingUp color="primary" />
                          <Typography variant="body1">
                            {topic.topic}
                          </Typography>
                        </Box>
                      }
                      secondary={`Mentioned ${topic.count} times`}
                    />
                    <Chip
                      label={topic.count}
                      color="primary"
                      size="small"
                      sx={{ fontWeight: 'bold' }}
                    />
                  </ListItem>
                  {index < trendingTopics.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>

          {/* Summary Card */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📈 Quick Stats
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Total Sources Monitored
                </Typography>
                <Typography variant="h4" color="primary">
                  {sources.length}
                </Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Active Trending Topics
                </Typography>
                <Typography variant="h4" color="secondary">
                  {trendingTopics.length}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SourceCredibility;
