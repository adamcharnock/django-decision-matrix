from django.conf import settings


DDM_SCORE_MIN = getattr(settings, 'DDM_SCORE_MIN', 0),
DDM_SCORE_MAX = getattr(settings, 'DDM_SCORE_MAX', 5),

DDM_WEIGHT_MIN = getattr(settings, 'DDM_WEIGHT_MIN', 0),
DDM_WEIGHT_MAX = getattr(settings, 'DDM_WEIGHT_MAX', 5),
