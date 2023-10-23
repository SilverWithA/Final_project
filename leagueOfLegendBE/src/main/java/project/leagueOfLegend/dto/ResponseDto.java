package project.leagueOfLegend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor(staticName = "set")
public class ResponseDto<D> {
    public String message;

    public D data;
    public boolean result;

    public static <D> ResponseDto<D> setSuccess(String message, D data) {
        return ResponseDto.set(message, data, true);

    }
    public static <D> ResponseDto<D> setFailed(String message) {

        return ResponseDto.set(message, null, false);
    }

}
