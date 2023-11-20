import React from "react";
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
} from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBookmark,
  faStar,
  faCircleInfo,
} from "@fortawesome/free-solid-svg-icons";

const MovieCard = ({ id, title, imageUrl, releaseYear }) => {
  return (
    <Card>
      <CardMedia component="img" alt={title} height="300" image={imageUrl} />
      <CardContent>
        <Typography variant="subtitle1" component="div">
          <strong>{title}</strong>&nbsp;•&nbsp;{releaseYear}
        </Typography>
        <div style={{ display: "flex"}}>
          <Button variant="contained" style={{ marginRight: '5px' }}>
            <FontAwesomeIcon icon={faBookmark} /> Add to Library
          </Button>
          <Button variant="contained" style={{ marginRight: '5px' }}>&nbsp;
            <FontAwesomeIcon icon={faStar} /> &nbsp;Wishlist&nbsp;
          </Button>
          <Button variant="contained">
            <FontAwesomeIcon icon={faCircleInfo} />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default MovieCard;
