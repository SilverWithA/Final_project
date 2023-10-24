import React, { useEffect, useState } from "react";
import "../search/style/Search.css";
import "../tier/style/Classic.css";
import "../tier/style/Classic2.css";
import Classic_Search from "./Classic_Search";
import { ClassicAnalysis } from "../../api";

const ClassicBuild = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedTier, setSelectedTier] = useState("등급설정  ");
  const [searchText1, setSearchText1] = useState("");
  const [buildData, setBuildData] = useState([]); // 상태 변수로 buildData를 저장
  const imageUrl =
    "https://i.namu.wiki/i/d87ruSFsV6wCgnE1MW03j4UVoP1GY5UOUWi4u_KDb35MyZMkXetzYT0t-X52WTKK3jrddfw-3VRUImhdA9W4EpYcM7YBaUpih7N59zxAJgYAiwHNFZEgRM1gQ_HHgBmaiUOa8HPPvweNvkmxzv85Ag.webp";

  const tierList = [
    "챌린저",
    "그랜드마스터",
    "마스터",
    "다이아",
    "에메랄드",
    "플레티넘",
    "골드",
    "실버",
    "브론즈",
    "아이언",
  ];

  const buttonStyle = {
    backgroundImage: `url(${imageUrl})`,
    backgroundSize: "cover",
    width: "50px", // 원하는 너비 설정
    height: "50px", // 원하는 높이 설정
    border: "none",
    borderRadius: "50%",
  };

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const changeButtonText = (newText) => {
    setSelectedTier(newText);
    setIsDropdownOpen(false);
  };
  const [effectData, setEffectData] = useState(null);
  useEffect(() => {
    console.log("effectData:", effectData);
    // return ()=>{
    //   console.log('useEffect End');
    // }
  }, [effectData]);

  const handleRoleClick = async (searchText1) => {
    setSearchText1(searchText1);

    const tier = selectedTier;
    const champion_name = searchText1;

    const data = {
      tier,
      champion_name,
    };

    try {
      const buildData = await ClassicAnalysis(data);
      setEffectData(buildData.list);
      setBuildData(buildData);
      console.log("buildData:", buildData.list[0]);
    } catch (error) {
      // 오류 처리
      console.error("Error fetching Classic Build:", error);
    }
  };
  console.log(buildData);
  const getData = () => {
    console.log("getData:", searchText1);
    handleRoleClick(searchText1).then((r) => console.log(r));
  };
  return (
    <div>
      <div className="anal-title">
        <div className="css-123">협곡 챔피언 분석</div>
        <div className="input-table">
          <div>
            <div className="dropdown123">
              <button
                className="btn custom-button dropdown-toggle"
                type="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
                onClick={toggleDropdown}
              >
                {selectedTier}
              </button>
              <ul
                className={`dropdown-menu text-center ${
                  isDropdownOpen ? "show dropdown-menu-up" : ""
                }`}
              >
                {tierList.map((tier) => (
                  <li key={tier}>
                    <a
                      className="dropdown-item"
                      href="##"
                      onClick={() => changeButtonText(tier)}
                    >
                      {tier}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="grade-table">
            <input
            style={{fontFamily: "omyu_pretty, sans-serif",
            fontSize: "18px",}}
              className="form-control"
              type="search"
              value={searchText1}
              onChange={(e) => setSearchText1(e.target.value)}
              placeholder="챔피언명 검색"
              aria-label="Search"
            />
            <button
              className="search1234"
              type="button"
              onClick={getData}
              style={buttonStyle}
            ></button>
          </div>
        </div>
      </div>

      {effectData && <Classic_Search championData={effectData} />}
    </div>
  );
};

export default ClassicBuild;
