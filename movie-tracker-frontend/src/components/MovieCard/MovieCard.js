import React from "react";
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  Modal,
  Box,
} from "@mui/material";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import AddToLibraryButton from "../AddToLibraryButton/AddToLibraryButton";
import AddToWishlistButton from "../AddToWishlistButton/AddToWishlistButton";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "50%",
  height: "50%",
  bgcolor: "background.paper",
  boxShadow: "1px 1px 18px #888888",
  display: "flex",
  pt: 2,
  px: 4,
  pb: 3,
};

const MovieCard = ({ id, title, imageUrl, releaseYear, pageType }) => {
  const [openInfos, setOpenInfos] = React.useState(false);
  const handleOpenInfos = () => {
    setOpenInfos(true);
  };
  const handleCloseInfos = () => {
    setOpenInfos(false);
  };
  console.log(id);
  return (
    <Card>
      <CardMedia component="img" alt={title} height="300" image={imageUrl} />

      <CardContent>
        <Typography variant="subtitle1" component="div">
          <strong>{title}</strong>&nbsp;•&nbsp;{releaseYear}
        </Typography>
        <div style={{ display: "flex" }}>
          {pageType !== "wishlist" && <AddToWishlistButton movieId={id} />}
          <AddToLibraryButton movieId={id} />
          <Button variant="contained" onClick={handleOpenInfos}>
            <FontAwesomeIcon icon={faCircleInfo} />
          </Button>
          <Modal
            open={openInfos}
            onClose={handleCloseInfos}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box sx={style}>
              <CardMedia
                component="img"
                alt={title}
                height="100%"
                style={{
                  objectFit: "contain",
                  margin: 0,
                  position: "absolute",
                  top: 0,
                  right: "-230px",
                }}
                image={imageUrl}
              />
              <div style={{ flex: 1 }}>
                <Typography variant="h5" component="div">
                  <strong>{title}</strong>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {releaseYear}
                </Typography>
                <div
                  style={{ position: "absolute", bottom: "20px", left: "20px" }}
                >
                  <div style={{ flex: 1, marginBottom: "10px" }}>
                    <AddToLibraryButton
                      movieId={id}
                      style={{ width: "100%" }}
                    />
                  </div>
                  {pageType !== "wishlist" && (
                    <div style={{ flex: 1 }}>
                      <AddToWishlistButton
                        movieId={id}
                        style={{ width: "100%" }}
                      />
                    </div>
                  )}
                </div>
              </div>
            </Box>
          </Modal>
        </div>
      </CardContent>
    </Card>
  );
};

export default MovieCard;
