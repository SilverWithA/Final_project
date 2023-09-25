package project.leagueOfLegend.controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/") // Request의 URL 패턴을보고 해당하는 패턴이 왔을때 해당 클래스 실행
public class MainController {

    @GetMapping("")
    public String hello() {
        return "Connection Successful";
    }
}
