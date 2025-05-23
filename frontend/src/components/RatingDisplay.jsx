import React from "react";
import { Typography, Grid, Paper, Box, Divider, Chip } from "@mui/material";

function RatingDisplay({ data }) {
  // Function to get color based on rating
  const getRatingColor = (platform, rating) => {
    if (!rating) return "#757575"; // Default gray for N/A

    if (platform === "codeforces") {
      if (rating < 1200) return "#808080"; // Gray (Newbie)
      if (rating < 1400) return "#008000"; // Green (Pupil)
      if (rating < 1600) return "#03A89E"; // Cyan (Specialist)
      if (rating < 1900) return "#0000FF"; // Blue (Expert)
      if (rating < 2100) return "#AA00AA"; // Violet (Candidate Master)
      if (rating < 2400) return "#FF8C00"; // Orange (Master)
      return "#FF0000"; // Red (Grandmaster)
    }

    if (platform === "leetcode") {
      if (rating < 1500) return "#808080"; // Gray
      if (rating < 1800) return "#008000"; // Green
      if (rating < 2000) return "#0000FF"; // Blue
      if (rating < 2200) return "#AA00AA"; // Violet
      return "#FF8C00"; // Orange
    }

    if (platform === "codechef") {
      if (rating < 1800) return "#808080"; // Gray
      if (rating < 2000) return "#008000"; // Green
      if (rating < 2200) return "#0000FF"; // Blue
      if (rating < 2500) return "#AA00AA"; // Violet
      return "#FF8C00"; // Orange
    }

    return "#757575"; // Default
  };

  // Get platforms and their weights
  const platforms = Object.keys(data.platform_ratings);
  const weights = data.platform_weights || {};

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Platform Ratings
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {platforms.map((platform) => {
          const platformData = data.platform_ratings[platform];
          const rating = platformData?.rating;
          const color = getRatingColor(platform, rating);

          return (
            <Grid item xs={12} sm={6} md={3} key={platform}>
              <Paper
                sx={{
                  p: 2,
                  textAlign: "center",
                  borderTop: `4px solid ${color}`,
                }}
                elevation={3}
              >
                <Typography variant="h6" gutterBottom>
                  {platform.charAt(0).toUpperCase() + platform.slice(1)}
                </Typography>
                <Typography variant="h4" sx={{ color }}>
                  {rating || "N/A"}
                </Typography>
                <Chip
                  label={`Weight: ${(
                    weights[platform.toUpperCase()] || 0
                  ).toFixed(2)}`}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </Paper>
            </Grid>
          );
        })}
      </Grid>

      <Divider sx={{ my: 3 }} />

      <Paper
        sx={{ p: 3, textAlign: "center", bgcolor: "#f5f5f5" }}
        elevation={2}
      >
        <Typography variant="h5" gutterBottom>
          Unified Rating
        </Typography>
        <Typography variant="h2" color="primary">
          {data.unified_rating ? data.unified_rating.toFixed(1) : "N/A"}
        </Typography>
      </Paper>
    </Box>
  );
}

export default RatingDisplay;
