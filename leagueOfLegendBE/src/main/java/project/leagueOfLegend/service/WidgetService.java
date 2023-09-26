package project.leagueOfLegend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import project.leagueOfLegend.dto.WidgetOneDto;
import project.leagueOfLegend.dto.WidgetTwoDto;
import project.leagueOfLegend.entity.User;
import project.leagueOfLegend.entity.WidgetOne;
import project.leagueOfLegend.entity.WidgetTwo;
import project.leagueOfLegend.repository.UserRepository;
import project.leagueOfLegend.repository.WidgetOneRepository;
import project.leagueOfLegend.repository.WidgetTwoRepository;

@Service
@RequiredArgsConstructor
public class WidgetService {

    private final WidgetOneRepository widgetOneRepository;
    private final UserRepository userRepository;
    private final WidgetTwoRepository widgetTwoRepository;

    public WidgetOne updateWidgetOne(WidgetOneDto dto) {
        String userId = dto.getUserId();
        String columnName = dto.getColumnName();
        boolean newValue = dto.isNewValue();

        User user = userRepository.findByUserId(userId);
        WidgetOne widgetOne = this.widgetOneRepository.findByUser(user);

        switch (columnName) {
            case "Classic_An":
                widgetOne.setClassic_An(newValue);
                break;
            case "Classic_Ti":
                widgetOne.setClassic_Ti(newValue);
                break;
            case "Aram_An":
                widgetOne.setAram_An(newValue);
                break;
            case "Aram_Ti":
                widgetOne.setAram_Ti(newValue);
                break;
            default:
                throw new IllegalArgumentException("올바르지 않습니다.");
        }
        return widgetOneRepository.save(widgetOne);
    }


    public WidgetTwo updateWidgetTwo(WidgetTwoDto dto) {
        String userId = dto.getUserId();
        String columnName = dto.getColumnName();
        boolean newValue = dto.isNewValue();

        User user = userRepository.findByUserId(userId);
        WidgetTwo widgetTwo = this.widgetTwoRepository.findByUser(user);

        switch (columnName) {
            case "Classic_An":
                widgetTwo.setClassic_An(newValue);
                break;
            case "Classic_Ti":
                widgetTwo.setClassic_Ti(newValue);
                break;
            case "Aram_An":
                widgetTwo.setAram_An(newValue);
                break;
            case "Aram_Ti":
                widgetTwo.setAram_Ti(newValue);
                break;
            default:
                throw new IllegalArgumentException("올바르지 않습니다.");
        }
        return widgetTwoRepository.save(widgetTwo);
    }

    }
