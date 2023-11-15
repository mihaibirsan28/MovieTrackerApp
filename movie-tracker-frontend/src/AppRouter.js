// AppRouter.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import Register from './pages/Register/Register';
import Login from './pages/Login/Login';
import MyMovies from './pages/MyMovies/MyMovies';

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/home" element={<Home/>}/>
        <Route exact path="/myMovies" element={<MyMovies/>}/>
        {/* <Route path="/myMovies" component={MyMovies} />
        <Route path="/myWishlist" component={MyWishlist} /> */}
        <Route exact path="/register" element={<Register/>}/>
        <Route exact path="/login" element={<Login/>}/>
        {/* <Route path="/friends" component={Friends} /> */}
      </Routes>
    </Router>
  );
};

export default AppRouter;
