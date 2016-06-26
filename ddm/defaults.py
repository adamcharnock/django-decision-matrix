from django.conf import settings


DDM_SCORE_MIN = getattr(settings, 'DDM_SCORE_MIN', 0)
DDM_SCORE_MAX = getattr(settings, 'DDM_SCORE_MAX', 5)

DDM_WEIGHT_MIN = getattr(settings, 'DDM_WEIGHT_MIN', 0)
DDM_WEIGHT_MAX = getattr(settings, 'DDM_WEIGHT_MAX', 5)

DDM_WEIGHT_WORDS = (
    (4.5, 'Mandatory'),
    (3.5, 'Important'),
    (2.5, 'Desired'),
    (1.0, 'Unimportant'),
    (0, 'Irrelevant'),
)

# Variances in scores/weights above this value will
# be flagged up
VARIANCE_CUTOFF = getattr(settings, 'VARIANCE_CUTOFF', 1.0)

DDM_EXTENSIONS = getattr(settings, 'DDM_EXTENSIONS', {
    # Example:
    # 'ddm.core.models.Criterion': ['my_app.extensions.CriterionExtension'],
})
