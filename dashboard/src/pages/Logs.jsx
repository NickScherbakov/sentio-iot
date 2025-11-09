import React, { useState } from 'react'
import { Box, Paper, Typography, TextField, Button, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { logsAPI } from '../services/api'

function Logs() {
  const [query, setQuery] = useState('{job="sentio"}')
  const [logs, setLogs] = useState([])

  const handleQuery = async () => {
    try {
      const response = await logsAPI.query(query)
      console.log('Logs data:', response.data)
      // Process and set logs
    } catch (error) {
      console.error('Error querying logs:', error)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Logs Explorer
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={9}>
            <TextField
              fullWidth
              label="LogQL Query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., {job='sentio'} |= 'error'"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button fullWidth variant="contained" onClick={handleQuery} size="large">
              Search Logs
            </Button>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Timestamp</TableCell>
              <TableCell>Level</TableCell>
              <TableCell>Message</TableCell>
              <TableCell>Source</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <Typography color="textSecondary">No logs found. Execute a query to see results.</Typography>
                </TableCell>
              </TableRow>
            ) : (
              logs.map((log, index) => (
                <TableRow key={index}>
                  <TableCell>{log.timestamp}</TableCell>
                  <TableCell>{log.level}</TableCell>
                  <TableCell>{log.message}</TableCell>
                  <TableCell>{log.source}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default Logs
