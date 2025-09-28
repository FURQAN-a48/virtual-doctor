import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Chip,
  Grid,
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  FormGroup
} from '@mui/material';
import {
  Add,
  Remove,
  LocalHospital,
  Warning,
  CheckCircle,
  Chat
} from '@mui/icons-material';
import { apiService } from '../services/apiService';

const SymptomChecker = () => {
  const [symptoms, setSymptoms] = useState([]);
  const [availableSymptoms, setAvailableSymptoms] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [availableConditions, setAvailableConditions] = useState([]);
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [severity, setSeverity] = useState('moderate');
  const [recommendations, setRecommendations] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatMode, setChatMode] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedMedicine, setSelectedMedicine] = useState(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [symptomsData, conditionsData] = await Promise.all([
        apiService.getSymptoms(),
        apiService.getConditions()
      ]);
      setAvailableSymptoms(symptomsData);
      setAvailableConditions(conditionsData);
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  };

  const handleSymptomToggle = (symptom) => {
    setSymptoms(prev => 
      prev.includes(symptom.name) 
        ? prev.filter(s => s !== symptom.name)
        : [...prev, symptom.name]
    );
  };

  const handleConditionToggle = (condition) => {
    setConditions(prev => 
      prev.includes(condition.name) 
        ? prev.filter(c => c !== condition.name)
        : [...prev, condition.name]
    );
  };

  const handleGetRecommendations = async () => {
    if (symptoms.length === 0) {
      alert('Please select at least one symptom');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.getRecommendations({
        symptoms,
        conditions,
        age: age ? parseInt(age) : null,
        gender: gender || null,
        severity
      });

      setRecommendations(response.recommendations || []);
      setWarnings(response.warnings || []);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      alert('Error getting recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChatSubmit = async () => {
    if (!chatMessage.trim()) return;

    const userMessage = { type: 'user', message: chatMessage };
    setChatHistory(prev => [...prev, userMessage]);
    setChatMessage('');

    try {
      const response = await apiService.chatWithDoctor({
        message: chatMessage,
        history: chatHistory
      });

      const botMessage = { type: 'bot', ...response };
      setChatHistory(prev => [...prev, botMessage]);

      // Update symptoms if found
      if (response.symptoms_found && response.symptoms_found.length > 0) {
        setSymptoms(prev => [...new Set([...prev, ...response.symptoms_found])]);
      }

      // Update patient info
      if (response.patient_info) {
        if (response.patient_info.age) setAge(response.patient_info.age.toString());
        if (response.patient_info.gender) setGender(response.patient_info.gender);
        if (response.patient_info.conditions) {
          setConditions(prev => [...new Set([...prev, ...response.patient_info.conditions])]);
        }
      }

    } catch (error) {
      console.error('Error in chat:', error);
      const errorMessage = { type: 'bot', message: 'Sorry, I encountered an error. Please try again.' };
      setChatHistory(prev => [...prev, errorMessage]);
    }
  };

  const handleMedicineDetails = (medicine) => {
    setSelectedMedicine(medicine);
    setShowDetails(true);
  };

  const clearAll = () => {
    setSymptoms([]);
    setConditions([]);
    setAge('');
    setGender('');
    setSeverity('moderate');
    setRecommendations([]);
    setWarnings([]);
    setChatHistory([]);
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Symptom Checker
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Describe your symptoms and get personalized medicine recommendations based on your medical history.
      </Typography>

      {/* Chat Mode Toggle */}
      <Box sx={{ mb: 3 }}>
        <Button
          variant={chatMode ? "contained" : "outlined"}
          startIcon={<Chat />}
          onClick={() => setChatMode(!chatMode)}
        >
          {chatMode ? 'Switch to Form Mode' : 'Switch to Chat Mode'}
        </Button>
      </Box>

      {chatMode ? (
        /* Chat Interface */
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Chat with Virtual Doctor
          </Typography>
          <Box sx={{ height: 400, overflowY: 'auto', mb: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
            {chatHistory.map((msg, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: msg.type === 'user' ? 'flex-end' : 'flex-start',
                  mb: 2
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    bgcolor: msg.type === 'user' ? 'primary.main' : 'white',
                    color: msg.type === 'user' ? 'white' : 'text.primary'
                  }}
                >
                  <Typography variant="body2">{msg.message}</Typography>
                  {msg.recommendations && msg.recommendations.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Recommendations:
                      </Typography>
                      {msg.recommendations.slice(0, 3).map((rec, idx) => (
                        <Chip
                          key={idx}
                          label={rec.medicine.brand_name || rec.medicine.generic_name}
                          size="small"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
                    </Box>
                  )}
                </Paper>
              </Box>
            ))}
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              placeholder="Describe your symptoms..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleChatSubmit()}
            />
            <Button variant="contained" onClick={handleChatSubmit}>
              Send
            </Button>
          </Box>
        </Paper>
      ) : (
        /* Form Interface */
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Select Symptoms
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {symptoms.map((symptom) => (
                  <Chip
                    key={symptom}
                    label={symptom}
                    onDelete={() => handleSymptomToggle({ name: symptom })}
                    color="primary"
                  />
                ))}
              </Box>
              <FormGroup>
                {availableSymptoms.map((symptom) => (
                  <FormControlLabel
                    key={symptom.id}
                    control={
                      <Checkbox
                        checked={symptoms.includes(symptom.name)}
                        onChange={() => handleSymptomToggle(symptom)}
                      />
                    }
                    label={symptom.name}
                  />
                ))}
              </FormGroup>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Medical Conditions
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                {conditions.map((condition) => (
                  <Chip
                    key={condition}
                    label={condition}
                    onDelete={() => handleConditionToggle({ name: condition })}
                    color="secondary"
                  />
                ))}
              </Box>
              <FormGroup>
                {availableConditions.map((condition) => (
                  <FormControlLabel
                    key={condition.id}
                    control={
                      <Checkbox
                        checked={conditions.includes(condition.name)}
                        onChange={() => handleConditionToggle(condition)}
                      />
                    }
                    label={condition.name}
                  />
                ))}
              </FormGroup>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Patient Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Age"
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    placeholder="Enter your age"
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth>
                    <InputLabel>Gender</InputLabel>
                    <Select
                      value={gender}
                      onChange={(e) => setGender(e.target.value)}
                    >
                      <MenuItem value="">Not specified</MenuItem>
                      <MenuItem value="male">Male</MenuItem>
                      <MenuItem value="female">Female</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <FormControl fullWidth>
                    <InputLabel>Severity</InputLabel>
                    <Select
                      value={severity}
                      onChange={(e) => setSeverity(e.target.value)}
                    >
                      <MenuItem value="mild">Mild</MenuItem>
                      <MenuItem value="moderate">Moderate</MenuItem>
                      <MenuItem value="severe">Severe</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', gap: 2, mt: 3, mb: 3 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<LocalHospital />}
          onClick={handleGetRecommendations}
          disabled={loading || symptoms.length === 0}
        >
          {loading ? <CircularProgress size={24} /> : 'Get Recommendations'}
        </Button>
        <Button
          variant="outlined"
          onClick={clearAll}
        >
          Clear All
        </Button>
      </Box>

      {/* Warnings */}
      {warnings.length > 0 && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Important Warnings:
          </Typography>
          {warnings.map((warning, index) => (
            <Typography key={index} variant="body2">
              • {warning}
            </Typography>
          ))}
        </Alert>
      )}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Recommendations ({recommendations.length})
          </Typography>
          <Grid container spacing={3}>
            {recommendations.map((rec, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card elevation={3}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {rec.medicine.brand_name || rec.medicine.generic_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {rec.medicine.generic_name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Typography variant="body2" sx={{ mr: 2 }}>
                        Effectiveness: {Math.round(rec.effectiveness * 100)}%
                      </Typography>
                      <Typography variant="body2">
                        Score: {rec.score.toFixed(2)}
                      </Typography>
                    </Box>
                    {rec.safety_warnings.length > 0 && (
                      <Alert severity="warning" sx={{ mb: 2 }}>
                        {rec.safety_warnings.map((warning, idx) => (
                          <Typography key={idx} variant="body2">
                            • {warning}
                          </Typography>
                        ))}
                      </Alert>
                    )}
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() => handleMedicineDetails(rec.medicine)}
                    >
                      View Details
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

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

export default SymptomChecker;
