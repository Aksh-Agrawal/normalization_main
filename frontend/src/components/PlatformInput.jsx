import React, { useState } from "react";
import {
  TextField,
  Button,
  Grid,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import axios from "axios";

function PlatformInput({ onSubmit }) {
  const [handles, setHandles] = useState({
    codeforces: "",
    leetcode: "",
    codechef: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (!handles.codeforces && !handles.leetcode && !handles.codechef) {
      setError("Please enter at least one platform handle");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5000/api/analyze",
        handles
      );
      onSubmit(response.data);
    } catch (error) {
      console.error("Error:", error);
      setError(
        error.response?.data?.error ||
          "Failed to analyze profiles. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Typography variant="h5" gutterBottom>
        Enter Your Coding Platform Handles
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label="Codeforces Handle"
            value={handles.codeforces}
            onChange={(e) =>
              setHandles({ ...handles, codeforces: e.target.value })
            }
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label="LeetCode Handle"
            value={handles.leetcode}
            onChange={(e) =>
              setHandles({ ...handles, leetcode: e.target.value })
            }
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label="CodeChef Handle"
            value={handles.codechef}
            onChange={(e) =>
              setHandles({ ...handles, codechef: e.target.value })
            }
          />
        </Grid>{" "}
        <Grid item xs={12}>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
            disabled={loading}
          >
            {loading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              "Analyze Profiles"
            )}
          </Button>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </Grid>
      </Grid>
    </form>
  );
}

export default PlatformInput;
