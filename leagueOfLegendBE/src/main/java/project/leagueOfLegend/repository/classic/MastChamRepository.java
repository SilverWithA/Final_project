package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.MastCham;

import java.util.List;

public interface MastChamRepository extends JpaRepository<MastCham, Integer> {
    @Query("select m from MastCham m where m.team_position = :team_position")
    List<MastCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT m FROM MastCham m WHERE m.champion_name = :champion_name AND m.win_cnt = (SELECT MAX(m2.win_cnt) FROM MastCham m2 WHERE m2.champion_name = :champion_name)")
    List<MastCham> findByAnal(@Param("champion_name") String champion_name);

}
