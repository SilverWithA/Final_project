package project.leagueOfLegend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import project.leagueOfLegend.dto.cham.ChamDto;
import project.leagueOfLegend.dto.cham.ChamResponseDto;
import project.leagueOfLegend.dto.cham.ResponseChamDto;
import project.leagueOfLegend.dto.cham.TierDto;
import project.leagueOfLegend.service.classic.AnalService;
import project.leagueOfLegend.service.classic.TierService;

@RestController
@RequestMapping("api/classic")
@CrossOrigin(origins = "http://52.79.230.210:3000")

public class ClassicController {
    @Autowired
    TierService tierService;
    @Autowired
    AnalService analService;

    @PostMapping("/tier")
    ResponseChamDto<ChamResponseDto> getTier(@RequestBody TierDto requestBody) {
        ResponseChamDto<ChamResponseDto> result = tierService.Tier(requestBody);
        return result;
    }

    @PostMapping("/anal")
    ResponseChamDto<ChamResponseDto> getAnal(@RequestBody ChamDto requestBody) {
        ResponseChamDto<ChamResponseDto> result = analService.Anal(requestBody);
        return result;
    }


}
