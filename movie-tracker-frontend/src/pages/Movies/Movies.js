import React, { useEffect, useState } from "react";
import movieData from "../../response.json";
import "./Movies.css";
import MovieGrid from "../../components/MovieGrid/MovieGrid";
import axios from "axios";
import { properties } from "../../properties";

function Movies() {
  const moviesLimit = 20;
  const [movies, setMovies] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get(
          `${properties.BACKEND_HOST}/random-movies?limit=${moviesLimit}`
        );
        console.log(response.data);
        setMovies(response.data.results);
      } catch (error) {
        console.log(error);
      }
    }
    fetchData();
  }, []);

  return (
    <>
      <MovieGrid movieList={movies} />
    </>
  );
}

export default Movies;
