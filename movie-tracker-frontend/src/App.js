import React from 'react';
import './App.css';
import NavbarComponent from './components/Navbar/NavbarComponent';
import AppRouter from './AppRouter';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <>
      <NavbarComponent />
      <AppRouter />
    </>
  );
}


export default App;