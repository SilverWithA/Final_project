import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./style/Searchbar.css";

const Searchbar = () => {
  const [searchText, setSearchText] = useState("");
  const navigate = useNavigate();
  const imageUrl =
    "https://i.namu.wiki/i/d87ruSFsV6wCgnE1MW03j4UVoP1GY5UOUWi4u_KDb35MyZMkXetzYT0t-X52WTKK3jrddfw-3VRUImhdA9W4EpYcM7YBaUpih7N59zxAJgYAiwHNFZEgRM1gQ_HHgBmaiUOa8HPPvweNvkmxzv85Ag.webp";

  const submitFunc = (event) => {
    event.preventDefault();
    navigate("/search/search", {
      state: { searchText },
    });
  };

  const buttonStyle = {
    backgroundImage: `url(${imageUrl})`,
    backgroundSize: "cover",
    width: "50px", // 원하는 너비 설정
    height: "50px", // 원하는 높이 설정
    border: "none",
    borderRadius: "50%",
  };

  return (
    <>
      <div className="input-container">
        <form
          onSubmit={submitFunc}
          class="form-control me-2 d-flex search-form"
          role="search"
        >
          <input
            className="custom-input"
            type="search"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="소환사명 검색"
            aria-label="Search"
          />
          <Link
            to={{
              pathname: "/search/search",
              state: { searchText: searchText },
            }}
            class="btn btn-outline-success me-2"
            type="text"
            state={{ searchText: searchText }}
            style={buttonStyle}
          >
            {" "}
          </Link>
        </form>
      </div>
    </>
  );
};
export default Searchbar;
