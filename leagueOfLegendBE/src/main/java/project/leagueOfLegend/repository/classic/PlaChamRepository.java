package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.PlaCham;

import java.util.List;

public interface PlaChamRepository extends JpaRepository<PlaCham, Integer> {
    @Query("select p from PlaCham p where p.team_position = :team_position")
    List<PlaCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT p FROM PlaCham p WHERE p.champion_name = :champion_name AND p.win_cnt = (SELECT MAX(p2.win_cnt) FROM PlaCham p2 WHERE p2.champion_name = :champion_name)")
    List<PlaCham> findByAnal(@Param("champion_name") String champion_name);

}
