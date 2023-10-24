import "./style/ClassicTable.css";

const Aram_Search = ({ championData }) => {
  console.log("props:", championData);
  const cursor = "https://s-lol-web.op.gg/images/icon/icon-arrow-right.svg";
  if (championData === null) {
    return <div>Loading..</div>;
  }
  const bestChampionData = championData[0];
  
  if (!bestChampionData) {
    return <div className="noname">없는 챔피언 이름입니다. 다시 한 번 확인해주세요.  </div>;
  }

  console.log(bestChampionData);

  const championImageUrl = `https://ddragon.leagueoflegends.com/cdn/13.20.1/img/champion/${bestChampionData.champion_name}.png`;
  const itemStart = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/item/${bestChampionData.itemSet1_1}.png`;
  const itemStart2 = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/item/${bestChampionData.itemSet1_2}.png`;
  const itemShoes = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/item/${bestChampionData.shoes1}.png`;
  const mainItem = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/item/${bestChampionData.core1_1}.png`;
  const mainItem2 = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/item/${
    bestChampionData.core1_2
      ? bestChampionData.core1_2
      : bestChampionData.core2_2
  }.png`;
  const convertSkillBuild = (skillValue) => {
    switch (Number(skillValue)) {
      case 1:
        return "Q";
      case 2:
        return "W";
      case 3:
        return "E";
      default:
        return ""; // 다른 값이 들어올 경우 처리
    }
  };

  const convertSpellBuild = (spellValue) => {
    switch (Number(spellValue)) {
      case 1:
        return "SummonerBoost";
      case 3:
        return "SummonerExhaust";
      case 4:
        return "SummonerFlash";
      case 6:
        return "SummonerHaste";
      case 7:
        return "SummonerHeal";
      case 11:
        return "SummonerSmite";
      case 12:
        return "SummonerTeleport";
      case 13:
        return "SummonerMana";
      case 14:
        return "SummonerDot";
      case 21:
        return "SummonerBarrier";
      case 32:
        return "SummonerSnowball";
      default:
        return ""; // 다른 값이 들어올 경우 처리
    }
  };

  // filteredChampionData 내의 데이터를 변환

  // 스킬빌드 1,2,3형식으로 들어오는 것을 Q,W,E로 변환 확인
  console.log(convertSkillBuild(bestChampionData.skill_build1));

  // 스펠 변환 형식으로 들어오는 것 확인
  console.log(convertSpellBuild(bestChampionData.spell1_1));
  const summonerspell1 = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/spell/${convertSpellBuild(
    bestChampionData.spell1_1
  )}.png`;
  const summonerspell2 = `http://ddragon.leagueoflegends.com/cdn/13.19.1/img/spell/${convertSpellBuild(
    bestChampionData.spell1_2
  )}.png`;

  const skillImageUrl = `https://opgg-static.akamaized.net/meta/images/lol/spell/${
    bestChampionData.champion_name
  }${convertSkillBuild(
    bestChampionData.skill_build1
  )}.png?image=q_auto,f_webp,w_64&v=1696570752446`;
  const skillImageUrl2 = `https://opgg-static.akamaized.net/meta/images/lol/spell/${
    bestChampionData.champion_name
  }${convertSkillBuild(
    bestChampionData.skill_build2
  )}.png?image=q_auto,f_webp,w_64&v=1696570752446`;
  const skillImageUrl3 = `https://opgg-static.akamaized.net/meta/images/lol/spell/${
    bestChampionData.champion_name
  }${convertSkillBuild(
    bestChampionData.skill_build3
  )}.png?image=q_auto,f_webp,w_64&v=1696570752446`;

  const runecode1 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_pristyle}_60.webp`;
  const runecode2 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_priperk1}_60.webp`;
  const runecode3 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_priperk2}_60.webp`;
  const runecode4 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_priperk3}_60.webp`;
  const runecode5 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_priperk4}_60.webp`;
  const runecode6 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_substyle}_60.webp`;
  const runecode7 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_subperk1}_60.webp`;
  const runecode8 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.most_subperk2}_60.webp`;
  const runecode9 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.abil_off}_60.webp`;
  const runecode10 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.abil_fle}_60.webp`;
  const runecode11 = `https://cdn.lol.ps/assets/img/runes/${bestChampionData.abil_def}_60.webp`;

  return (
    <div>
      <main className="main-123">
        <div className="classic-table">
          <img src={championImageUrl} alt="champimg" className="champ-image" />

          <div className="champ-name">{bestChampionData.champion_name}</div>
        </div>

        <div className="rate-table">
          <div className="rate">승률</div>

          <div className="rate">픽률</div>
        </div>

        <div className="rate-table">
          <div className="percent-table">
            {(bestChampionData.win_rate * 100).toFixed(1)}%
          </div>

          <div className="percent-table">
            {(bestChampionData.pick_rate * 100).toFixed(1)}%
          </div>
        </div>

        <div className="rate-table">
          <div className="skilltreename">스킬트리</div>
        </div>
        {/* 스킬 빌드에 들어오는 순서대로 리턴 */}
        <div className="rate-table">
          <img src={skillImageUrl} alt="champimg" className="image-all" />
          <img src={cursor} alt="champimg" className="image-all" />
          <img src={skillImageUrl2} alt="champimg" className="image-all" />
          <img src={cursor} alt="champimg" className="image-all" />
          <img src={skillImageUrl3} alt="champimg" className="image-all" />
        </div>

        <div className="rate-table">
          <div className="skill-tree123">
            {convertSkillBuild(bestChampionData.skill_build1)}
          </div>
          <img src={cursor} alt="champimg" className="image-all" />
          <div className="skill-tree123">
            {convertSkillBuild(bestChampionData.skill_build2)}
          </div>
          <img src={cursor} alt="champimg" className="image-all" />
          <div className="skill-tree123">
            {convertSkillBuild(bestChampionData.skill_build3)}
          </div>
        </div>

        <div className="rune-table">
          <div className="runetable-left">
            <div className="rune-name">룬페이지</div>
            <div className="rune-page">
              <div className="rune-page-perk1">
                <div className="rune-row-top">
                  <img src={runecode1} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode2} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode3} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode4} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode5} alt="rune" className="rune-image" />
                </div>
              </div>
              <div className="rune-page-perk1">
                <div className="rune-row-top2">
                  <img src={runecode6} alt="rune" className="rune-image" />
                </div>

                <div className="rune-row">
                  <img src={runecode7} alt="rune" className="rune-image" />
                </div>

                <div className="rune-row">
                  <img src={runecode8} alt="rune" className="rune-image" />
                </div>
              </div>

              <div className="rune-page-perk1-end">
                <div className="rune-row-top3">
                  <img src={runecode9} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode10} alt="rune" className="rune-image" />
                </div>
                <div className="rune-row">
                  <img src={runecode11} alt="rune" className="rune-image" />
                </div>
              </div>
            </div>
          </div>

          <div className="runetable-right">
            <div className="runetable-1">
              소환사 주문
              <div>
                <img
                  src={summonerspell1}
                  alt="spell"
                  className="image-all123"
                />
                <img
                  src={summonerspell2}
                  alt="spell"
                  className="image-all123"
                />

                <div className="win-rate">
                  승률:{(bestChampionData.spell1_win * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            <div className="runetable-1">
              시작 아이템
              <div>
                <img
                  src={itemStart}
                  alt="시작아이템"
                  className="image-all123"
                />
                {bestChampionData.itemSet1_2 && (
                  <img
                    src={itemStart2}
                    alt="시작아이템"
                    className="image-all123"
                  />
                )}

                <div className="win-rate">
                  승률:
                  {(bestChampionData.itemSet1_win * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            <div className="runetable-1">
              신발
              <div>
                <img src={itemShoes} alt="shoes" className="image-all123" />

                <div className="win-rate">
                  승률:{(bestChampionData.shoes1_win * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            <div className="runetable-end">
              메인 아이템 빌드
              <div>
                <img src={mainItem} alt="shoes" className="image-all123" />
                <img src={cursor} alt="cursor" className="image-all123" />
                <img src={mainItem2} alt="shoes" className="image-all123" />
                <div className="win-rate">
                  승률:{(bestChampionData.core1_win * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
export default Aram_Search;
