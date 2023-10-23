import React, { useState } from "react";
import "../Home.css";
import { widgetTwoApi } from "../../api";
import { useNavigate } from "react-router-dom";

export default function Two() {
  const widgetTwoComponentName = sessionStorage.getItem("widgetTwoTrue");
  const userId = sessionStorage.getItem("user");
  const navigate = useNavigate();

  const widgetNameMap = {
    Classic_An: "협곡 분석",
    Classic_Ti: "협곡 티어",
    Aram_An: "칼바람 분석",
    Aram_Ti: "칼바람 티어",
  };

  const widgetTwoNameMap = {
    "협곡 분석": "Classic_An",
    "협곡 티어": "Classic_Ti",
    "칼바람 분석": "Aram_An",
    "칼바람 티어": "Aram_Ti",
  };

  const widgerTwoName = widgetNameMap[widgetTwoComponentName];
  const [activeButton2, setActiveButton2] = useState(`${widgerTwoName}`);

  const handleButtonClick2 = async (buttonText2) => {
    setActiveButton2(buttonText2);

    const columnName = widgetTwoNameMap[buttonText2];

    const data = {
      userId,
      columnName,
    };

    const widgetResponse = await widgetTwoApi(data);
    console.log(widgetResponse.data.columnName);
    sessionStorage.setItem(
      "widgetTwoTrue",
      `${widgetResponse.data.columnName}`
    );
    navigate(0);
  };

  return (
    <div className="widgetTwoButton">
      {["협곡 분석", "협곡 티어", "칼바람 분석", "칼바람 티어"].map(
        (buttonText2) => (
          <button
            key={buttonText2}
            type="button"
            class={`nav-button ${
              activeButton2 === buttonText2 ? "active" : ""
            }`}
            onClick={() => handleButtonClick2(buttonText2)}
          >
            {buttonText2}
          </button>
        )
      )}
    </div>
  );
}
