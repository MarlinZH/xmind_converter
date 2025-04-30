import React from 'react';
import {
  Box,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material';

interface ConversionStepProps {
  filePath: string | null;
  onConvert: () => void;
  status: 'idle' | 'converting' | 'success' | 'error';
  error: string | null;
}

const ConversionStep: React.FC<ConversionStepProps> = ({
  filePath,
  onConvert,
  status,
  error,
}) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Convert to Notion
      </Typography>

      {filePath && (
        <Typography variant="body1" paragraph>
          Selected file: {filePath}
        </Typography>
      )}

      {status === 'converting' && (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 3 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            Converting your XMind file to Notion...
          </Typography>
        </Box>
      )}

      {status === 'success' && (
        <Alert severity="success" sx={{ mt: 2 }}>
          Conversion completed successfully! Your XMind content has been imported to Notion.
        </Alert>
      )}

      {status === 'error' && error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Error during conversion: {error}
        </Alert>
      )}

      {status === 'idle' && (
        <Typography variant="body2" color="text.secondary" paragraph>
          Click the Convert button to start the conversion process.
        </Typography>
      )}
    </Box>
  );
};

export default ConversionStep; 