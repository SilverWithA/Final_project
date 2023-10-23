package project.leagueOfLegend.dto.cham;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ChamDto {
    private String champion_name;
    private String tier;
}
