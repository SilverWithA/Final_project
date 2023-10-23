package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import project.leagueOfLegend.entity.classic.BroCham;

import java.util.List;

@Repository
public interface BroChamRepository extends JpaRepository<BroCham, Integer> {
    @Query("select b from BroCham b where b.team_position = :team_position")
    List<BroCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT b FROM BroCham b WHERE b.champion_name = :champion_name AND b.win_cnt = (SELECT MAX(b2.win_cnt) FROM BroCham b2 WHERE b2.champion_name = :champion_name)")
    List<BroCham> findByAnal(@Param("champion_name") String champion_name);
}

