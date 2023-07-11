import React, { useState, useEffect } from "react";
import MyAppBar from "./components/AppBar";
import CardBar from "./components/CardBar";
import ArticleView from "./components/ArticleView";
import SortControl from "./components/SortControl";
import { Paper } from "@mui/material";

const App = () => {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [sortType, setSortType] = useState("date");

  const fetchArticles = async () => {
    try {
      const response = await fetch("http://localhost:8000/");
      let data = await response.json();

      // Sort articles based on sortType state
      if (sortType === "date") {
        data.sort(
          (a, b) => new Date(b.published_date) - new Date(a.published_date)
        );
      } else if (sortType === "duration") {
        data.sort((a, b) => a.duration.localeCompare(b.duration));
      }

      setArticles(data);
      setSelectedArticle(data[0]);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, [sortType]);

  const handleSortChange = (event) => {
    setSortType(event.target.value);
  };

  return (
    <Paper elevation={3} style={{ maxWidth: "80%", margin: "auto" }}>
      <MyAppBar />
      <SortControl value={sortType} onChange={handleSortChange} />
      {articles.length > 0 && (
        <CardBar articles={articles} onCardClick={setSelectedArticle} />
      )}
      {selectedArticle && <ArticleView article={selectedArticle} />}
    </Paper>
  );
};

export default App;




// CardBar.js

import React from "react";
import { Card, CardContent, Typography } from "@mui/material";

const CardBar = ({ articles, onCardClick }) => {
  return (
    <div style={{ display: "flex", overflowX: "scroll" }}>
      {articles.map((article, index) => (
        <Card key={index} onClick={() => onCardClick(article)}>
          <CardContent>
            <Typography variant="h5">{article.headline}</Typography>
            <Typography variant="body2">{article.teaser}</Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default CardBar;



import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

const MyCard = ({ article }) => (
  <Card>
    <CardContent>
      <Typography variant="h5">{article.headline}</Typography>
      <Typography variant="body2">{article.teaser}</Typography>
    </CardContent>
  </Card>
);

export default MyCard;


// SortControl.js

import React from "react";
import { FormControlLabel, Radio, RadioGroup } from "@mui/material";

const SortControl = ({ value, onChange }) => {
  return (
    <RadioGroup row value={value} onChange={onChange}>
      <FormControlLabel value="date" control={<Radio />} label="Recency Date" />
      <FormControlLabel value="duration" control={<Radio />} label="Duration" />
    </RadioGroup>
  );
};

export default SortControl;



// ArticleView.js

import React from "react";
import { Paper, Tab, Tabs, Typography, Box } from "@mui/material";

const ArticleView = ({ article }) => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Paper sx={{ flexGrow: 1, backgroundColor: "grey" }}>
      <Tabs value={value} onChange={handleChange} centered>
        <Tab label="Article" />
        <Tab label="Key Takeaways" />
        <Tab label="AI Summary" />
      </Tabs>
      {value === 0 && (
        <Box p={3}>
          <Typography>{article.article}</Typography>
        </Box>
      )}
      {value === 1 && (
        <Box p={3}>
          <Typography>{article.summary}</Typography>
        </Box>
      )}
      {value === 2 && (
        <Box p={3}>
          <Typography>{article.ai_summary}</Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ArticleView;

