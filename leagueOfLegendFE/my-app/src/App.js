import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Searchbar from "./pages/search/Searchbar";
import Aram from "./pages/tier/Aram";
import Classic from "./pages/tier/Classic";
import Login from "./pages/login/Login";
import SignUp from "./pages/login/SignUp";
import Nav from "./pages/Nav";
import Search from "./pages/search/Search";
import AramBuild from "./pages/anal/AramBuild";
import ClassicBuild from "./pages/anal/ClassicBuild";
import AramSearch from "./pages/anal/AramSearch";
import ClassicSearch from "./pages/anal/ClassicSearch";
import Noname from "./pages/Noname";
import ErrorPage from "./pages/ErrorPage";

const App = () => {
  return (
    <div>
      {/* 상단 네비게이션바 불러오기 */}
      <Nav />
      {/* 검색기 불러오기 */}
      <Searchbar />
      {/* 경로 설정 */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tier/classic" element={<Classic />} />
        <Route path="/tier/aram" element={<Aram />} />
        <Route path="/arambuild" element={<AramBuild />} />
        <Route path="/aramsearch" element={<AramSearch />} />
        <Route path="/classicsearch" element={<ClassicSearch />} />
        <Route path="/classicbuild" element={<ClassicBuild />} />
        <Route path="/login/login" element={<Login />} />
        <Route path="/login/signup" element={<SignUp />} />
        <Route path="/search/search" element={<Search />} />
        <Route path="/noname" element={<Noname />} />
        <Route path="/errorpage" element={<ErrorPage />} />
      </Routes>
    </div>
  );
};

export default App;
