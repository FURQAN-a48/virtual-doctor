import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import { LocalHospital, CameraAlt, Chat } from '@mui/icons-material';

// Components
import HomePage from './components/HomePage';
import SymptomChecker from './components/SymptomChecker';
import TabletRecognition from './components/TabletRecognition';
import MedicineDatabase from './components/MedicineDatabase';
import Navigation from './components/Navigation';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static" elevation={2}>
            <Toolbar>
              <LocalHospital sx={{ mr: 2 }} />
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Virtual Doctor
              </Typography>
              <Typography variant="body2" sx={{ mr: 2 }}>
                AI-Powered Medicine Assistant
              </Typography>
            </Toolbar>
          </AppBar>
          
          <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
          
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/symptoms" element={<SymptomChecker />} />
              <Route path="/tablet" element={<TabletRecognition />} />
              <Route path="/medicines" element={<MedicineDatabase />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
