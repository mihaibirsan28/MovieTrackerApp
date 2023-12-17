import { Container, Grid } from '@mui/material';
import MovieCard from '../../components/MovieCard/MovieCard';
import React, { useEffect, useState } from 'react';
import movieData from '../../response.json'
import './MovieGrid.css'

function MovieGrid({movieList}) {
    return (
        <Container class="grid" >
        <Grid container spacing={3}>
          {movieList.map((movie) => (
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

export default MovieGrid;
