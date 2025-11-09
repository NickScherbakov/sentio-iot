import React from 'react'
import { Box, Paper, Typography } from '@mui/material'

function Traces() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Distributed Traces
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography color="textSecondary">
          Trace visualization and analysis interface. Query and explore distributed traces from your IoT devices and services.
        </Typography>
      </Paper>
    </Box>
  )
}

export default Traces
