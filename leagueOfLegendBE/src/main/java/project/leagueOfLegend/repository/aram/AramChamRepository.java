package project.leagueOfLegend.repository.aram;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import project.leagueOfLegend.entity.aram.AramCham;

import java.util.List;

public interface AramChamRepository extends JpaRepository<AramCham, Integer> {

    @Query("select a from AramCham a where a.champion_name = :champion_name")
    List<AramCham> findByAramAnal(@Param("champion_name") String champion_name);

}
