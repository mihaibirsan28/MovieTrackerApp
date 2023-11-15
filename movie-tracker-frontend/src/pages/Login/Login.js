import React, { useState } from 'react';
import { TextField, Button, Container, Grid, Typography } from '@mui/material';
import './Login.css'

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
      });
    
      const handleChange = (e) => {
        setFormData({
          ...formData,
          [e.target.name]: e.target.value,
        });
      };
    
      const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
      };
    
      return (
        <Container id="grid" component="main" maxWidth="md">
          <div>
            <Typography id="title" align='center' variant='h3'>Login</Typography>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    label="Email Address"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    label="Password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                  />
                </Grid>
              </Grid>
              <Button id="button" type="submit" fullWidth variant="contained" color="warning">
                Login
              </Button>
            </form>
          </div>
        </Container>
      );
}

export default Login;