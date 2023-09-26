package project.leagueOfLegend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import project.leagueOfLegend.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User, String> {

    public boolean existsByUserIdAndUserPassword(String userId, String userPassword);

    public User findByUserId(String userId);

}
