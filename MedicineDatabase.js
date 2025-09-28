import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Pagination,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material';
import {
  Search,
  Medication,
  Info,
  Warning,
  LocalHospital
} from '@mui/icons-material';
import { apiService } from '../services/apiService';

const MedicineDatabase = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedMedicine, setSelectedMedicine] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMedicines();
  }, [currentPage, searchTerm]);

  const loadMedicines = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.getMedicines({
        page: currentPage,
        per_page: 12,
        search: searchTerm
      });
      
      setMedicines(response.medicines || []);
      setTotalPages(response.pages || 1);
    } catch (error) {
      console.error('Error loading medicines:', error);
      setError('Failed to load medicines. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    setCurrentPage(1);
    loadMedicines();
  };

  const handlePageChange = (event, page) => {
    setCurrentPage(page);
  };

  const handleMedicineDetails = (medicine) => {
    setSelectedMedicine(medicine);
    setShowDetails(true);
  };

  const formatText = (text, maxLength = 150) => {
    if (!text) return 'N/A';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getPregnancyColor = (category) => {
    switch (category) {
      case 'A': return 'success';
      case 'B': return 'info';
      case 'C': return 'warning';
      case 'D': return 'error';
      case 'X': return 'error';
      default: return 'default';
    }
  };

  const getPregnancyText = (category) => {
    switch (category) {
      case 'A': return 'Safe (A)';
      case 'B': return 'Probably Safe (B)';
      case 'C': return 'Caution (C)';
      case 'D': return 'Harmful (D)';
      case 'X': return 'Contraindicated (X)';
      default: return 'Unknown';
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Medicine Database
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Browse our comprehensive database of medicines with detailed information from FDA sources.
      </Typography>

      {/* Search Section */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <TextField
            fullWidth
            label="Search medicines"
            placeholder="Enter brand name, generic name, or active ingredient..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <Button
            variant="contained"
            startIcon={<Search />}
            onClick={handleSearch}
            disabled={loading}
          >
            Search
          </Button>
        </Box>
      </Paper>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Loading */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Medicines Grid */}
      {!loading && medicines.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Found {medicines.length} medicines
          </Typography>
          
          <Grid container spacing={3}>
            {medicines.map((medicine) => (
              <Grid item xs={12} sm={6} md={4} key={medicine.id}>
                <Card elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Medication color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6" component="h3">
                        {medicine.brand_name || medicine.generic_name}
                      </Typography>
                    </Box>
                    
                    {medicine.brand_name && medicine.generic_name && (
                      <Typography variant="body2" color="text.secondary" paragraph>
                        Generic: {medicine.generic_name}
                      </Typography>
                    )}
                    
                    <Typography variant="body2" paragraph>
                      <strong>Manufacturer:</strong> {medicine.manufacturer || 'N/A'}
                    </Typography>
                    
                    <Typography variant="body2" paragraph>
                      <strong>Active Ingredients:</strong> {formatText(medicine.active_ingredients)}
                    </Typography>
                    
                    <Typography variant="body2" paragraph>
                      <strong>Strength:</strong> {medicine.strength || 'N/A'}
                    </Typography>
                    
                    {medicine.pregnancy_category && (
                      <Chip
                        label={getPregnancyText(medicine.pregnancy_category)}
                        color={getPregnancyColor(medicine.pregnancy_category)}
                        size="small"
                        sx={{ mb: 1 }}
                      />
                    )}
                    
                    {medicine.indications_and_usage && (
                      <Typography variant="body2" color="text.secondary">
                        <strong>Usage:</strong> {formatText(medicine.indications_and_usage, 100)}
                      </Typography>
                    )}
                  </CardContent>
                  
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() => handleMedicineDetails(medicine)}
                    >
                      View Details
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
          
          {/* Pagination */}
          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={totalPages}
                page={currentPage}
                onChange={handlePageChange}
                color="primary"
                size="large"
              />
            </Box>
          )}
        </Box>
      )}

      {/* No Results */}
      {!loading && medicines.length === 0 && !error && (
        <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            No medicines found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search terms or browse all medicines.
          </Typography>
        </Paper>
      )}

      {/* Medicine Details Dialog */}
      <Dialog
        open={showDetails}
        onClose={() => setShowDetails(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Medication color="primary" sx={{ mr: 1 }} />
            {selectedMedicine?.brand_name || selectedMedicine?.generic_name}
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedMedicine && (
            <Box>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Basic Information
                  </Typography>
                  
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Brand Name"
                        secondary={selectedMedicine.brand_name || 'N/A'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Generic Name"
                        secondary={selectedMedicine.generic_name}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Manufacturer"
                        secondary={selectedMedicine.manufacturer || 'N/A'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Product Type"
                        secondary={selectedMedicine.product_type || 'N/A'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Active Ingredients"
                        secondary={selectedMedicine.active_ingredients || 'N/A'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Strength"
                        secondary={selectedMedicine.strength || 'N/A'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Route of Administration"
                        secondary={selectedMedicine.route_of_administration || 'N/A'}
                      />
                    </ListItem>
                  </List>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    Safety Information
                  </Typography>
                  
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Pregnancy Category"
                        secondary={
                          selectedMedicine.pregnancy_category ? 
                          getPregnancyText(selectedMedicine.pregnancy_category) : 
                          'N/A'
                        }
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Pediatric Use"
                        secondary={selectedMedicine.pediatric_use ? 'Yes' : 'No'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Geriatric Use"
                        secondary={selectedMedicine.geriatric_use ? 'Yes' : 'No'}
                      />
                    </ListItem>
                  </List>
                  
                  {selectedMedicine.tablet_shape && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        Physical Properties
                      </Typography>
                      <List dense>
                        <ListItem>
                          <ListItemText
                            primary="Tablet Shape"
                            secondary={selectedMedicine.tablet_shape}
                          />
                        </ListItem>
                        {selectedMedicine.tablet_color && (
                          <ListItem>
                            <ListItemText
                              primary="Tablet Color"
                              secondary={selectedMedicine.tablet_color}
                            />
                          </ListItem>
                        )}
                        {selectedMedicine.imprint_code && (
                          <ListItem>
                            <ListItemText
                              primary="Imprint Code"
                              secondary={selectedMedicine.imprint_code}
                            />
                          </ListItem>
                        )}
                      </List>
                    </Box>
                  )}
                </Grid>
              </Grid>
              
              <Divider sx={{ my: 3 }} />
              
              {/* Detailed Information */}
              {selectedMedicine.indications_and_usage && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Indications and Usage
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.indications_and_usage}
                  </Typography>
                </Box>
              )}
              
              {selectedMedicine.dosage_and_administration && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Dosage and Administration
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.dosage_and_administration}
                  </Typography>
                </Box>
              )}
              
              {selectedMedicine.warnings && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    <Warning sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Warnings
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.warnings}
                  </Typography>
                </Box>
              )}
              
              {selectedMedicine.adverse_reactions && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Adverse Reactions
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.adverse_reactions}
                  </Typography>
                </Box>
              )}
              
              {selectedMedicine.contraindications && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Contraindications
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.contraindications}
                  </Typography>
                </Box>
              )}
              
              {selectedMedicine.drug_interactions && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Drug Interactions
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.drug_interactions}
                  </Typography>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDetails(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MedicineDatabase;
