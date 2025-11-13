import React, { useEffect, useRef } from 'react'
import { Box, Card, CardContent, Typography, Chip } from '@mui/material'
import * as d3 from 'd3'

const NetworkView = () => {
  const svgRef = useRef()

  useEffect(() => {
    // Sample network data
    const nodes = [
      { id: 'seed', group: 1, size: 20, label: 'Original Post' },
      { id: 'user1', group: 2, size: 15, label: 'User 1' },
      { id: 'user2', group: 2, size: 15, label: 'User 2' },
      { id: 'user3', group: 2, size: 12, label: 'User 3' },
      { id: 'bot1', group: 3, size: 10, label: 'Bot 1' },
      { id: 'bot2', group: 3, size: 10, label: 'Bot 2' },
      { id: 'user4', group: 2, size: 12, label: 'User 4' },
      { id: 'user5', group: 2, size: 12, label: 'User 5' },
    ]

    const links = [
      { source: 'seed', target: 'user1' },
      { source: 'seed', target: 'user2' },
      { source: 'seed', target: 'bot1' },
      { source: 'user1', target: 'user3' },
      { source: 'user2', target: 'user4' },
      { source: 'bot1', target: 'bot2' },
      { source: 'bot2', target: 'user5' },
    ]

    // Clear previous SVG
    d3.select(svgRef.current).selectAll('*').remove()

    const width = 800
    const height = 600

    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height])

    // Color scale
    const color = d3.scaleOrdinal()
      .domain([1, 2, 3])
      .range(['#ef4444', '#3b82f6', '#f59e0b'])

    // Force simulation
    const simulation = d3
      .forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))

    // Links
    const link = svg
      .append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#3b82f6')
      .attr('stroke-opacity', 0.3)
      .attr('stroke-width', 2)

    // Nodes
    const node = svg
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', d => d.size)
      .attr('fill', d => color(d.group))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .call(drag(simulation))

    // Labels
    const label = svg
      .append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .text(d => d.label)
      .attr('font-size', 10)
      .attr('fill', '#fff')
      .attr('text-anchor', 'middle')
      .attr('dy', 4)

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)

      label
        .attr('x', d => d.x)
        .attr('y', d => d.y)
    })

    // Drag functionality
    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        event.subject.fx = event.subject.x
        event.subject.fy = event.subject.y
      }

      function dragged(event) {
        event.subject.fx = event.x
        event.subject.fy = event.y
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0)
        event.subject.fx = null
        event.subject.fy = null
      }

      return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    }
  }, [])

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 700 }}>
        Network Visualization
      </Typography>

      <Card className="card">
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            <Chip
              label="Original Post"
              sx={{ backgroundColor: '#ef444420', color: '#ef4444' }}
            />
            <Chip
              label="Users"
              sx={{ backgroundColor: '#3b82f620', color: '#3b82f6' }}
            />
            <Chip
              label="Bots"
              sx={{ backgroundColor: '#f59e0b20', color: '#f59e0b' }}
            />
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'center', bgcolor: '#0a0e27', borderRadius: 2, p: 2 }}>
            <svg ref={svgRef}></svg>
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography variant="body2" sx={{ color: '#9ca3af', mb: 1 }}>
              Network Statistics:
            </Typography>
            <Box sx={{ display: 'flex', gap: 3 }}>
              <Box>
                <Typography variant="h6">8</Typography>
                <Typography variant="caption" sx={{ color: '#6b7280' }}>Total Nodes</Typography>
              </Box>
              <Box>
                <Typography variant="h6">7</Typography>
                <Typography variant="caption" sx={{ color: '#6b7280' }}>Connections</Typography>
              </Box>
              <Box>
                <Typography variant="h6">25%</Typography>
                <Typography variant="caption" sx={{ color: '#6b7280' }}>Bot Ratio</Typography>
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}

export default NetworkView
