package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.GrandCham;

import java.util.List;

public interface GrandChamRepository extends JpaRepository<GrandCham, Integer> {
    @Query("select g from GrandCham g where g.team_position = :team_position")
    List<GrandCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT g FROM GrandCham g WHERE g.champion_name = :champion_name AND g.win_cnt = (SELECT MAX(g2.win_cnt) FROM GrandCham g2 WHERE g2.champion_name = :champion_name)")
    List<GrandCham> findByAnal(@Param("champion_name") String champion_name);

}