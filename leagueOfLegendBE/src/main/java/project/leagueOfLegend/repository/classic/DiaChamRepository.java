package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.DiaCham;

import java.util.List;

public interface DiaChamRepository extends JpaRepository<DiaCham, Integer> {
    @Query("select d from DiaCham d where d.team_position = :team_position")
    List<DiaCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT d FROM DiaCham d WHERE d.champion_name = :champion_name AND d.win_cnt = (SELECT MAX(d2.win_cnt) FROM DiaCham d2 WHERE d2.champion_name = :champion_name)")
    List<DiaCham> findByAnal(@Param("champion_name") String champion_name);
}
