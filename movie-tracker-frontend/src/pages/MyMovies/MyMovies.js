import React, { useEffect, useState } from 'react';
import movieData from '../../response.json'
import MovieGrid from '../../components/MovieGrid/MovieGrid';

function MyMovies() {
    const [movies, setMovies] = useState([]);
    const [page, setPage] = useState(1);

    const fetchMovies = async () => {
        // const response = await fetch();
        // const data = await response.json();
        const data = movieData.results;
        setMovies((prevMovies) => [...prevMovies, ...data]);
      };

      useEffect(() => {
        fetchMovies();
      }, [page]);

    return (
        <>
          <MovieGrid movieList={movies} />
        </>
    )
}

export default MyMovies;