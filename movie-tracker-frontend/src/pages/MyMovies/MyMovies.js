import React, { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import axios from "axios";
import { properties } from "../../properties";
import MovieGrid from "../../components/MovieGrid/MovieGrid";

function MyMovies() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchData() {
      if (sessionStorage.accessToken)
        try {
          const response = await axios.get(
            `${properties.BACKEND_HOST}/my-library`,
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
        <MovieGrid movieList={movies} />
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
            Please log in/register to be able to see your library.
          </Typography>
        </Box>
      )}
    </>
  );
}

export default MyMovies;
