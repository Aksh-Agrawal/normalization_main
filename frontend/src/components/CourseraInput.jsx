import React, { useState } from "react";
import {
  TextField,
  Button,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Paper,
  Tooltip,
} from "@mui/material";
import axios from "axios";

function CourseraInput({ onSubmit }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validate URL (simple validation)
    if (!url.includes("coursera.org")) {
      setError(
        "Please enter a valid Coursera profile URL (e.g., https://www.coursera.org/user/...)"
      );
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/api/coursera", {
        url,
      });
      onSubmit(response.data);
    } catch (err) {
      console.error("Error fetching Coursera data:", err);
      setError(
        err.response?.data?.error ||
          "Failed to fetch Coursera data. Please make sure the URL is correct and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3 }} elevation={1}>
      <Box component="form" onSubmit={handleSubmit}>
        <Typography variant="h5" gutterBottom>
          Coursera Profile Bonus Calculator
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Calculate additional bonus points based on your Coursera course
          completions. Enter your Coursera profile URL to analyze your course
          history.
        </Typography>

        <Box sx={{ display: "flex", gap: 2, alignItems: "flex-start" }}>
          <TextField
            fullWidth
            label="Coursera Profile URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={loading}
            placeholder="https://www.coursera.org/user/..."
            helperText="Enter your public Coursera profile URL"
            variant="outlined"
            InputProps={{
              sx: { bgcolor: "white" },
            }}
          />
          <Tooltip title="This will analyze your Coursera profile to calculate bonus points based on your completed courses">
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading || !url}
              sx={{ py: 1.5 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                "Calculate Bonus"
              )}
            </Button>
          </Tooltip>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {loading && (
          <Box sx={{ textAlign: "center", my: 3 }}>
            <CircularProgress />
            <Typography variant="body2" sx={{ mt: 1 }}>
              Analyzing your Coursera profile...
            </Typography>
            <Typography variant="caption" color="text.secondary">
              This may take a few moments
            </Typography>
          </Box>
        )}
      </Box>
    </Paper>
  );
}

export default CourseraInput;
