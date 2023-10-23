package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.SilCham;

import java.util.List;

public interface SilChamRepository extends JpaRepository<SilCham, Integer> {
    @Query("select s from SilCham s where s.team_position = :team_position")
    List<SilCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT s FROM SilCham s WHERE s.champion_name = :champion_name AND s.win_cnt = (SELECT MAX(s2.win_cnt) FROM SilCham s2 WHERE s2.champion_name = :champion_name)")
    List<SilCham> findByAnal(@Param("champion_name") String champion_name);

}