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

const App = () => {
  const [searchText, setSearchText] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [data, setData] = useState(null); // State variable for data

  useEffect(() => {
    // Fetch data from API when component mounts
    fetch("https://newsapi.org/v2/everything?q=tesla&from=2023-05-23&sortBy=publishedAt&apiKey=623042cedc12401eb8cf268e0bb86a84")
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error(error));
  }, []);

  const handleSearchChange = (event) => {
    setSearchText(event.target.value);
  };

  const handleSearchClear = () => {
    setSearchText("");
  };

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  return (
    <Box style={{height: "100%"}}>
      <AppBar position="static" style={{backgroundColor: 'green'}}>
        <Toolbar>
          // Your Nav Bar
        </Toolbar>
      </AppBar>
      <Box display="flex" p={2} style={{height: "100%"}}>
        <Box flexBasis="20%" borderRight={1} borderColor="grey.500">
          // Your Side Bar
        </Box>
        <Box flexBasis="60%" borderRight={1} borderColor="grey.500" ml={2}>
          <Box display="block" justifyContent="center" alignItems="top" style={{height: "100%"}}>
            <Box display="flex" flexDirection="column">
              <TextField
              style={{marginLeft: '100px', width:'70%'}}
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
              <Box alignSelf="flex-end" width="20%" mt={2}>
                <Select
                  value={selectedOption}
                  onChange={handleSelectChange}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                  sx={{ height: '30px', width: '100px', fontSize: '0.875rem' }}
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  <MenuItem value={10}>Option 1</MenuItem>
                  <MenuItem value={20}>Option 2</MenuItem>
                  <MenuItem value={30}>Option 3</MenuItem>
                </Select>
              </Box>
            </Box>
            {data && <div>{/* Display data here */}</div>}
          </Box>
          // Your filters and search results
        </Box>
        <Box flexBasis="20%" ml={2}>
          // Your text section
        </Box>
      </Box>
    </Box>
  );
};

export default App;
