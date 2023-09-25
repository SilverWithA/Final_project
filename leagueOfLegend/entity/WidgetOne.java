package project.leagueOfLegend.entity;

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
public class WidgetOne {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int IDX;

    @Column
    private Boolean Classic_Na = false;

    @Column
    private Boolean Classic_Ti = false;

    @Column
    private Boolean Aram_An = false;

    @Column
    private Boolean Aram_Ti = false;

    @OneToOne
    private User user;
}
