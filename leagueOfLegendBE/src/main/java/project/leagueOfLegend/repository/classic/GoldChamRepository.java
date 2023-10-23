package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.GoldCham;

import java.util.List;

public interface GoldChamRepository extends JpaRepository<GoldCham, Integer> {
    @Query("select g from GoldCham g where g.team_position = :team_position")
    List<GoldCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT g FROM GoldCham g WHERE g.champion_name = :champion_name AND g.win_cnt = (SELECT MAX(g2.win_cnt) FROM GoldCham g2 WHERE g2.champion_name = :champion_name)")
    List<GoldCham> findByAnal(@Param("champion_name") String champion_name);

}
