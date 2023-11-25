import React, { useContext, useState } from "react";
import { TextField, Button, Container, Grid, Typography } from "@mui/material";
import "./Login.css";
import axios from "axios";
import { properties } from "../../properties";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    grant_type: "password",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(properties.BACKEND_HOST + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });
      sessionStorage.setItem("accessToken", response.data.access_token);
      navigate("/movies");
      window.location.reload();
    } catch (error) {}
  };

  return (
    <Container id="grid" component="main" maxWidth="md">
      <div>
        <Typography id="title" align="center" variant="h3">
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                label="Username"
                name="username"
                value={formData.username}
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
          <Button
            id="button"
            type="submit"
            fullWidth
            variant="contained"
            color="warning"
          >
            Login
          </Button>
        </form>
      </div>
    </Container>
  );
}

export default Login;
