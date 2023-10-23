package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.ChallCham;

import java.util.List;

public interface ChallChamRepository extends JpaRepository<ChallCham, Integer> {
    @Query("select c from ChallCham c where c.team_position = :team_position")
    List<ChallCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT c FROM ChallCham c WHERE c.champion_name = :champion_name AND c.win_cnt = (SELECT MAX(c2.win_cnt) FROM ChallCham c2 WHERE c2.champion_name = :champion_name)")
    List<ChallCham> findByAnal(@Param("champion_name") String champion_name);
}
