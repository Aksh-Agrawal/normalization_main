import React, { useState } from "react";
import {
  Container,
  Paper,
  Typography,
  Box,
  AppBar,
  Toolbar,
  Stepper,
  Step,
  StepLabel,
  Button,
  Card,
  CardContent,
  Divider,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from "@mui/material";
import PlatformInput from "./components/PlatformInput";
import RatingDisplay from "./components/RatingDisplay";
import ActivityHeatmap from "./components/ActivityHeatmap";
import CourseraInput from "./components/CourseraInput";
import BonusDisplay from "./components/BonusDisplay";

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5",
    },
    secondary: {
      main: "#f50057",
    },
    background: {
      default: "#f5f5f5",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h3: {
      fontWeight: 500,
    },
    h5: {
      fontWeight: 500,
      marginBottom: "16px",
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

function App() {
  const [userData, setUserData] = useState(null);
  const [courseBonus, setCourseBonus] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  // Calculate the total score if both userData and courseBonus are available
  const totalScore =
    userData && courseBonus
      ? userData.unified_rating + courseBonus.total_bonus
      : null;

  // Handle step changes
  const handleNext = () => {
    setActiveStep((prevStep) => (prevStep < 2 ? prevStep + 1 : prevStep));
  };

  const handleBack = () => {
    setActiveStep((prevStep) => (prevStep > 0 ? prevStep - 1 : prevStep));
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  // Handle user data submission
  const handleUserDataSubmit = (data) => {
    setUserData(data);
    handleNext(); // Move to next step automatically
  };

  // Handle course bonus submission
  const handleCourseBonusSubmit = (data) => {
    setCourseBonus(data);
    handleNext(); // Move to next step automatically
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" color="primary" elevation={0}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Coding Profile Analyzer
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            align="center"
            sx={{ mb: 4 }}
          >
            Unified Rating System
          </Typography>

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            <Step>
              <StepLabel>Platform Analysis</StepLabel>
            </Step>
            <Step>
              <StepLabel>Course Bonus</StepLabel>
            </Step>
            <Step>
              <StepLabel>Final Results</StepLabel>
            </Step>
          </Stepper>

          {activeStep === 0 && (
            <Card sx={{ mb: 3, overflow: "visible" }} elevation={2}>
              <CardContent>
                <PlatformInput onSubmit={handleUserDataSubmit} />
              </CardContent>
            </Card>
          )}

          {activeStep === 1 && userData && (
            <>
              <Card sx={{ mb: 3 }} elevation={2}>
                <CardContent>
                  <RatingDisplay data={userData} />
                </CardContent>
              </Card>

              <Card sx={{ mb: 3 }} elevation={2}>
                <CardContent>
                  <ActivityHeatmap data={userData} />
                </CardContent>
              </Card>

              <Card sx={{ mb: 3, overflow: "visible" }} elevation={2}>
                <CardContent>
                  <CourseraInput onSubmit={handleCourseBonusSubmit} />
                </CardContent>
              </Card>
            </>
          )}

          {activeStep === 2 && userData && courseBonus && (
            <>
              <Card sx={{ mb: 3 }} elevation={2}>
                <CardContent>
                  <BonusDisplay data={courseBonus} />
                </CardContent>
              </Card>

              <Card sx={{ mb: 3 }} elevation={3}>
                <CardContent sx={{ textAlign: "center" }}>
                  <Typography variant="h4" gutterBottom color="primary">
                    Final Result
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-around",
                      flexWrap: "wrap",
                      gap: 2,
                    }}
                  >
                    <Box>
                      <Typography variant="h6" color="text.secondary">
                        Platform Rating
                      </Typography>
                      <Typography variant="h3" color="primary">
                        {userData.unified_rating.toFixed(1)}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h1" color="text.secondary">
                        +
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="text.secondary">
                        Course Bonus
                      </Typography>
                      <Typography variant="h3" color="secondary">
                        {courseBonus.total_bonus.toFixed(1)}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h1" color="text.secondary">
                        =
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="h6" color="text.secondary">
                        Total Score
                      </Typography>
                      <Typography variant="h2" sx={{ fontWeight: "bold" }}>
                        {totalScore.toFixed(1)}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </>
          )}

          <Box sx={{ display: "flex", flexDirection: "row", pt: 2 }}>
            <Button
              color="inherit"
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Back
            </Button>
            <Box sx={{ flex: "1 1 auto" }} />
            {activeStep !== 2 ? (
              <Button
                onClick={handleNext}
                disabled={
                  (activeStep === 0 && !userData) ||
                  (activeStep === 1 && !userData)
                }
              >
                Next
              </Button>
            ) : (
              <Button onClick={handleReset}>Restart</Button>
            )}
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
