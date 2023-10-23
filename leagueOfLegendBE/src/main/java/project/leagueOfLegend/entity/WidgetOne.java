package project.leagueOfLegend.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity
@JsonNaming(PropertyNamingStrategy.UpperCamelCaseStrategy.class)
public class WidgetOne {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int IDX;

    @Column
    private Boolean Classic_An = false;

    @Column
    private Boolean Classic_Ti = false;

    @Column
    private Boolean Aram_An = false;

    @Column
    private Boolean Aram_Ti = false;

    @OneToOne
    private User user;

    public void setClassic_An(boolean Classic_An) {
        if(Classic_An) {
            this.Classic_An = Classic_An;
            this.Classic_Ti = false;
            this.Aram_An = false;
            this.Aram_Ti = false;
        } else {
            this.Classic_An = Classic_An;
        }
    }
    public void setClassic_Ti(boolean Classic_Ti) {
        if(Classic_Ti) {
            this.Classic_An = false;
            this.Classic_Ti = Classic_Ti;
            this.Aram_An = false;
            this.Aram_Ti = false;
        } else {
            this.Classic_Ti = Classic_Ti;
        }
    }
    public void setAram_An(boolean Aram_An) {
        if(Aram_An) {
            this.Classic_An = false;
            this.Classic_Ti = false;
            this.Aram_An = Aram_An;
            this.Aram_Ti = false;
        } else {
            this.Aram_An = Aram_An;
        }
    }
    public void setAram_Ti(boolean Aram_Ti) {
        if(Aram_Ti) {
            this.Classic_An = false;
            this.Classic_Ti = false;
            this.Aram_An = false;
            this.Aram_Ti = Aram_Ti;
        } else {
            this.Aram_Ti = Aram_Ti;
        }
    }

}
