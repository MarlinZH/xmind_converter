import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  Stepper, 
  Step, 
  StepLabel,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CredentialsStep from './CredentialsStep';
import FileSelectionStep from './FileSelectionStep';
import ConversionStep from './ConversionStep';
import { ipcRenderer } from 'electron';

const steps = ['Notion Credentials', 'Select XMind File', 'Convert'];

const StyledPaper = styled(Paper)(({ theme }) => ({
  marginTop: theme.spacing(3),
  marginBottom: theme.spacing(3),
  padding: theme.spacing(2),
  [theme.breakpoints.up(600)]: {
    marginTop: theme.spacing(6),
    marginBottom: theme.spacing(6),
    padding: theme.spacing(3),
  },
}));

const App: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [credentials, setCredentials] = useState({ token: '', databaseId: '' });
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [conversionStatus, setConversionStatus] = useState<'idle' | 'converting' | 'success' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load saved credentials
    const loadCredentials = async () => {
      const savedCredentials = await ipcRenderer.invoke('get-credentials');
      if (savedCredentials) {
        setCredentials(savedCredentials);
      }
    };
    loadCredentials();
  }, []);

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleCredentialsSubmit = async (newCredentials: { token: string; databaseId: string }) => {
    await ipcRenderer.invoke('save-credentials', newCredentials);
    setCredentials(newCredentials);
    handleNext();
  };

  const handleFileSelect = (filePath: string) => {
    setSelectedFile(filePath);
    handleNext();
  };

  const handleConvert = async () => {
    if (!selectedFile || !credentials.databaseId) {
      setError('Missing required information');
      return;
    }

    setConversionStatus('converting');
    try {
      const result = await ipcRenderer.invoke('convert-xmind', {
        filePath: selectedFile,
        databaseId: credentials.databaseId,
      });

      if (result.success) {
        setConversionStatus('success');
      } else {
        setError(result.error);
        setConversionStatus('error');
      }
    } catch (err) {
      setError(err.message);
      setConversionStatus('error');
    }
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 0:
        return <CredentialsStep onSubmit={handleCredentialsSubmit} initialValues={credentials} />;
      case 1:
        return <FileSelectionStep onFileSelect={handleFileSelect} />;
      case 2:
        return (
          <ConversionStep
            filePath={selectedFile}
            onConvert={handleConvert}
            status={conversionStatus}
            error={error}
          />
        );
      default:
        return 'Unknown step';
    }
  };

  return (
    <Container maxWidth="md">
      <StyledPaper elevation={3}>
        <Typography component="h1" variant="h4" align="center" gutterBottom>
          XMind to Notion Converter
        </Typography>
        <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Box sx={{ mt: 2 }}>
          {getStepContent(activeStep)}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Back
            </Button>
            {activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                color="primary"
                onClick={handleConvert}
                disabled={conversionStatus === 'converting'}
              >
                {conversionStatus === 'converting' ? (
                  <CircularProgress size={24} />
                ) : (
                  'Convert'
                )}
              </Button>
            ) : null}
          </Box>
        </Box>
      </StyledPaper>
    </Container>
  );
};

export default App; 