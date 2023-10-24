import React, { useState, useEffect } from "react";
import "./style/Classic.css";
import "./style/Classic2.css";
import { AramTier } from "../../api";

const Aram = () => {
  const [topPositionData, setTopPositionData] = useState([]);

  useEffect(() => {
    AramTier()
      .then((result) => {
        if (result) {
          console.log("받아온 Tier 데이터:", { result });
          const initialData = [...result.list].sort((a, b) => b.pick_cnt - a.pick_cnt);
          setTopPositionData(initialData);
        } else {
          console.log("Tier 데이터를 받아올 수 없음.");
        }
      })
      .catch((error) => {
        console.error("오류 발생:", error);
      });

    // 표본이 높은 순으로 정렬해서 초기 데이터 설정
    // const initialData = [...topPositionData].sort((a, b) => b.pick_cnt - a.pick_cnt);
    // setTopPositionData(initialData);
  }, []);

  const [sortBy, setSortBy] = useState("pick_cnt"); // 초기 정렬 기준
  const [sortDirection, setSortDirection] = useState("descending"); // 초기 정렬 방향

  // 데이터를 주어진 key로 정렬하는 함수
  const sortByKey = (key) => {
    const sortedData = [...topPositionData].sort((a, b) => {
      if (sortDirection === "ascending") {
        return a[key] - b[key];
      } else {
        return b[key] - a[key];
      }
    });
    setTopPositionData(sortedData);
    setSortBy(key);
    // 정렬 방향을 토글 (ascending <-> descending)
    setSortDirection(
      sortDirection === "ascending" ? "descending" : "ascending"
    );
  };

  return (
    <div>
      <div className="css-123">칼바람 티어 정보</div>
      <br></br>
      <br></br>
      <div className="css-gtm9xc">
        <div className="input-table"></div>
      </div>

      <div>
        <div className="table-container2">
          <div className="table-header">챔피언</div>
          <div className="table-header">
            K/D/A
            <button onClick={() => sortByKey("av_kda")}>
              {sortBy === "av_kda"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            승률
            <button onClick={() => sortByKey("win_rate")}>
              {sortBy === "win_rate"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            픽률
            <button onClick={() => sortByKey("pick_rate")}>
              {sortBy === "pick_rate"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            표본
            <button onClick={() => sortByKey("pick_cnt")}>
              {sortBy === "pick_cnt"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
        </div>
        {topPositionData.map((champion) => (
          <div key={champion.champion_name} className="table-row2">
            <div className="table-data">{champion.champion_name}</div>
            <div
              className="table-data"
              style={{
                color:
                  champion.av_kda >= 4
                    ? "#E84057"
                    : champion.av_kda >= 3
                    ? "#0093FF"
                    : champion.av_kda >= 2
                    ? "#00BBA3"
                    : champion.av_kda < 2
                    ? "#9AA4AF"
                    : "inherit",
              }}
            >
              {champion.av_kda}
            </div>
            <div
              className="table-data"
              style={{
                color: champion.win_rate >= 0.6 ? "#E84057" : "inherit",
              }}
            >
              {(champion.win_rate * 100).toFixed(2)}%
            </div>
            <div className="table-data">
              {(champion.pick_rate * 100).toFixed(2)}%
            </div>
            <div className="table-data">{champion.pick_cnt}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Aram;
