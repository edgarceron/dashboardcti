from campaigns.models import CampaignForm, AnswersHeader

SALIENTE = 1
ENTRANTE = 2

def polls_attended(start_date, end_date, agent, campaign, type):
    if type = SALIENTE:
        campaign_manticore = CampaignForm.objects.filter(type=type, isabel_campaign=campaign)
