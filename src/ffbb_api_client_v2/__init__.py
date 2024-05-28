import sys

from .api_ffbb_app_client import ApiFFBBAppClient  # noqa
from .competition import Competition  # noqa
from .competition_type import CompetitionType  # noqa
from .external_id import ExternalID  # noqa
from .http_requests_utils import http_get_json, http_post_json, url_with_params  # noqa
from .id_organisme_equipe import IDOrganismeEquipe  # noqa
from .id_poule import IDPoule  # noqa
from .lives import Live  # noqa
from .logo import Logo  # noqa
from .salle import Salle  # noqa
from .sex import Sex  # noqa
from .team_engagement import TeamEngagement  # noqa

if sys.version_info[:2] >= (3, 8):
    # T-238 Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "ffbb_api_client"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
