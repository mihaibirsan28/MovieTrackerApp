import React, { useEffect, useState } from "react";
import movieData from "../../response.json";
import MovieGrid from "../../components/MovieGrid/MovieGrid";
import axios from "axios";
import { properties } from "../../properties";

function MyWishlist() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get(
          `${properties.BACKEND_HOST}/my-wishlist`,
          { headers: { Authorization: `Bearer ${sessionStorage.accessToken}` } }
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
      <MovieGrid movieList={movies} pageType="wishlist" />
    </>
  );
}

export default MyWishlist;
