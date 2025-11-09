import React from 'react'
import { useQuery } from 'react-query'
import { Box, Paper, Typography, Grid, Card, CardContent, Chip, CircularProgress } from '@mui/material'
import { devicesAPI } from '../services/api'

function Devices() {
  const { data, isLoading } = useQuery('devices', () =>
    devicesAPI.list().then((res) => res.data)
  )

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  // Mock devices for demo
  const mockDevices = [
    { id: '1', name: 'Temperature Sensor A', type: 'sensor', protocol: 'zigbee', status: 'online' },
    { id: '2', name: 'Pressure Gauge B', type: 'sensor', protocol: 'modbus', status: 'online' },
    { id: '3', name: 'Home Assistant Hub', type: 'gateway', protocol: 'homeassistant', status: 'online' },
    { id: '4', name: 'OPC-UA Server', type: 'plc', protocol: 'opcua', status: 'offline' },
  ]

  const devices = data?.devices || mockDevices

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Connected Devices
      </Typography>
      
      <Grid container spacing={3}>
        {devices.map((device) => (
          <Grid item xs={12} sm={6} md={4} key={device.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {device.name}
                  </Typography>
                  <Chip
                    label={device.status}
                    color={device.status === 'online' ? 'success' : 'error'}
                    size="small"
                  />
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  Type: {device.type}
                </Typography>
                <Typography color="textSecondary">
                  Protocol: {device.protocol.toUpperCase()}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

export default Devices
