import React, { useState } from 'react'
import { Box, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon, ListItemText, IconButton, Badge } from '@mui/material'
import { Link, useLocation } from 'react-router-dom'
import DashboardIcon from '@mui/icons-material/Dashboard'
import TimelineIcon from '@mui/icons-material/Timeline'
import AccountTreeIcon from '@mui/icons-material/AccountTree'
import BarChartIcon from '@mui/icons-material/BarChart'
import NotificationsIcon from '@mui/icons-material/Notifications'
import MenuIcon from '@mui/icons-material/Menu'
import { useSocket } from '../contexts/SocketContext'

const drawerWidth = 240

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: '📡 Live Posts', icon: <TimelineIcon />, path: '/live' },
  { text: '📊 Source Trust', icon: <BarChartIcon />, path: '/sources' },
  { text: 'Activity Feed', icon: <TimelineIcon />, path: '/activity' },
  { text: 'Network View', icon: <AccountTreeIcon />, path: '/network' },
  { text: 'Analytics', icon: <BarChartIcon />, path: '/analytics' },
]

const Layout = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()
  const { connected, messages } = useSocket()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const drawer = (
    <Box>
      <Toolbar>
        <Typography variant="h6" sx={{ fontWeight: 700, color: '#3b82f6' }}>
          🛡️ TrustNet
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderRight: '3px solid #3b82f6',
              },
              '&:hover': {
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
              }
            }}
          >
            <ListItemIcon sx={{ color: location.pathname === item.path ? '#3b82f6' : 'inherit' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: 'rgba(26, 31, 58, 0.95)',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid rgba(59, 130, 246, 0.1)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            TrustNet 2.0 - AI Misinformation Detection System
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                backgroundColor: connected ? '#10b981' : '#ef4444',
                animation: connected ? 'pulse 2s infinite' : 'none',
              }}
            />
            <Typography variant="body2" sx={{ color: connected ? '#10b981' : '#ef4444' }}>
              {connected ? 'Connected' : 'Disconnected'}
            </Typography>
            <IconButton color="inherit">
              <Badge badgeContent={messages.length} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: '#1a1f3a',
            borderRight: '1px solid rgba(59, 130, 246, 0.1)',
          },
        }}
      >
        {drawer}
      </Drawer>

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            backgroundColor: '#1a1f3a',
          },
        }}
      >
        {drawer}
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
        }}
      >
        {children}
      </Box>
    </Box>
  )
}

export default Layout
