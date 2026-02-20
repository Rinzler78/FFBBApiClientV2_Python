from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from ...meilisearch.models.hit import Hit
from ...utils.converter_utils import (
    from_datetime,
    from_duration,
    from_int,
    from_list,
    from_str,
    from_uuid,
)
from .formation_session import FormationSession


@dataclass
class FormationsHit(Hit):
    id: str | None = None
    title: str | None = None
    type: str | None = None
    mode: str | None = None
    domain: str | None = None
    theme: str | None = None
    description: str | None = None
    goals: str | None = None
    public: str | None = None
    prerequisites: str | None = None
    content: str | None = None
    pedagogy: str | None = None
    certification: str | None = None
    results: str | None = None
    modalities: str | None = None
    level: str | None = None
    reference: str | None = None
    program_id_fbi: str | None = None
    duration_hours: timedelta | None = None
    sessions: list[FormationSession] | None = None
    files: list[Any] | None = None
    image: str | None = None
    thumbnail: str | None = None
    mode_hidden: str | None = None
    postal_codes: list[str] | None = None
    places: list[str] | None = None
    id_origin_hash: str | None = None
    date_end: datetime | None = None
    date_end_formatted: int | None = None
    date_start: datetime | None = None
    date_start_formatted: int | None = None
    entity: str | None = None
    formation_domain: str | None = None
    formation_duration_hours: str | None = None
    formation_id: UUID | None = None
    formation_image: str | None = None
    formation_mode: str | None = None
    formation_theme: str | None = None
    formation_thumbnail: str | None = None
    formation_title: str | None = None
    place: str | None = None
    postal_code: str | None = None
    reference_hidden: str | None = None
    subscribe_btn: str | None = None
    subscribe_button: str | None = None
    lower_title: str | None = field(init=False, default=None, repr=False)
    lower_domain: str | None = field(init=False, default=None, repr=False)
    lower_theme: str | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.lower_title = self.title.lower() if self.title else None
        self.lower_domain = self.domain.lower() if self.domain else None
        self.lower_theme = self.theme.lower() if self.theme else None

    @staticmethod
    def from_dict(obj: Any) -> FormationsHit:
        assert isinstance(obj, dict)
        id = from_str(obj, "id")
        title = from_str(obj, "title")
        type = from_str(obj, "type")
        mode = from_str(obj, "mode")
        domain = from_str(obj, "domain")
        theme = from_str(obj, "theme")
        description = from_str(obj, "description")
        goals = from_str(obj, "goals")
        public = from_str(obj, "public")
        prerequisites = from_str(obj, "prerequisites")
        content = from_str(obj, "content")
        pedagogy = from_str(obj, "pedagogy")
        certification = from_str(obj, "certification")
        results = from_str(obj, "results")
        modalities = from_str(obj, "modalities")
        level = from_str(obj, "level")
        reference = from_str(obj, "reference")
        program_id_fbi = from_str(obj, "programIdFbi")
        duration_hours = from_duration(obj, "duration_hours")
        sessions = from_list(FormationSession.from_dict, obj, "sessions")
        files = from_list(lambda x: x, obj, "files")
        image = from_str(obj, "image")
        thumbnail = from_str(obj, "thumbnail")
        mode_hidden = from_str(obj, "mode_hidden")
        postal_codes = from_list(str, obj, "postal_codes")
        places = from_list(str, obj, "places")
        id_origin_hash = from_str(obj, "id_origin_hash")
        date_end = from_datetime(obj, "date_end")
        date_end_formatted = from_int(obj, "date_end_formatted")
        date_start = from_datetime(obj, "date_start")
        date_start_formatted = from_int(obj, "date_start_formatted")
        entity = from_str(obj, "entity")
        formation_domain = from_str(obj, "formation_domain")
        formation_duration_hours = from_str(obj, "formation_duration_hours")
        formation_id = from_uuid(obj, "formation_id")
        formation_image = from_str(obj, "formation_image")
        formation_mode = from_str(obj, "formation_mode")
        formation_theme = from_str(obj, "formation_theme")
        formation_thumbnail = from_str(obj, "formation_thumbnail")
        formation_title = from_str(obj, "formation_title")
        place = from_str(obj, "place")
        postal_code = from_str(obj, "postal_code")
        reference_hidden = from_str(obj, "reference_hidden")
        subscribe_btn = from_str(obj, "subscribeBtn")
        subscribe_button = from_str(obj, "subscribe_button")
        return FormationsHit(
            id=id,
            title=title,
            type=type,
            mode=mode,
            domain=domain,
            theme=theme,
            description=description,
            goals=goals,
            public=public,
            prerequisites=prerequisites,
            content=content,
            pedagogy=pedagogy,
            certification=certification,
            results=results,
            modalities=modalities,
            level=level,
            reference=reference,
            program_id_fbi=program_id_fbi,
            duration_hours=duration_hours,
            sessions=sessions,
            files=files,
            image=image,
            thumbnail=thumbnail,
            mode_hidden=mode_hidden,
            postal_codes=postal_codes,
            places=places,
            id_origin_hash=id_origin_hash,
            date_end=date_end,
            date_end_formatted=date_end_formatted,
            date_start=date_start,
            date_start_formatted=date_start_formatted,
            entity=entity,
            formation_domain=formation_domain,
            formation_duration_hours=formation_duration_hours,
            formation_id=formation_id,
            formation_image=formation_image,
            formation_mode=formation_mode,
            formation_theme=formation_theme,
            formation_thumbnail=formation_thumbnail,
            formation_title=formation_title,
            place=place,
            postal_code=postal_code,
            reference_hidden=reference_hidden,
            subscribe_btn=subscribe_btn,
            subscribe_button=subscribe_button,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = self.id
        if self.title is not None:
            result["title"] = self.title
        if self.type is not None:
            result["type"] = self.type
        if self.mode is not None:
            result["mode"] = self.mode
        if self.domain is not None:
            result["domain"] = self.domain
        if self.theme is not None:
            result["theme"] = self.theme
        if self.description is not None:
            result["description"] = self.description
        if self.goals is not None:
            result["goals"] = self.goals
        if self.public is not None:
            result["public"] = self.public
        if self.prerequisites is not None:
            result["prerequisites"] = self.prerequisites
        if self.content is not None:
            result["content"] = self.content
        if self.pedagogy is not None:
            result["pedagogy"] = self.pedagogy
        if self.certification is not None:
            result["certification"] = self.certification
        if self.results is not None:
            result["results"] = self.results
        if self.modalities is not None:
            result["modalities"] = self.modalities
        if self.level is not None:
            result["level"] = self.level
        if self.reference is not None:
            result["reference"] = self.reference
        if self.program_id_fbi is not None:
            result["programIdFbi"] = self.program_id_fbi
        if self.duration_hours is not None:
            total_seconds = int(self.duration_hours.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes = remainder // 60
            result["duration_hours"] = f"{hours}h{minutes:02d}"
        if self.sessions is not None:
            result["sessions"] = [s.to_dict() for s in self.sessions]
        if self.files is not None:
            result["files"] = self.files
        if self.image is not None:
            result["image"] = self.image
        if self.thumbnail is not None:
            result["thumbnail"] = self.thumbnail
        if self.mode_hidden is not None:
            result["mode_hidden"] = self.mode_hidden
        if self.postal_codes is not None:
            result["postal_codes"] = self.postal_codes
        if self.places is not None:
            result["places"] = self.places
        if self.id_origin_hash is not None:
            result["id_origin_hash"] = self.id_origin_hash
        if self.date_end is not None:
            result["date_end"] = self.date_end.isoformat()
        if self.date_end_formatted is not None:
            result["date_end_formatted"] = self.date_end_formatted
        if self.date_start is not None:
            result["date_start"] = self.date_start.isoformat()
        if self.date_start_formatted is not None:
            result["date_start_formatted"] = self.date_start_formatted
        if self.entity is not None:
            result["entity"] = self.entity
        if self.formation_domain is not None:
            result["formation_domain"] = self.formation_domain
        if self.formation_duration_hours is not None:
            result["formation_duration_hours"] = self.formation_duration_hours
        if self.formation_id is not None:
            result["formation_id"] = str(self.formation_id)
        if self.formation_image is not None:
            result["formation_image"] = self.formation_image
        if self.formation_mode is not None:
            result["formation_mode"] = self.formation_mode
        if self.formation_theme is not None:
            result["formation_theme"] = self.formation_theme
        if self.formation_thumbnail is not None:
            result["formation_thumbnail"] = self.formation_thumbnail
        if self.formation_title is not None:
            result["formation_title"] = self.formation_title
        if self.place is not None:
            result["place"] = self.place
        if self.postal_code is not None:
            result["postal_code"] = self.postal_code
        if self.reference_hidden is not None:
            result["reference_hidden"] = self.reference_hidden
        if self.subscribe_btn is not None:
            result["subscribeBtn"] = self.subscribe_btn
        if self.subscribe_button is not None:
            result["subscribe_button"] = self.subscribe_button
        return result

    def is_valid_for_query(self, query: str) -> bool:
        return bool(
            not query
            or (self.lower_title and query in self.lower_title)
            or (self.lower_domain and query in self.lower_domain)
            or (self.lower_theme and query in self.lower_theme)
        )
