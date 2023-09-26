package project.leagueOfLegend.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;

// JWT : 전자 서명이 된 토큰
// JSON 형태로 구성
// {haeder}.{payload}.{signature}
// header : typ(해당 토큰의 타입), alg(토큰 서명시 사용된 해시 알고리즘)
// payload : sub(해당 토큰의 주인), iat(토큰이 발행된 시간), exp( 토큰이 만료되는 시간)
@Service
public class TokenProvider {

    // Jwt 생성 및 검증을 위한 키
    private static final String SECURITY_KEY = "jwtseckey!@";

    //Jwt 생성하는 매서드
    public String create (String userId) {
        // 만료 날짜를 현재 날짜 + 1시간
        Date exprTime = Date.from(Instant.now().plus(1, ChronoUnit.HOURS));

        // jwt 생성
        return Jwts.builder()
                // 암호화에 사용될 알고리즘, 키
                .signWith(SignatureAlgorithm.HS512, SECURITY_KEY)
                // jwt 제목, 생성일, 만료일
                .setSubject(userId).setIssuedAt(new Date(System.currentTimeMillis())).setExpiration(exprTime)
                // 생성
                .compact();
    }

    // jwt 검증
    public String validate (String token) {
        // 매개 변수로 받은 token을 키를 사용하여 복호화(디코딩)
        Claims claims = Jwts.parser().setSigningKey(SECURITY_KEY).parseClaimsJws(token).getBody();

        // 복호화된 토큰의 payload 에서 제목을 가져옴
        return claims.getSubject();
    }
}
