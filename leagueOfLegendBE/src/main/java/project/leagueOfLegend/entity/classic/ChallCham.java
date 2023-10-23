package project.leagueOfLegend.entity.classic;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ChallCham {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int idx;

    private String tier;
    private String champion_name;
    private String champion_id;
    private String team_position;
    private Integer match_cnt;
    private Integer win_cnt;
    private Integer ban_cnt;
    private Integer pick_cnt;
    private Double win_rate;
    private Double ban_rate;
    private Double pick_rate;
    private Double av_kda;
    private String most_priperk1;
    private String most_priperk2;
    private String most_priperk3;
    private String most_priperk4;
    private String most_pristyle;
    private String most_subperk1;
    private String most_subperk2;
    private String most_substyle;
    private String abil_def;
    private String abil_fle;
    private String abil_off;
    private String spell1_1;
    private String spell1_2;
    private Integer spell1_cnt;
    private Double spell1_rate;
    private Double spell1_win;
    private String spell2_1;
    private String spell2_2;
    private Integer spell2_cnt;
    private Double spell2_rate;
    private Double spell2_win;
    private String skill_build1;
    private String skill_build2;
    private String  skill_build3;
    private Integer skill_cnt;
    private Double skill_rate;
    private Double skill_win;
    private String itemSet1_1;
    private String itemSet1_2;
    private String itemSet1_3;
    private String itemSet1_4;
    private String itemSet1_5;
    private String itemSet1_6;
    private String itemSet1_7;
    private String itemSet1_8;
    private Integer itemSet1_cnt;
    private Double itemSet1_rate;
    private Double itemSet1_win;
    private String itemSet2_1;
    private String itemSet2_2;
    private String itemSet2_3;
    private String itemSet2_4;
    private String itemSet2_5;
    private String itemSet2_6;
    private String itemSet2_7;
    private String itemSet2_8;
    private Integer itemSet2_cnt;
    private Double itemSet2_rate;
    private Double itemSet2_win;
    private String shoes1;
    private Integer shoes1_cnt;
    private Double shoes1_rate;
    private Double shoes1_win;
    private String shoes2;
    private Integer shoes2_cnt;
    private Double shoes2_rate;
    private Double shoes2_win;
    private String core1_1;
    private String core1_2;
    private String core1_3;
    private String core1_4;
    private String core1_5;
    private String core1_6;
    private Integer core1_cnt;
    private Double core1_rate;
    private Double core1_win;
    private String core2_1;
    private String core2_2;
    private String core2_3;
    private String core2_4;
    private String core2_5;
    private String core2_6;
    private Integer core2_cnt;
    private Double core2_rate;
    private Double core2_win;
    private String core3_1;
    private String core3_2;
    private String core3_3;
    private String core3_4;
    private String core3_5;
    private String core3_6;
    private Integer core3_cnt;
    private Double core3_rate;
    private Double core3_win;


}
