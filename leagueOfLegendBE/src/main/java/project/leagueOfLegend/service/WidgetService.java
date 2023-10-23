package project.leagueOfLegend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import project.leagueOfLegend.dto.*;
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

    public ResponseDto<WidgetResponseDto> updateWidgetOne(WidgetOneDto dto) {
        String userId = dto.getUserId();
        String columnName = dto.getColumnName();


//        User user = User.builder().userId(userId).build();


        User user = userRepository.findByUserId(userId);
        WidgetOne widgetOne = this.widgetOneRepository.findByUser(user);

        switch (columnName) {
            case "Classic_An":
                widgetOne.setClassic_An(true);
                break;
            case "Classic_Ti":
                widgetOne.setClassic_Ti(true);
                break;
            case "Aram_An":
                widgetOne.setAram_An(true);
                break;
            case "Aram_Ti":
                widgetOne.setAram_Ti(true);
                break;
            default:
                throw new IllegalArgumentException("올바르지 않습니다.");
        }
        widgetOneRepository.save(widgetOne);
        WidgetResponseDto widgetResponseDto = new WidgetResponseDto(userId, columnName);
        return ResponseDto.setSuccess("위젯1 변경 성공", widgetResponseDto);
 }

    public ResponseDto<WidgetResponseDto> updateWidgetTwo(WidgetTwoDto dto) {
        String userId = dto.getUserId();
        String columnName = dto.getColumnName();

        User user = userRepository.findByUserId(userId);

        WidgetTwo widgetTwo = this.widgetTwoRepository.findByUser(user);

        switch (columnName) {
            case "Classic_An":
                widgetTwo.setClassic_An(true);
                break;
            case "Classic_Ti":
                widgetTwo.setClassic_Ti(true);
                break;
            case "Aram_An":
                widgetTwo.setAram_An(true);
                break;
            case "Aram_Ti":
                widgetTwo.setAram_Ti(true);
                break;
            default:
                throw new IllegalArgumentException("올바르지 않습니다.");
        }
        widgetTwoRepository.save(widgetTwo);
        WidgetResponseDto widgetResponseDto = new WidgetResponseDto(userId, columnName);
        return ResponseDto.setSuccess("위젯2 변경 성공", widgetResponseDto);
    }

    }
