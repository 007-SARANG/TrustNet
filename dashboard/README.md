# TrustNet 2.0 Dashboard

## 🎨 React Dashboard for TrustNet 2.0

A modern, real-time dashboard built with React, Material-UI, and D3.js for visualizing TrustNet's misinformation detection system.

## ✨ Features

- **Real-time Updates**: WebSocket integration for live agent activity
- **Interactive Visualizations**: Charts, graphs, and network diagrams
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Professional dark mode interface
- **Multiple Views**: Dashboard, Activity Feed, Network View, Analytics

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
cd dashboard
npm install
```

### Development

```bash
npm run dev
```

Open http://localhost:3000

### Production Build

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
dashboard/
├── src/
│   ├── components/        # Reusable components
│   │   └── Layout.jsx     # Main layout with sidebar
│   ├── contexts/          # React contexts
│   │   └── SocketContext.jsx  # WebSocket connection
│   ├── pages/             # Page components
│   │   ├── Dashboard.jsx  # Main dashboard
│   │   ├── ActivityFeed.jsx  # Live activity
│   │   ├── NetworkView.jsx   # Network visualization
│   │   └── Analytics.jsx     # Performance analytics
│   ├── App.jsx            # Main app component
│   ├── App.css            # Global styles
│   └── main.jsx           # Entry point
├── index.html
├── package.json
└── vite.config.js         # Vite configuration
```

## 🎯 Pages

### 1. Dashboard
- Key metrics (posts analyzed, fake detected, interventions, success rate)
- Agent status indicators
- Recent activity feed
- Detection trend chart
- Topic distribution pie chart
- Intervention types bar chart

### 2. Activity Feed
- Real-time stream of agent activities
- Filterable by type
- Priority indicators
- Timestamp tracking

### 3. Network View
- Interactive D3.js force-directed graph
- Visual representation of content spread
- Bot detection highlights
- Network statistics

### 4. Analytics
- Model performance trends
- Intervention success rates
- Agent processing times
- Performance summary

## 🔌 API Integration

The dashboard connects to the TrustNet backend API:

- REST API: `http://localhost:8000/api/*`
- WebSocket: `ws://localhost:8000/ws`

Endpoints used:
- `GET /api/metrics` - System metrics
- `GET /api/dashboard/stats` - Dashboard statistics
- `WS /ws` - Real-time updates

## 🎨 Customization

### Theme

Edit `src/App.jsx` to customize the Material-UI theme:

```javascript
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#3b82f6' },
    // ... customize colors
  },
})
```

### Charts

Charts use Recharts and D3.js. Customize in respective page components.

## 📦 Dependencies

- **React 18** - UI framework
- **Material-UI** - Component library
- **Recharts** - Chart library
- **D3.js** - Network visualization
- **Socket.io** - WebSocket client
- **Axios** - HTTP client
- **React Router** - Routing

## 🚀 Deployment

### Build for production

```bash
npm run build
```

Files will be in `dist/` directory.

### Deploy to static hosting

```bash
# Example: Deploy to Netlify
netlify deploy --prod --dir=dist

# Example: Deploy to Vercel
vercel --prod
```

### Environment Variables

Create `.env` file:

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🐛 Troubleshooting

**Issue**: Dashboard not connecting to backend

```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend
# Ensure FastAPI allows origin: http://localhost:3000
```

**Issue**: Charts not rendering

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Learn More

- [React Documentation](https://react.dev/)
- [Material-UI](https://mui.com/)
- [Recharts](https://recharts.org/)
- [D3.js](https://d3js.org/)
- [Vite](https://vitejs.dev/)

## 🤝 Contributing

See main project CONTRIBUTING.md

## 📄 License

MIT License - See LICENSE file in root directory

---

**Built with ❤️ for TrustNet 2.0**
