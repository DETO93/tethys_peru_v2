from tethys_sdk.base import TethysAppBase


class NationalWaterLevelForecastPeru(TethysAppBase):
    """
    Tethys app class for National Water Level Forecast Peru.
    """

    name = 'National Water Level Forecast Peru'
    description = ''
    package = 'national_water_level_forecast_peru'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'national-water-level-forecast-peru'
    color = '#d35400'
    tags = ''
    enable_feedback = False
    feedback_emails = []