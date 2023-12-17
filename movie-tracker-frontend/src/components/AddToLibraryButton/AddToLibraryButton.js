import React from "react";
import { Button } from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBookmark } from "@fortawesome/free-solid-svg-icons";

function AddToLibraryButton({movieId}) {
    return (
        <Button variant="contained" style={{ marginRight: "5px" }}>
            <FontAwesomeIcon icon={faBookmark} /> Add to Library
        </Button>
    );
}

export default AddToLibraryButton;