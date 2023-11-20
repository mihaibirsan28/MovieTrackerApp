import { Container, Grid } from '@mui/material';
import MovieCard from '../../components/MovieCard/MovieCard';
import React, { useEffect, useState } from 'react';
import movieData from '../../response.json'
import './Movies.css'

function Movies() {
    const [movies, setMovies] = useState([]);
    const [page, setPage] = useState(1);

    const fetchMovies = async () => {
        // const response = await fetch();
        // const data = await response.json();
        console.log("Fetching... ")
        const data = movieData.results;
        setMovies((prevMovies) => [...prevMovies, ...data]);
      };

      useEffect(() => {
        console.log('Effect running...');
        fetchMovies();
      }, [page]);

      return (
        <Container class="grid" >
        <Grid container spacing={3}>
          {movies.map((movie) => (
            <Grid key={movie.id} item xs={12} sm={6} md={4} lg={3}>
              <MovieCard
                title={movie.titleText.text}
                imageUrl={movie.primaryImage?.url || 'defaultImageUrl'}
                releaseYear={movie.releaseYear.year}
              />
            </Grid>
          ))}
        </Grid>
      </Container>
      );
}

export default Movies;