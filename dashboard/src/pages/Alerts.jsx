import React from 'react'
import { useQuery } from 'react-query'
import { Box, Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, CircularProgress } from '@mui/material'
import { alertsAPI } from '../services/api'

function Alerts() {
  const { data, isLoading } = useQuery('alerts', () =>
    alertsAPI.list().then((res) => res.data)
  )

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  // Mock alerts for demo
  const mockAlerts = [
    { id: '1', name: 'High CPU Usage', severity: 'high', status: 'firing', timestamp: new Date().toISOString() },
    { id: '2', name: 'Disk Space Low', severity: 'medium', status: 'firing', timestamp: new Date().toISOString() },
    { id: '3', name: 'Network Latency', severity: 'low', status: 'resolved', timestamp: new Date().toISOString() },
  ]

  const alerts = data?.alerts || mockAlerts

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'error'
      case 'high':
        return 'error'
      case 'medium':
        return 'warning'
      case 'low':
        return 'info'
      default:
        return 'default'
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Alert Management
      </Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Alert Name</TableCell>
              <TableCell>Severity</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Timestamp</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alerts.map((alert) => (
              <TableRow key={alert.id}>
                <TableCell>{alert.name}</TableCell>
                <TableCell>
                  <Chip
                    label={alert.severity}
                    color={getSeverityColor(alert.severity)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={alert.status}
                    color={alert.status === 'firing' ? 'error' : 'success'}
                    size="small"
                  />
                </TableCell>
                <TableCell>{new Date(alert.timestamp).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default Alerts
