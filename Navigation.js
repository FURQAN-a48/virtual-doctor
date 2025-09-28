import React from 'react';
import {
  BottomNavigation,
  BottomNavigationAction,
  Paper,
  Box
} from '@mui/material';
import {
  Home,
  Chat,
  CameraAlt,
  Medication
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const Navigation = ({ currentPage, setCurrentPage }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (event, newValue) => {
    setCurrentPage(newValue);
    switch (newValue) {
      case 'home':
        navigate('/');
        break;
      case 'symptoms':
        navigate('/symptoms');
        break;
      case 'tablet':
        navigate('/tablet');
        break;
      case 'medicines':
        navigate('/medicines');
        break;
      default:
        navigate('/');
    }
  };

  const getCurrentValue = () => {
    switch (location.pathname) {
      case '/':
        return 'home';
      case '/symptoms':
        return 'symptoms';
      case '/tablet':
        return 'tablet';
      case '/medicines':
        return 'medicines';
      default:
        return 'home';
    }
  };

  return (
    <Box sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 1000 }}>
      <Paper elevation={3}>
        <BottomNavigation
          value={getCurrentValue()}
          onChange={handleNavigation}
          showLabels
        >
          <BottomNavigationAction
            label="Home"
            value="home"
            icon={<Home />}
          />
          <BottomNavigationAction
            label="Symptoms"
            value="symptoms"
            icon={<Chat />}
          />
          <BottomNavigationAction
            label="Tablet ID"
            value="tablet"
            icon={<CameraAlt />}
          />
          <BottomNavigationAction
            label="Medicines"
            value="medicines"
            icon={<Medication />}
          />
        </BottomNavigation>
      </Paper>
    </Box>
  );
};

export default Navigation;
