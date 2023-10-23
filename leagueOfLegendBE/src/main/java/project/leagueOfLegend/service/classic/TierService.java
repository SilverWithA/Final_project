package project.leagueOfLegend.service.classic;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import project.leagueOfLegend.dto.cham.ResponseChamDto;
import project.leagueOfLegend.dto.cham.TierDto;
import project.leagueOfLegend.entity.classic.*;
import project.leagueOfLegend.repository.classic.*;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional
@RequiredArgsConstructor
public class TierService {
    private final IronChamRepository ironChamRepository;
    private final BroChamRepository broChamRepository;
    private final SilChamRepository silChamRepository;
    private final GoldChamRepository goldChamRepository;
    private final PlaChamRepository plaChamRepository;
    private final EmChamRepository emChamRepository;
    private final DiaChamRepository diaChamRepository;
    private final MastChamRepository mastChamRepository;
    private final GrandChamRepository grandChamRepository;
    private final ChallChamRepository challChamRepository;

    public ResponseChamDto Tier(TierDto dto) {
        String tier = dto.getTier();
        String team_position = dto.getTeam_position();

        switch (team_position) {
            case "탑":
                team_position = "TOP";
                break;
            case "정글":
                team_position = "JUNGLE";
                break;
            case "미드":
                team_position = "MIDDLE";
                break;
            case "바텀":
                team_position = "BOTTOM";
                break;
            case "서폿":
                team_position = "UTILITY";
                break;
        }

        List list = new ArrayList<>();

        List<IronCham> Ironlist = new ArrayList<>();
        List<BroCham> Brolist = new ArrayList<>();
        List<SilCham> Sillist = new ArrayList<>();
        List<GoldCham> Goldlist = new ArrayList<>();
        List<PlaCham> Plalist = new ArrayList<>();
        List<EmCham> Emlist = new ArrayList<>();
        List<DiaCham> Dialist = new ArrayList<>();
        List<MastCham> Mastlist = new ArrayList<>();
        List<GrandCham> Grandlist = new ArrayList<>();
        List<ChallCham> Challlist = new ArrayList<>();

        try {
                    switch (tier) {
                        case "아이언":
                            Ironlist = ironChamRepository.findByTier(team_position);
                            break;
                        case "브론즈":
                            Brolist = broChamRepository.findByTier(team_position);
                            break;
                        case "실버":
                            Sillist = silChamRepository.findByTier(team_position);
                            break;
                        case "골드":
                            Goldlist = goldChamRepository.findByTier(team_position);
                            break;
                        case "플레티넘":
                            Plalist = plaChamRepository.findByTier(team_position);
                            break;
                        case "에메랄드":
                            Emlist = emChamRepository.findByTier(team_position);
                            break;
                        case "다이아":
                            Dialist = diaChamRepository.findByTier(team_position);
                            break;
                        case "마스터":
                            Mastlist = mastChamRepository.findByTier(team_position);
                            break;
                        case "그랜드마스터":
                            Grandlist = grandChamRepository.findByTier(team_position);
                            break;
                        case "챌린저":
                            Challlist = challChamRepository.findByTier(team_position);
                            break;
                    }

            if (Ironlist.size() > 0) {
                list = Ironlist;
            } else if (Brolist.size() > 0) {
                list = Brolist;
            } else if (Sillist.size() > 0) {
                list = Sillist;
            } else if (Goldlist.size() > 0) {
                list = Goldlist;
            } else if (Plalist.size() > 0) {
                list = Plalist;
            } else if (Emlist.size() > 0) {
                list = Emlist;
            } else if (Dialist.size() > 0) {
                list = Dialist;
            } else if (Mastlist.size() > 0) {
                list = Mastlist;
            } else if (Grandlist.size() > 0) {
                list = Grandlist;
            } else if (Challlist.size() > 0) {
                list = Challlist;
            }
            if (list.isEmpty()) {
                return ResponseChamDto.setFailed("올바른 티어를 입력하세요");
            }
        } catch (Exception Error) {
            return ResponseChamDto.setFailed("다시 시도하세요");
        }

        return ResponseChamDto.setSuccess("success", list);
    }
}
