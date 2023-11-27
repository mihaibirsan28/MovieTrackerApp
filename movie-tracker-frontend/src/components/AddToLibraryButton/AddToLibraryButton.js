import React, { useState } from "react";
import { Button, Typography } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookmark } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { properties } from "../../properties";

const handleAddMovieLibrary = async (movieId, SetAdded) => {
  try {
    console.log(movieId);
    const response = await axios.post(
      `${properties.BACKEND_HOST}/library/${movieId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${sessionStorage.accessToken}`,
          "Content-type": "application/json",
        },
      }
    );
    if (response.status == 200) {
      SetAdded(true);
    }
  } catch (error) {
    console.log(error);
  }
};

function AddToLibraryButton({ movieId }) {
  const [added, SetAdded] = useState(false);
  return (
    <Button
      variant="contained"
      style={{ marginRight: "5px" }}
      onClick={() => handleAddMovieLibrary(movieId, SetAdded)}
    >
      <FontAwesomeIcon icon={faBookmark} />
      {!added ? (
        <Typography variant="subtitle2" component="div">
          Add to Library
        </Typography>
      ) : (
        <Typography variant="subtitle2" component="div">
          Added
        </Typography>
      )}
    </Button>
  );
}

export default AddToLibraryButton;
