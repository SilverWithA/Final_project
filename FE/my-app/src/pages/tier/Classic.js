import React, { useState } from "react";
import "./style/Classic.css";
import "./style/Classic2.css";
import { ClassicTier } from "../../api";

const Classic = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedTier, setSelectedTier] = useState("등급설정");
  const [selectedRole, setSelectedRole] = useState("");
  const [sortBy, setSortBy] = useState("pick_rate"); // 초기 정렬 승률 높은순
  const [sortDirection, setSortDirection] = useState("descending");
  const [tierData, setTierData] = useState([]); // 상태 변수로 tierData를 저장
  const [buttonState, setButtonState] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
    setButtonState(true);
  };

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

  const changeButtonText = (newText) => {
    setSelectedTier(newText);
    setIsDropdownOpen(false);
  };

  const handleRoleClick = async (role) => {
    setButtonState(false);
    setSelectedRole(role);

    const tier = selectedTier;
    const team_position = role;

    const data = {
      tier,
      team_position,
    };

    try {
      const tierData = await ClassicTier(data);
      setTierData(tierData.list);
      // console.log("tierData:", tierData.list);
      
    } catch (error) {
      // 오류 처리
      console.error("Error fetching Classic Tier:", error);
    }
  };

  // console.log(tierData);
  const championData = tierData;
  // console.log(championData);

  const toggleSortDirection = () => {
    setSortDirection(
      sortDirection === "ascending" ? "descending" : "ascending"
    );
  };

  const sortedData = championData.slice().sort((a, b) => {
    if (sortDirection === "ascending") {
      return a[sortBy] - b[sortBy];
    } else {
      return b[sortBy] - a[sortBy];
    }
  });

  return (
    <div>
      <div className="css-123">협곡 티어 정보</div>
      <div className="css-gtm9xc">
        <nav>
          <div className="css-g46fbk">
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
          </div>
        </nav>
        <div className="input-table">
          <nav className="nav-container">
            {["탑", "정글", "미드", "바텀", "서폿"].map((role) => (
              <button
                
                key={role}
                type="button"
                className={`nav-button ${
                  selectedRole === role ? "active" : ""
                }`}
                disabled={!buttonState}
                onClick={() => handleRoleClick(role)}
              >
                {role}
              </button>
            ))}
          </nav>
        </div>
      </div>

      <div>
        <div className="table-container1">
          <div className="table-header">챔피언</div>
          <div className="table-header">
            K/D/A
            <button
              onClick={() => {
                setSortBy("av_kda");
                toggleSortDirection();
              }}
            >
              {sortBy === "av_kda"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            승률
            <button
              onClick={() => {
                setSortBy("win_rate");
                toggleSortDirection();
              }}
            >
              {sortBy === "win_rate"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            픽률
            <button
              onClick={() => {
                setSortBy("pick_rate");
                toggleSortDirection();
              }}
            >
              {sortBy === "pick_rate"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            밴율
            <button
              onClick={() => {
                setSortBy("ban_rate");
                toggleSortDirection();
              }}
            >
              {sortBy === "ban_rate"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
          <div className="table-header">
            표본
            <button
              onClick={() => {
                setSortBy("pick_cnt");
                toggleSortDirection();
              }}
            >
              {sortBy === "pick_cnt"
                ? sortDirection === "ascending"
                  ? "▲"
                  : "▼"
                : "▲"}
            </button>
          </div>
        </div>

        {sortedData.map((champion) => (
          <div key={champion.champion_name} className="table-row">
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
            <div className="table-data">
              {(champion.ban_rate * 100).toFixed(2)}%
            </div>
            <div className="table-data">{champion.pick_cnt}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Classic;
