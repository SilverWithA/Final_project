package project.leagueOfLegend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import project.leagueOfLegend.entity.WidgetOne;

import javax.validation.constraints.NotBlank;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SignInDto {
    @NotBlank
    private String userId;
    @NotBlank
    private String userPassword;
    @NotBlank
    private WidgetOne widgetOne;
}
