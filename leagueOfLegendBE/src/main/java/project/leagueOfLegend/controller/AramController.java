package project.leagueOfLegend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import project.leagueOfLegend.dto.cham.ChamDto;
import project.leagueOfLegend.dto.cham.ChamResponseDto;
import project.leagueOfLegend.dto.cham.ResponseChamDto;
import project.leagueOfLegend.dto.cham.TierDto;
import project.leagueOfLegend.service.aram.AramAnalService;
import project.leagueOfLegend.service.aram.AramTierService;

import javax.lang.model.util.Elements;

@RestController
@RequestMapping("api/aram")
@CrossOrigin(origins = "http://52.79.230.210:3000")
public class AramController {

    @Autowired
    AramAnalService aramAnalService;
    @Autowired
    AramTierService aramTierService;

    @PostMapping("/anal")
    public ResponseChamDto<ChamResponseDto> getAramAnal(@RequestBody ChamDto requestBody) {
        ResponseChamDto<ChamResponseDto> result = aramAnalService.AramAnal(requestBody);
        return result;
    }
    @PostMapping("/tier")
    public ResponseChamDto<ChamResponseDto> getAramTier() {
        ResponseChamDto<ChamResponseDto> result = aramTierService.AramTier();
        return result;
    }
}