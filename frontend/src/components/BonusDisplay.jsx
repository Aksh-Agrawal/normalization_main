import React from "react";
import {
  Typography,
  Box,
  Paper,
  Grid,
  LinearProgress,
  CircularProgress,
  Divider,
} from "@mui/material";

function BonusDisplay({ data }) {
  const { bonus_breakdown, total_bonus, percentage } = data;
  const totalBonus =
    total_bonus ||
    Object.values(bonus_breakdown || {}).reduce((a, b) => a + b, 0);

  // Format category names for display
  const formatCategoryName = (category) => {
    return category
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  // Get color based on points value
  const getColorForPoints = (points, max = 15) => {
    const ratio = points / max;
    if (ratio < 0.3) return "#f44336"; // red
    if (ratio < 0.6) return "#ff9800"; // orange
    return "#4caf50"; // green
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Course Bonus Breakdown
      </Typography>

      <Paper sx={{ p: 3, mb: 4, bgcolor: "#f9f9f9" }} elevation={2}>
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" gutterBottom>
            Overall Completion: {percentage ? percentage.toFixed(1) : 0}%
          </Typography>
          <LinearProgress
            variant="determinate"
            value={percentage || 0}
            sx={{
              height: 10,
              borderRadius: 5,
              bgcolor: "#e0e0e0",
              "& .MuiLinearProgress-bar": {
                bgcolor:
                  percentage > 70
                    ? "#4caf50"
                    : percentage > 40
                    ? "#ff9800"
                    : "#f44336",
              },
            }}
          />
        </Box>
        <Divider sx={{ my: 2 }} />

        <Grid container spacing={3}>
          {Object.entries(bonus_breakdown || {}).map(([category, points]) => (
            <Grid item xs={12} sm={6} md={3} key={category}>
              <Paper
                sx={{
                  p: 2,
                  textAlign: "center",
                  height: "100%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  bgcolor: "white",
                }}
                elevation={1}
              >
                <Box>
                  <Typography variant="subtitle1" gutterBottom>
                    {formatCategoryName(category)}
                  </Typography>
                  <Box
                    sx={{ position: "relative", display: "inline-flex", my: 1 }}
                  >
                    <CircularProgress
                      variant="determinate"
                      value={(points / 15) * 100}
                      size={80}
                      sx={{
                        color: getColorForPoints(points),
                      }}
                    />
                    <Box
                      sx={{
                        top: 0,
                        left: 0,
                        bottom: 0,
                        right: 0,
                        position: "absolute",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <Typography
                        variant="h5"
                        component="div"
                        color="text.secondary"
                      >
                        {points.toFixed(1)}
                      </Typography>
                    </Box>
                  </Box>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  Max: 15 points
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Paper>

      <Paper
        sx={{
          p: 3,
          textAlign: "center",
          bgcolor: "#f5f5f5",
          borderTop: "4px solid #3f51b5",
        }}
        elevation={3}
      >
        <Typography variant="h6" gutterBottom>
          Total Bonus
        </Typography>
        <Typography variant="h2" color="primary">
          {totalBonus.toFixed(1)}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" sx={{ mt: 1 }}>
          Out of maximum 45 points
        </Typography>
      </Paper>
    </Box>
  );
}

export default BonusDisplay;
