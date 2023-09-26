package project.leagueOfLegend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import project.leagueOfLegend.entity.User;
import project.leagueOfLegend.entity.WidgetOne;
import project.leagueOfLegend.entity.WidgetTwo;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SignInResponseDto {
    private String token;
    private int exprTime;
    private User user;
    private WidgetOne widgetOne;
    private WidgetTwo widgetTwo;
}
