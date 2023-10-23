package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.EmCham;

import java.util.List;

public interface EmChamRepository extends JpaRepository<EmCham, Integer> {
    @Query("select e from EmCham e where e.team_position = :team_position")
    List<EmCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT e FROM EmCham e WHERE e.champion_name = :champion_name AND e.win_cnt = (SELECT MAX(e2.win_cnt) FROM EmCham e2 WHERE e2.champion_name = :champion_name)")
    List<EmCham> findByAnal(@Param("champion_name") String champion_name);


}
