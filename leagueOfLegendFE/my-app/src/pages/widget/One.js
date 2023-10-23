import React, { useState } from "react";
import "../Home.css";
import { widgetOneApi } from "../../api";
import { useNavigate } from "react-router-dom";

export default function One() {
  const widgetOneComponentName = sessionStorage.getItem("widgetOneTrue");
  const userId = sessionStorage.getItem("user");
  const navigate = useNavigate();

  const widgetNameMap = {
    Classic_An: "협곡 분석",
    Classic_Ti: "협곡 티어",
    Aram_An: "칼바람 분석",
    Aram_Ti: "칼바람 티어",
  };

  const widgetOneNameMap = {
    "협곡 분석": "Classic_An",
    "협곡 티어": "Classic_Ti",
    "칼바람 분석": "Aram_An",
    "칼바람 티어": "Aram_Ti",
  };

  const widgetOneName = widgetNameMap[widgetOneComponentName];
  const [activeButton1, setActiveButton1] = useState(`${widgetOneName}`);
  const handleButtonClick1 = async (buttonText1) => {
    setActiveButton1(buttonText1);

    const columnName = widgetOneNameMap[buttonText1];

    const data = {
      userId,
      columnName,
    };

    const widgetResponse = await widgetOneApi(data);
    console.log(widgetResponse.data.columnName);
    sessionStorage.setItem(
      "widgetOneTrue",
      `${widgetResponse.data.columnName}`
    );
    navigate(0);
  };

  return (
    <div className="widgetOneButton">
      {["협곡 분석", "협곡 티어", "칼바람 분석", "칼바람 티어"].map(
        (buttonText1) => (
          <button
            key={buttonText1}
            type="button"
            class={`nav-button ${
              activeButton1 === buttonText1 ? "active" : ""
            }`}
            onClick={() => handleButtonClick1(buttonText1)}
          >
            {buttonText1}
          </button>
        )
      )}
    </div>
  );
}
