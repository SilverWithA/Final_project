package project.leagueOfLegend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import project.leagueOfLegend.dto.WidgetOneDto;
import project.leagueOfLegend.dto.WidgetTwoDto;
import project.leagueOfLegend.entity.WidgetOne;
import project.leagueOfLegend.entity.WidgetTwo;
import project.leagueOfLegend.service.WidgetService;

@RestController
@RequestMapping("api/widget")
public class WidgetController {
    @Autowired WidgetService widgetService;

    @PutMapping("/one")
    public WidgetOne updateColumnOne(@RequestBody WidgetOneDto requestBody)
    {
        return widgetService.updateWidgetOne(requestBody);
    }

    @PutMapping("/two")
    public WidgetTwo updateColumnTwo(@RequestBody WidgetTwoDto requestBody) {
        return widgetService.updateWidgetTwo(requestBody);
    }
}
