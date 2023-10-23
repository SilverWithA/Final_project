package project.leagueOfLegend.dto.cham;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TierDto {
    private String tier;
    private String team_position;
}
