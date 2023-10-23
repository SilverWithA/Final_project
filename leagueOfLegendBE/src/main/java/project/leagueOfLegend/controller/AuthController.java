package project.leagueOfLegend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import project.leagueOfLegend.dto.ResponseDto;
import project.leagueOfLegend.dto.SignInDto;
import project.leagueOfLegend.dto.SignInResponseDto;
import project.leagueOfLegend.dto.SignUpDto;
import project.leagueOfLegend.service.AuthService;

@RestController
@RequestMapping("api/auth")
@CrossOrigin(origins = "http://52.79.230.210/:3000")
public class AuthController {
    @Autowired
    AuthService authService;
    @PostMapping("/signUp")
    public ResponseDto<?> signUp(@RequestBody SignUpDto requestBody) {
        ResponseDto<?> result = authService.signUp(requestBody);
        return result;
    }

    @PostMapping("/signIn")
    public ResponseDto<SignInResponseDto> signIn(@RequestBody SignInDto requestBody) {
        ResponseDto<SignInResponseDto> result = authService.signIn(requestBody);
        return result;
    }
}
