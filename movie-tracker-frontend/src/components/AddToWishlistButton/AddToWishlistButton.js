import React from "react";
import { Button } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faStar } from "@fortawesome/free-solid-svg-icons";

function AddToWishlistButton({ movieId }) {
  return (
    <Button variant="contained" style={{ marginRight: "5px" }}>
      &nbsp;
      <FontAwesomeIcon icon={faStar} /> &nbsp;Wishlist&nbsp;
    </Button>
  );
}

export default AddToWishlistButton;
