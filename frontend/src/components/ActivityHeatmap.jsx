import React, { useMemo } from "react";
import { Typography, Box, Paper, CircularProgress } from "@mui/material";
import { ResponsiveCalendar } from "@nivo/calendar";

function ActivityHeatmap({ data }) {
  const heatmapData = useMemo(() => {
    if (!data.heatmap_data || data.heatmap_data.length === 0) {
      return [];
    }

    return data.heatmap_data.map((entry) => ({
      day: entry.date,
      value: entry.count,
    }));
  }, [data.heatmap_data]);

  // Calculate date range for the calendar - last 12 months
  const today = new Date();
  const toDate = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate()
  );
  const fromDate = new Date(
    today.getFullYear() - 1,
    today.getMonth(),
    today.getDate()
  );

  if (heatmapData.length === 0) {
    return (
      <Box>
        <Typography variant="h5" gutterBottom>
          Coding Activity
        </Typography>
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <Typography color="textSecondary">
            No activity data available
          </Typography>
        </Paper>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Coding Activity
      </Typography>
      <Paper elevation={1} sx={{ p: 2, bgcolor: "#fafafa" }}>
        <Box sx={{ height: 400 }}>
          <ResponsiveCalendar
            data={heatmapData}
            from={fromDate}
            to={toDate}
            emptyColor="#eeeeee"
            colors={["#9be9a8", "#40c463", "#30a14e", "#216e39"]} // GitHub style colors
            margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
            yearSpacing={40}
            monthBorderColor="#ffffff"
            dayBorderWidth={2}
            dayBorderColor="#ffffff"
            legends={[
              {
                anchor: "bottom-right",
                direction: "row",
                translateY: 36,
                itemCount: 4,
                itemWidth: 42,
                itemHeight: 36,
                itemsSpacing: 14,
                itemDirection: "right-to-left",
              },
            ]}
            tooltip={(data) => (
              <Box
                sx={{
                  backgroundColor: "white",
                  p: 1,
                  borderRadius: 1,
                  boxShadow: "0 2px 5px rgba(0,0,0,0.15)",
                }}
              >
                <Typography variant="body2">
                  {data.day}: {data.value} contributions
                </Typography>
              </Box>
            )}
          />
        </Box>
      </Paper>
    </Box>
  );
}

export default ActivityHeatmap;
