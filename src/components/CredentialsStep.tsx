import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Link,
} from '@mui/material';

interface CredentialsStepProps {
  onSubmit: (credentials: { token: string; databaseId: string }) => void;
  initialValues: { token: string; databaseId: string };
}

const CredentialsStep: React.FC<CredentialsStepProps> = ({ onSubmit, initialValues }) => {
  const [token, setToken] = useState(initialValues.token);
  const [databaseId, setDatabaseId] = useState(initialValues.databaseId);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ token, databaseId });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Notion API Credentials
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        To get your Notion API token and database ID:
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        1. Create an integration at{' '}
        <Link href="https://www.notion.so/my-integrations" target="_blank" rel="noopener">
          Notion Integrations
        </Link>
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        2. Share your database with the integration
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        3. Copy the integration token and database ID
      </Typography>

      <TextField
        required
        fullWidth
        label="Notion API Token"
        value={token}
        onChange={(e) => setToken(e.target.value)}
        margin="normal"
        helperText="Your Notion integration token"
      />

      <TextField
        required
        fullWidth
        label="Database ID"
        value={databaseId}
        onChange={(e) => setDatabaseId(e.target.value)}
        margin="normal"
        helperText="The ID of your Notion database"
      />

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={!token || !databaseId}
        >
          Next
        </Button>
      </Box>
    </Box>
  );
};

export default CredentialsStep; 