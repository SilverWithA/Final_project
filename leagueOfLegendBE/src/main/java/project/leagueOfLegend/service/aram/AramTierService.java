package project.leagueOfLegend.service.aram;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import project.leagueOfLegend.dto.cham.ResponseChamDto;
import project.leagueOfLegend.entity.aram.AramCham;
import project.leagueOfLegend.repository.aram.AramChamRepository;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional
@RequiredArgsConstructor
public class AramTierService {
    private final AramChamRepository aramChamRepository;

    public ResponseChamDto AramTier() {

            List list = new ArrayList<>();
        try {
            List<AramCham> Aramlist = aramChamRepository.findAll();
            list = Aramlist;
        } catch (Exception Error) {
            return ResponseChamDto.setFailed(Error.getMessage());
        }
        return ResponseChamDto.setSuccess("성공", list);
    }

}
