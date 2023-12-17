import React, { useState } from "react";
import { Button, Typography } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { properties } from "../../properties";

const handleAddMovieWishlist = async (movieId, SetAdded) => {
  try {
    const response = await axios.post(
      `${properties.BACKEND_HOST}/wishlist/${movieId}`,
      {},
      { headers: { Authorization: `Bearer ${sessionStorage.accessToken}` } }
    );
    if (response.status == 200) {
      SetAdded(true);
    }
  } catch (error) {
    console.log(error);
  }
};

function AddToWishlistButton({ movieId }) {
  const [added, SetAdded] = useState(false);
  return (
    <Button
      variant="contained"
      style={{ marginRight: "5px" }}
      onClick={() => handleAddMovieWishlist(movieId, SetAdded)}
    >
      <FontAwesomeIcon icon={faStar} />
      {!added ? (
        <Typography variant="subtitle2" component="div">
          Add to Wishlist
        </Typography>
      ) : (
        <Typography variant="subtitle2" component="div">
          Added
        </Typography>
      )}
    </Button>
  );
}

export default AddToWishlistButton;
