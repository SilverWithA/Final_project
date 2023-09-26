package project.leagueOfLegend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import project.leagueOfLegend.entity.User;
import project.leagueOfLegend.entity.WidgetOne;


@Repository

public interface WidgetOneRepository extends JpaRepository<WidgetOne, Integer> {

    WidgetOne findByUser(User user);


}
