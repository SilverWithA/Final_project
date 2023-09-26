package project.leagueOfLegend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@AllArgsConstructor
@NoArgsConstructor
public class WidgetOneDto {
    private String userId;
    private String columnName;
    private boolean newValue;
}
