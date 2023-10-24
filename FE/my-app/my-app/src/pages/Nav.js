import React, { useState } from "react";
import "./Nav.css";
import { useNavigate } from "react-router-dom";

const Nav = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isChampionDropdownOpen, setIsChampionDropdownOpen] = useState(false);

  const navigate = useNavigate();
  const logOutHandler = () => {
    sessionStorage.clear();
    navigate(0);
    navigate(`/`);
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
    setIsChampionDropdownOpen(false); // 챔피언 티어 드롭다운을 닫습니다.
  };

  const toggleChampionDropdown = () => {
    setIsChampionDropdownOpen(!isChampionDropdownOpen);
    setIsDropdownOpen(false); // 다른 드롭다운을 닫습니다.
  };

  const closeDropdowns = () => {
    setIsDropdownOpen(false);
    setIsChampionDropdownOpen(false);
  };

  return (
    <div className="App">
      <nav className="nav nav-tabs">
        <li className="nav-item">
          <a className="nav-link" href="/">
            15GG
          </a>
        </li>
        <li
          className={`nav-item dropdown ${isDropdownOpen ? "show" : ""}`}
          onMouseEnter={toggleDropdown}
          onMouseLeave={closeDropdowns}
        >
          <a
            className="nav-link dropdown-toggle"
            href="/classicsearch"
            role="button"
          >
            챔피언 분석
          </a>
          <ul
            className={`dropdown-menu ${isDropdownOpen ? "show" : ""}`}
            aria-labelledby="navbarDropdown"
            style={{ backgroundColor: "#380101", color: "white" }}
          >
            <li>
              <a className="dropdown-item" href="/classicsearch">
                협곡 분석
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="/aramsearch">
                칼바람 분석
              </a>
            </li>
          </ul>
        </li>
        <li
          className={`nav-item dropdown ${
            isChampionDropdownOpen ? "show" : ""
          }`}
          onMouseEnter={toggleChampionDropdown}
          onMouseLeave={closeDropdowns}
        >
          <a
            className="nav-link dropdown-toggle"
            href="/tier/classic  "
            role="button"
          >
            챔피언 티어
          </a>
          <ul
            className={`dropdown-menu ${isChampionDropdownOpen ? "show" : ""}`}
            aria-labelledby="navbarDropdown"
            style={{ backgroundColor: "#380101", color: "white" }}
          >
            <li>
              <a className="dropdown-item" href="/tier/classic">
                협곡 티어
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="/tier/aram">
                칼바람 티어
              </a>
            </li>
          </ul>
        </li>
        {sessionStorage.getItem("token") ? (
          <li className="nav-item">
            <button className="nav-link" onClick={() => logOutHandler()}>
              로그아웃
            </button>
          </li>
        ) : (
          <li className="nav-item">
            <a className="nav-link" href="/login/Login">
              로그인 / 회원가입
            </a>
          </li>
        )}
      </nav>
    </div>
  );
};

export default Nav;
