import React, { useState } from 'react'
import { Box, Paper, Typography, TextField, Button, Grid } from '@mui/material'
import { metricsAPI } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function Metrics() {
  const [query, setQuery] = useState('up')
  const [data, setData] = useState([])

  const handleQuery = async () => {
    try {
      const response = await metricsAPI.query(query)
      // Process and set data
      console.log('Metrics data:', response.data)
    } catch (error) {
      console.error('Error querying metrics:', error)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Metrics Explorer
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={9}>
            <TextField
              fullWidth
              label="PromQL Query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., up, rate(http_requests_total[5m])"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button fullWidth variant="contained" onClick={handleQuery} size="large">
              Execute Query
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Query Results
        </Typography>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#2196f3" />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  )
}

export default Metrics
