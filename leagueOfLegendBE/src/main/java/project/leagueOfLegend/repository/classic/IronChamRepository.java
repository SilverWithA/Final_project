package project.leagueOfLegend.repository.classic;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.classic.IronCham;

import java.util.List;

public interface IronChamRepository extends JpaRepository<IronCham, Integer> {

    @Query("select i from IronCham i where i.team_position = :team_position")
    List<IronCham> findByTier(@Param("team_position") String team_position);

    @Query("SELECT i FROM IronCham i WHERE i.champion_name = :champion_name AND i.win_cnt = (SELECT MAX(i2.win_cnt) FROM IronCham i2 WHERE i2.champion_name = :champion_name)")
    List<IronCham> findByAnal(@Param("champion_name") String champion_name);

}