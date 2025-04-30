import React from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
} from '@mui/material';
import { ipcRenderer } from 'electron';

interface FileSelectionStepProps {
  onFileSelect: (filePath: string) => void;
}

const FileSelectionStep: React.FC<FileSelectionStepProps> = ({ onFileSelect }) => {
  const handleFileSelect = async () => {
    try {
      const result = await ipcRenderer.invoke('select-file');
      if (result.filePath) {
        onFileSelect(result.filePath);
      }
    } catch (error) {
      console.error('Error selecting file:', error);
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Select XMind File
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Choose the XMind file you want to convert to Notion
      </Typography>

      <Paper
        variant="outlined"
        sx={{
          p: 3,
          mt: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          cursor: 'pointer',
        }}
        onClick={handleFileSelect}
      >
        <Button
          variant="contained"
          component="span"
          sx={{ mb: 2 }}
        >
          Select XMind File
        </Button>
        <Typography variant="body2" color="text.secondary">
          Click to choose an XMind file (.xmind)
        </Typography>
      </Paper>
    </Box>
  );
};

export default FileSelectionStep; 