import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Box from "@mui/material/Box";
import { Button, TextField, Typography } from "@mui/material";
import axios from "axios";
import { properties } from "../../properties";
import MovieGrid from "../../components/MovieGrid/MovieGrid";

function Home() {
  const [movies, setMovies] = useState([]);
  const [movieTitle, setMovieTitle] = useState("");
  const [page, setPage] = useState(1);

  const searchMovie = async () => {
    if (movieTitle !== "")
      try {
        const response = await axios.get(
          `${properties.BACKEND_HOST}/search/${movieTitle}?page=${page}`,
          {
            headers: {
              Authorization: `Bearer ${sessionStorage.accessToken}`,
            },
          }
        );
        console.log(response);
        setMovies(response.data.results);
      } catch (error) {
        console.log(error);
      }
  };

  useEffect(() => {
    searchMovie();
  }, [page]);
  return (
    <>
      {sessionStorage.accessToken ? (
        <>
          <Box
            sx={{
              width: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <TextField
              value={movieTitle}
              size="small"
              sx={{ width: "40%", marginTop: "50px" }}
              onChange={(e) => {
                setMovieTitle(e.target.value);
              }}
              placeholder="Movie Title"
            />
            <Button
              variant="contained"
              color="warning"
              onClick={() => {
                searchMovie();
                setPage(1);
              }}
              sx={{ marginTop: "20px" }}
            >
              Search
            </Button>
          </Box>
          <MovieGrid movieList={movies} />

          {movies.length !== 0 && (
            <Box
              sx={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
                marginBottom: "30px",
              }}
            >
              <Button
                variant="contained"
                color="warning"
                onClick={() => setPage((page) => page + 1)}
                sx={{ cursor: "pointer" }}
              >
                Next Page
              </Button>
            </Box>
          )}
        </>
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

export default Home;
