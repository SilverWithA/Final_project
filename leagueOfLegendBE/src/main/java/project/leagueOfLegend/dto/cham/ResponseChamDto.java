package project.leagueOfLegend.dto.cham;

import lombok.AllArgsConstructor;
import lombok.Data;
import project.leagueOfLegend.entity.classic.BroCham;

@Data
@AllArgsConstructor(staticName = "set")
public class ResponseChamDto<List>{
    public String message;
    public java.util.List<BroCham> list;
    public boolean result;

    public static  ResponseChamDto setSuccess(String message, java.util.List<BroCham> list) {
        return ResponseChamDto.set(message, list, true);
    }
    public static ResponseChamDto setFailed(String message) {
        return ResponseChamDto.set(message, null, false);
    }

}
