import React, { useState, useEffect } from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import { Search, Clear } from "@mui/icons-material";
import InputAdornment from "@mui/material/InputAdornment";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import CloseIcon from "@mui/icons-material/Close";
import Button from "@mui/material/Button";

const App = () => {
  const [searchText, setSearchText] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [data, setData] = useState(null); // State variable for data
  const [value, setValue] = useState(0);
  const [expandedCard, setExpandedCard] = useState([]);
  const [activeButton, setActiveButton] = useState([]);

  useEffect(() => {
    // Fetch data from API when component mounts
    fetch("http://localhost:8000/")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error(error));
  }, []);

  const handleSearchChange = (event) => {
    setSearchText(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    fetchData(searchText);
  };

  const fetchData = (searchText) => {
    fetch("http://localhost:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ value: searchText }),
    })
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error(error));
  };

  const handleSearchClear = () => {
    setSearchText("");
  };

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleTabClick = (index, section) => {
    setExpandedCard((prevExpandedCard) => {
      let newExpandedCard = [...prevExpandedCard];
      let newActiveButton = [...activeButton]; // copy the current state

      if (!newExpandedCard[index]) {
        newExpandedCard[index] = {};
      }

      // If the clicked section is already open, close it
      if (newExpandedCard[index].openSection === section) {
        newExpandedCard[index].openSection = null;
        newActiveButton[index] = null; // no active button if section is closed
      } else {
        // Otherwise, open the clicked section and close any others
        newExpandedCard[index].openSection = section;
        newActiveButton[index] = section; // update active button
      }

      setActiveButton(newActiveButton); // set the new state
      return newExpandedCard;
    });
  };

  return (
    <Box style={{ height: "100%" }}>
      <AppBar position="static" style={{ backgroundColor: "green" }}>
        <Toolbar>Social Media Post Generator</Toolbar>
      </AppBar>
      <Box display="flex" p={2} style={{ height: "100%" }}>
        <Box flexBasis="60%" borderRight={1} borderColor="grey.500" ml={2}>
          <Box
            display="block"
            justifyContent="center"
            alignItems="top"
            style={{ height: "100%" }}
          >
            <Box display="flex" flexDirection="column">
              <form onSubmit={handleSearchSubmit}>
                <TextField
                  style={{ marginLeft: "100px", width: "70%" }}
                  fullWidth
                  placeholder="Search articles"
                  value={searchText}
                  onChange={handleSearchChange}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        {searchText && (
                          <IconButton onClick={handleSearchClear}>
                            <Clear />
                          </IconButton>
                        )}
                      </InputAdornment>
                    ),
                    startAdornment: searchText ? (
                      <InputAdornment position="start">
                        <Search />
                      </InputAdornment>
                    ) : null,
                  }}
                />
              </form>
              <Box alignSelf="flex-end" width="20%" mt={2}>
                <Select
                  value={selectedOption}
                  onChange={handleSelectChange}
                  displayEmpty
                  inputProps={{ "aria-label": "Without label" }}
                  sx={{ height: "30px", width: "100px", fontSize: "0.875rem" }}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  <MenuItem value={10}>Option 1</MenuItem>
                  <MenuItem value={20}>Option 2</MenuItem>
                  <MenuItem value={30}>Option 3</MenuItem>
                </Select>
              </Box>
              <Box alignSelf="center" flexDirection="column" width="80%">
                {Array.isArray(data) &&
                  data.map((item, index) => (
                    <Card sx={{ mt: 2 }} key={index}>
                      <CardContent>
                        <Typography variant="body1">{item.headline}</Typography>
                      </CardContent>
                      <CardActions
                        disableSpacing
                        alignSelf="center"
                        display="block"
                      >
                        <Button
                          style={
                            activeButton[index] === "summary"
                              ? { backgroundColor: "lightgray", color: "black" }
                              : { color: "black" }
                          }
                          onClick={() => handleTabClick(index, "summary")}
                        >
                          Summary
                        </Button>
                        <Button
                          style={
                            activeButton[index] === "article"
                              ? { backgroundColor: "lightgray", color: "black" }
                              : { color: "black" }
                          }
                          onClick={() => handleTabClick(index, "article")}
                        >
                          Article
                        </Button>
                        <Button
                          style={
                            activeButton[index] === "ai_summary"
                              ? { backgroundColor: "lightgray", color: "black" }
                              : { color: "black" }
                          }
                          onClick={() => handleTabClick(index, "ai_summary")}
                        >
                          AI Summary
                        </Button>
                      </CardActions>
                      <Collapse
                        in={expandedCard[index]?.openSection === "summary"}
                        timeout="auto"
                        unmountOnExit
                      >
                        <CardContent>
                          <Typography paragraph>{item.summary}</Typography>
                        </CardContent>
                      </Collapse>
                      <Collapse
                        in={expandedCard[index]?.openSection === "article"}
                        timeout="auto"
                        unmountOnExit
                      >
                        <CardContent>
                          <Typography paragraph>{item.article}</Typography>
                        </CardContent>
                      </Collapse>
                      <Collapse
                        in={expandedCard[index]?.openSection === "ai_summary"}
                        timeout="auto"
                        unmountOnExit
                      >
                        <CardContent>
                          <Typography paragraph>{item.ai_summary}</Typography>
                        </CardContent>
                      </Collapse>
                    </Card>
                  ))}
              </Box>
            </Box>
          </Box>
        </Box>
        <Box flexBasis="20%" ml={2}>
          Post Generator
        </Box>
      </Box>
    </Box>
  );
};

export default App;
