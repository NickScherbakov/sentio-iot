import React from 'react'
import { useQuery } from 'react-query'
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { statusAPI, aiAPI } from '../services/api'

function Dashboard() {
  const { data: status, isLoading: statusLoading } = useQuery('status', () =>
    statusAPI.get().then((res) => res.data)
  )

  const { data: anomalies, isLoading: anomaliesLoading } = useQuery(
    'anomalies',
    () => aiAPI.getAnomalies().then((res) => res.data),
    { refetchInterval: 30000 }
  )

  const { data: predictions, isLoading: predictionsLoading } = useQuery(
    'predictions',
    () => aiAPI.getPredictions().then((res) => res.data),
    { refetchInterval: 60000 }
  )

  // Mock data for charts
  const mockMetricsData = [
    { time: '00:00', cpu: 45, memory: 62, network: 28 },
    { time: '04:00', cpu: 52, memory: 65, network: 35 },
    { time: '08:00', cpu: 78, memory: 71, network: 52 },
    { time: '12:00', cpu: 65, memory: 68, network: 48 },
    { time: '16:00', cpu: 82, memory: 75, network: 61 },
    { time: '20:00', cpu: 58, memory: 69, network: 42 },
  ]

  const StatCard = ({ title, value, unit, color }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography color="textSecondary" gutterBottom variant="overline">
          {title}
        </Typography>
        <Typography variant="h4" component="div" sx={{ color, fontWeight: 'bold' }}>
          {value}
          {unit && <Typography component="span" variant="h6" color="textSecondary"> {unit}</Typography>}
        </Typography>
      </CardContent>
    </Card>
  )

  if (statusLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Dashboard Overview
      </Typography>

      {/* Status Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Active Devices" value="127" color="#2196f3" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Metrics/sec" value="3.2k" color="#4caf50" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Active Alerts" value="5" color="#ff9800" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard title="Anomalies" value={anomalies?.anomalies?.length || 0} color="#f44336" />
        </Grid>
      </Grid>

      {/* System Status */}
      {status && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            System Status
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(status.components || {}).map(([key, value]) => (
              <Grid item xs={6} sm={4} md={2} key={key}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                  }}
                >
                  <Box
                    sx={{
                      width: 12,
                      height: 12,
                      borderRadius: '50%',
                      bgcolor: value === 'healthy' ? '#4caf50' : '#f44336',
                    }}
                  />
                  <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                    {key.replace('_', ' ')}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* Metrics Chart */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Resource Utilization
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={mockMetricsData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="cpu" stroke="#2196f3" strokeWidth={2} />
            <Line type="monotone" dataKey="memory" stroke="#4caf50" strokeWidth={2} />
            <Line type="monotone" dataKey="network" stroke="#ff9800" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </Paper>

      {/* AI Insights */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Anomalies
            </Typography>
            {anomaliesLoading ? (
              <CircularProgress size={24} />
            ) : anomalies?.anomalies?.length > 0 ? (
              <Box>
                {anomalies.anomalies.slice(0, 5).map((anomaly, index) => (
                  <Alert severity="warning" key={index} sx={{ mb: 1 }}>
                    {anomaly.metric}: {anomaly.value.toFixed(2)} at {new Date(anomaly.timestamp).toLocaleTimeString()}
                  </Alert>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary">No anomalies detected</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Predictive Insights
            </Typography>
            {predictionsLoading ? (
              <CircularProgress size={24} />
            ) : predictions?.predictions?.length > 0 ? (
              <Box>
                {predictions.predictions.slice(0, 5).map((prediction, index) => (
                  <Alert
                    severity={prediction.risk_level === 'high' ? 'error' : 'info'}
                    key={index}
                    sx={{ mb: 1 }}
                  >
                    {prediction.device_id}: {prediction.risk_level} risk ({(prediction.confidence * 100).toFixed(0)}% confidence)
                  </Alert>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary">No predictions available</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard
