package project.leagueOfLegend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import project.leagueOfLegend.entity.User;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class WidgetTwoDto {
    private Boolean Classic_Na;
    private Boolean Classic_Ti;
    private Boolean Aram_An;
    private Boolean Aram_Ti;
    private User user;
}
