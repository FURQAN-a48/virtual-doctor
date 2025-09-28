import React, { useState, useRef } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Card,
  CardContent,
  CardActions,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  CloudUpload,
  CameraAlt,
  Medication,
  CheckCircle,
  Warning,
  Info
} from '@mui/icons-material';
import { apiService } from '../services/apiService';

const TabletRecognition = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedMedicine, setSelectedMedicine] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setResult(null);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleIdentify = async () => {
    if (!selectedFile) {
      alert('Please select an image first');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await apiService.identifyTablet(formData);
      setResult(response);
    } catch (error) {
      console.error('Error identifying tablet:', error);
      alert('Error identifying tablet. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleMedicineDetails = (medicine) => {
    setSelectedMedicine(medicine);
    setShowDetails(true);
  };

  const clearImage = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Tablet Recognition
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload a photo of any tablet to identify the medicine and get detailed information.
      </Typography>

      {/* Upload Area */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          mb: 3,
          border: '2px dashed #ccc',
          borderRadius: 2,
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'border-color 0.3s',
          '&:hover': {
            borderColor: 'primary.main'
          }
        }}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        {preview ? (
          <Box>
            <img
              src={preview}
              alt="Preview"
              style={{
                maxWidth: '100%',
                maxHeight: 300,
                borderRadius: 8,
                marginBottom: 16
              }}
            />
            <Typography variant="h6" gutterBottom>
              {selectedFile?.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Click to change image or drag and drop a new one
            </Typography>
          </Box>
        ) : (
          <Box>
            <CloudUpload sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Upload Tablet Image
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Click to select an image or drag and drop it here
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Supported formats: JPG, PNG, GIF
            </Typography>
          </Box>
        )}
      </Paper>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={loading ? <CircularProgress size={24} /> : <CameraAlt />}
          onClick={handleIdentify}
          disabled={!selectedFile || loading}
        >
          {loading ? 'Identifying...' : 'Identify Tablet'}
        </Button>
        <Button
          variant="outlined"
          onClick={clearImage}
          disabled={!selectedFile}
        >
          Clear Image
        </Button>
      </Box>

      {/* Results */}
      {result && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Identification Results
          </Typography>
          
          {result.success ? (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card elevation={3}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <CheckCircle color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {result.medicine_name}
                      </Typography>
                    </Box>
                    
                    <Chip
                      label={getConfidenceText(result.confidence)}
                      color={getConfidenceColor(result.confidence)}
                      sx={{ mb: 2 }}
                    />
                    
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </Typography>
                    
                    {result.medicine_info && (
                      <Box>
                        <Typography variant="subtitle2" gutterBottom>
                          Medicine Information:
                        </Typography>
                        <List dense>
                          <ListItem>
                            <ListItemIcon>
                              <Medication />
                            </ListItemIcon>
                            <ListItemText
                              primary="Generic Name"
                              secondary={result.medicine_info.generic_name}
                            />
                          </ListItem>
                          {result.medicine_info.manufacturer && (
                            <ListItem>
                              <ListItemIcon>
                                <Info />
                              </ListItemIcon>
                              <ListItemText
                                primary="Manufacturer"
                                secondary={result.medicine_info.manufacturer}
                              />
                            </ListItem>
                          )}
                          {result.medicine_info.strength && (
                            <ListItem>
                              <ListItemIcon>
                                <Info />
                              </ListItemIcon>
                              <ListItemText
                                primary="Strength"
                                secondary={result.medicine_info.strength}
                              />
                            </ListItem>
                          )}
                        </List>
                      </Box>
                    )}
                  </CardContent>
                  <CardActions>
                    {result.medicine_info && (
                      <Button
                        size="small"
                        onClick={() => handleMedicineDetails(result.medicine_info)}
                      >
                        View Full Details
                      </Button>
                    )}
                  </CardActions>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper elevation={2} sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Recognition Details
                  </Typography>
                  
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Status"
                        secondary={result.success ? 'Successfully identified' : 'Identification failed'}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Confidence Score"
                        secondary={`${(result.confidence * 100).toFixed(1)}%`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Medicine ID"
                        secondary={result.medicine_id || 'Not found in database'}
                      />
                    </ListItem>
                  </List>
                  
                  {result.all_predictions && result.all_predictions.length > 1 && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        All Predictions:
                      </Typography>
                      {result.all_predictions.map((pred, index) => (
                        <Typography key={index} variant="body2">
                          Class {index}: {(pred * 100).toFixed(1)}%
                        </Typography>
                      ))}
                    </Box>
                  )}
                </Paper>
              </Grid>
            </Grid>
          ) : (
            <Alert severity="error">
              <Typography variant="h6" gutterBottom>
                Identification Failed
              </Typography>
              <Typography variant="body2">
                {result.error || 'Unable to identify the tablet. Please try with a clearer image.'}
              </Typography>
            </Alert>
          )}
        </Box>
      )}

      {/* Tips */}
      <Paper elevation={1} sx={{ p: 3, mt: 3, bgcolor: 'info.light' }}>
        <Typography variant="h6" gutterBottom>
          <Info sx={{ mr: 1, verticalAlign: 'middle' }} />
          Tips for Better Recognition
        </Typography>
        <List dense>
          <ListItem>
            <ListItemText
              primary="• Use good lighting and avoid shadows"
              secondary="Natural light works best for tablet recognition"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="• Ensure the tablet is clearly visible"
              secondary="Avoid blurry or partially obscured images"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="• Include the tablet imprint if visible"
              secondary="Text or numbers on the tablet help with identification"
            />
          </ListItem>
          <ListItem>
            <ListItemText
              primary="• Use a plain background"
              secondary="Contrasting backgrounds improve recognition accuracy"
            />
          </ListItem>
        </List>
      </Paper>

      {/* Medicine Details Dialog */}
      <Dialog
        open={showDetails}
        onClose={() => setShowDetails(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedMedicine?.brand_name || selectedMedicine?.generic_name}
        </DialogTitle>
        <DialogContent>
          {selectedMedicine && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Generic Name: {selectedMedicine.generic_name}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Manufacturer:</strong> {selectedMedicine.manufacturer || 'N/A'}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Active Ingredients:</strong> {selectedMedicine.active_ingredients || 'N/A'}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Strength:</strong> {selectedMedicine.strength || 'N/A'}
              </Typography>
              {selectedMedicine.indications_and_usage && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Indications and Usage:
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.indications_and_usage}
                  </Typography>
                </Box>
              )}
              {selectedMedicine.dosage_and_administration && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Dosage and Administration:
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.dosage_and_administration}
                  </Typography>
                </Box>
              )}
              {selectedMedicine.warnings && (
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    Warnings:
                  </Typography>
                  <Typography variant="body2" paragraph>
                    {selectedMedicine.warnings}
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

export default TabletRecognition;
