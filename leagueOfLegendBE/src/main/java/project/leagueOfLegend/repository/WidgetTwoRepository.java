package project.leagueOfLegend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import project.leagueOfLegend.entity.User;
import project.leagueOfLegend.entity.WidgetTwo;

@Repository
public interface WidgetTwoRepository extends JpaRepository<WidgetTwo, Integer> {
    WidgetTwo findByUser(User user);

}
