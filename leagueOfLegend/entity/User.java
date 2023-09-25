package project.leagueOfLegend.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import project.leagueOfLegend.dto.SignUpDto;

import javax.persistence.*;
import javax.validation.constraints.NotNull;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class User {

    @Id
    @NotNull
    private String userId;

    @NotNull
    private String userPassword;

    public User(SignUpDto dto) {
        this.userId = dto.getUserId();
        this.userPassword = dto.getUserPassword();
    }
}
