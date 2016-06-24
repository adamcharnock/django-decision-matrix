from django.conf import settings


def score_weight_bounds(request):
    return {
        'SCORE_MIN': settings.DDM_SCORE_MIN,
        'SCORE_MAX': settings.DDM_SCORE_MAX,
        'WEIGHT_MIN': settings.DDM_WEIGHT_MIN,
        'WEIGHT_MAX': settings.DDM_WEIGHT_MAX,
    }
