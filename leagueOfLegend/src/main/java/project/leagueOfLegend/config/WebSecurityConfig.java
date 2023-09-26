package project.leagueOfLegend.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import project.leagueOfLegend.filter.JwtAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class WebSecurityConfig {

    @Autowired
    JwtAuthenticationFilter jwtAuthenticationFilter;

    @Bean
    protected SecurityFilterChain configure(HttpSecurity httpSecurity) throws Exception{
        httpSecurity
                // cors 정책 (현재 메인에서 작업 해둠)
//                .cors(Customizer.withDefaults())
                .cors().and()
                // csrf - 대책 (현재는 csrf에 대한 대책을 비활성화)
//                .csrf((csrf) -> csrf.disable())
                .csrf().disable()
                // basic 인증 (현재는 bearer 사용중으로 비활성화)
//                .httpBasic((httpBasic) -> httpBasic.disable())
                .httpBasic().disable()
                // 세션 기반 인증 ( 현재는 session 기반 인증을 사용하지 않음
//                .sessionManagement((sessionManagement) -> sessionManagement.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS).and()
                // '/', '/api/auth' 모듈에 대하서는 모두 허용 ( 인증을 하지 않고 사용 가능하게 함 )
                // 나머지 Request에 대해서는 모두 인증된 사용자만 사용 가능하게 함
//                .authorizeHttpRequests((authorizeHttpRequests) -> authorizeHttpRequests.requestMatchers("/","/api/auth/**")
//                .authorizeHttpRequests((authorizeHttpRequests) -> authorizeHttpRequests.requestMatchers("/","/api/auth/**")
//                        .permitAll().anyRequest().authenticated());
                .authorizeRequests().antMatchers("/", "/api/auth/**","/api/widget/**").permitAll()
                .anyRequest().authenticated();


                // 나머지 Request에 대해서는 모두 인증된 사용자만 사용 가능하게 함


        httpSecurity.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        return httpSecurity.build();
    }
}
