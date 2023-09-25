package project.leagueOfLegend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import project.leagueOfLegend.repository.WidgetOneRepository;

@Service
public class WidgetService {
    @Autowired
    WidgetOneRepository widgetOneRepository;

}
