import React from "react";
import ClassicBuild from "./anal/ClassicBuild";
import Classic from "./tier/Classic";
import "./Home.css";
import AramBuild from "./anal/AramBuild";
import Aram from "./tier/Aram";
import WidgetOneButton from "./widget/One";
import WidgetTwoButton from "./widget/Two";

const Home = () => {
  const widgetOneComponentName = sessionStorage.getItem("widgetOneTrue");
  const widgetTwoComponentName = sessionStorage.getItem("widgetTwoTrue");
  const token = sessionStorage.getItem("token");

  const componentMap = {
    Classic_An: <ClassicBuild />,
    Classic_Ti: <Classic />,
    Aram_An: <AramBuild />,
    Aram_Ti: <Aram />,
  };

  const widgetOneComponent = componentMap[widgetOneComponentName];
  const widgetTwoComponent = componentMap[widgetTwoComponentName];

  return (
    <div className="container">
      <div className="image-container">
        <img
          src="https://cdn-store.leagueoflegends.co.kr/images/v2/champion-splashes/17018.jpg"
          alt=""
          style={{ width: "100%" }} // 원하는 너비로 설정하세요
        />

        <div className="widget-container">
          {widgetOneComponent ? (
            <div className="widgetOne">
              <WidgetOneButton />
              {widgetOneComponent}
            </div>
          ) : token ? (
            <div className="widgetNotLogin1">
              눌러주세요
              <WidgetOneButton />
            </div>
          ) : (
            <div className="widgetNotLogin1">
              <div className="widgetNotLogin3">로그인시 이용 가능한 페이지입니다.</div>
            </div>
          )}

          {widgetTwoComponent ? (
            <div className="widgetTwo">
              <WidgetTwoButton />
              {widgetTwoComponent}
            </div>
          ) : token ? (
            <div className="widgetNotLogin2">
              눌러주세요
              <WidgetTwoButton />
            </div>
          ) : (
            <div className="widgetNotLogin2">
              <div className="widgetNotLogin3">로그인시 이용 가능한 페이지입니다.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
