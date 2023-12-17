import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button, TextField } from "@mui/material";

function NavbarComponent() {
  const [isLogged, setIsLogged] = useState(false);

  const checkIfLogged = () => {
    const accessToken = sessionStorage.getItem("accessToken");
    if (accessToken) {
      setIsLogged(true);
    } else {
      setIsLogged(false);
    }
  };

  const logout = () => {
    sessionStorage.removeItem("accessToken");
    window.location.reload();
  };

  useEffect(() => {
    checkIfLogged();
  }, []);

  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="#home">Movie Tracker</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/home">Home</Nav.Link>
            <Nav.Link href="/movies">Movies</Nav.Link>
            <Nav.Link href="/myMovies">My Movies</Nav.Link>
            <Nav.Link href="/myWishlist">My Wishlist</Nav.Link>
            <Nav.Link href="#link">Friends</Nav.Link>
            <TextField
              id="outlined-search"
              label="Search..."
              type="search"
              size="small"
            />
          </Nav>
          <Nav className="ml-auto">
            {" "}
            {!isLogged && (
              <>
                <Nav.Link href="/register">Register</Nav.Link>
                <Nav.Link href="/login">Log In</Nav.Link>
              </>
            )}
            {isLogged && (
              <Button variant="contained" color="warning" onClick={logout}>
                Logout
              </Button>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavbarComponent;
