import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import MovieGrid from "../../components/MovieGrid/MovieGrid";
import axios from "axios";
import { properties } from "../../properties";

function MyWishlist() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchData() {
      if (sessionStorage.accessToken)
        try {
          const response = await axios.get(
            `${properties.BACKEND_HOST}/my-wishlist`,
            {
              headers: {
                Authorization: `Bearer ${sessionStorage.accessToken}`,
              },
            }
          );

          setMovies(response.data);
        } catch (error) {
          console.log(error);
        }
    }
    fetchData();
  }, []);

  return (
    <>
      {sessionStorage.accessToken ? (
        <MovieGrid movieList={movies} pageType="wishlist" />
      ) : (
        <Box
          sx={{
            width: "100%",
            height: "600px",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Typography variant="subtitle1" component="div">
            Please log in/register to be able to see your watchlist.
          </Typography>
        </Box>
      )}
    </>
  );
}

export default MyWishlist;
