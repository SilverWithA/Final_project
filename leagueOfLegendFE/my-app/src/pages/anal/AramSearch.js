import React, { useState, useEffect } from "react";

import "../search/style/Search.css";
import "../tier/style/Classic.css";
import "../tier/style/Classic2.css";
import Aram_Search from "./Aram_Search";
import { AramAnalysis } from "../../api";

const AramSearch = () => {
  const [searchText1, setSearchText1] = useState("");
  const [buildData, setBuildData] = useState([]); // 상태 변수로 buildData를 저장
  const imageUrl =
    "https://i.namu.wiki/i/d87ruSFsV6wCgnE1MW03j4UVoP1GY5UOUWi4u_KDb35MyZMkXetzYT0t-X52WTKK3jrddfw-3VRUImhdA9W4EpYcM7YBaUpih7N59zxAJgYAiwHNFZEgRM1gQ_HHgBmaiUOa8HPPvweNvkmxzv85Ag.webp";

  const buttonStyle = {
    backgroundImage: `url(${imageUrl})`,
    backgroundSize: "cover",
    width: "50px", // 원하는 너비 설정
    height: "50px", // 원하는 높이 설정
    border: "none",
    borderRadius: "50%",
  };

  const [effectData, setEffectData] = useState(null);
  useEffect(() => {
    console.log("effectData:", effectData);
  }, [effectData]);

  const handleRoleClick = async (searchText1) => {
    setSearchText1(searchText1);

    const champion_name = searchText1;

    const data = {
      champion_name,
    };

    try {
      const buildData = await AramAnalysis(data);
      console.log(1);
      setEffectData(buildData.list);
      console.log(2);
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
        <div className="css-123">칼바람 챔피언 분석</div>
        <div className="input-table">
          <div className="grade-table">
            <input
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

      {effectData && <Aram_Search championData={effectData} />}
    </div>
  );
};

export default AramSearch;
