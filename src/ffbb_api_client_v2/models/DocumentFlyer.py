from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils.converter_utils import (
    from_datetime,
    from_int,
    from_list,
    from_none,
    from_str,
    from_union,
    is_type,
    to_class,
    to_enum,
)
from .DocumentFlyerType import DocumentFlyerType
from .FacetStats import FacetStats
from .Folder import Folder
from .Source import Source


class DocumentFlyer:
    id: UUID | None = None
    storage: str | None = None
    filename_disk: str | None = None
    filename_download: str | None = None
    title: str | None = None
    type: DocumentFlyerType | None = None
    uploaded_on: datetime | None = None
    modified_on: datetime | None = None
    charset: None
    filesize: int | None = None
    width: int | None = None
    height: int | None = None
    duration: None
    embed: None
    description: None
    location: None
    tags: None
    metadata: FacetStats | None = None
    source: Source | None = None
    credits: None
    gradient_color: str | None = None
    md5: str | None = None
    newsbridge_media_id: None
    newsbridge_metadatas: None
    newsbridge_name: None
    newsbridge_recorded_at: None
    focal_point_x: None
    focal_point_y: None
    newsbridge_labels: list[Any] | None = None
    newsbridge_persons: list[Any] | None = None
    folder: Folder | None = None
    uploaded_by: None
    modified_by: None
    newsbridge_mission: None

    @staticmethod
    def from_dict(obj: Any) -> DocumentFlyer:
        assert isinstance(obj, dict)
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        storage = from_union([from_str, from_none], obj.get("storage"))
        filename_disk = from_union([from_str, from_none], obj.get("filename_disk"))
        filename_download = from_union(
            [from_str, from_none], obj.get("filename_download")
        )
        title = from_union([from_str, from_none], obj.get("title"))
        type = from_union([DocumentFlyerType, from_none], obj.get("type"))
        uploaded_on = from_union([from_datetime, from_none], obj.get("uploaded_on"))
        modified_on = from_union([from_datetime, from_none], obj.get("modified_on"))
        charset = from_none(obj.get("charset"))
        filesize = from_union(
            [lambda x: int(from_str(x)), from_none], obj.get("filesize")
        )
        width = from_union([from_int, from_none], obj.get("width"))
        height = from_union([from_int, from_none], obj.get("height"))
        duration = from_none(obj.get("duration"))
        embed = from_none(obj.get("embed"))
        description = from_none(obj.get("description"))
        location = from_none(obj.get("location"))
        tags = from_none(obj.get("tags"))
        metadata = from_union([FacetStats.from_dict, from_none], obj.get("metadata"))
        source = from_union([Source, from_none], obj.get("source"))
        credits = from_none(obj.get("credits"))
        gradient_color = from_union([from_str, from_none], obj.get("gradient_color"))
        md5 = from_union([from_str, from_none], obj.get("md5"))
        newsbridge_media_id = from_none(obj.get("newsbridge_media_id"))
        newsbridge_metadatas = from_none(obj.get("newsbridge_metadatas"))
        newsbridge_name = from_none(obj.get("newsbridge_name"))
        newsbridge_recorded_at = from_none(obj.get("newsbridge_recorded_at"))
        focal_point_x = from_none(obj.get("focal_point_x"))
        focal_point_y = from_none(obj.get("focal_point_y"))
        newsbridge_labels = from_union(
            [lambda x: from_list(lambda x: x, x), from_none],
            obj.get("newsbridge_labels"),
        )
        newsbridge_persons = from_union(
            [lambda x: from_list(lambda x: x, x), from_none],
            obj.get("newsbridge_persons"),
        )
        folder = from_union([Folder.from_dict, from_none], obj.get("folder"))
        uploaded_by = from_none(obj.get("uploaded_by"))
        modified_by = from_none(obj.get("modified_by"))
        newsbridge_mission = from_none(obj.get("newsbridge_mission"))
        return DocumentFlyer(
            id,
            storage,
            filename_disk,
            filename_download,
            title,
            type,
            uploaded_on,
            modified_on,
            charset,
            filesize,
            width,
            height,
            duration,
            embed,
            description,
            location,
            tags,
            metadata,
            source,
            credits,
            gradient_color,
            md5,
            newsbridge_media_id,
            newsbridge_metadatas,
            newsbridge_name,
            newsbridge_recorded_at,
            focal_point_x,
            focal_point_y,
            newsbridge_labels,
            newsbridge_persons,
            folder,
            uploaded_by,
            modified_by,
            newsbridge_mission,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        if self.id is not None:
            result["id"] = from_union([lambda x: str(x), from_none], self.id)
        if self.storage is not None:
            result["storage"] = from_union([from_str, from_none], self.storage)
        if self.filename_disk is not None:
            result["filename_disk"] = from_union(
                [from_str, from_none], self.filename_disk
            )
        if self.filename_download is not None:
            result["filename_download"] = from_union(
                [from_str, from_none], self.filename_download
            )
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.type is not None:
            result["type"] = from_union(
                [lambda x: to_enum(DocumentFlyerType, x), from_none], self.type
            )
        if self.uploaded_on is not None:
            result["uploaded_on"] = from_union(
                [lambda x: x.isoformat(), from_none], self.uploaded_on
            )
        if self.modified_on is not None:
            result["modified_on"] = from_union(
                [lambda x: x.isoformat(), from_none], self.modified_on
            )
        if self.charset is not None:
            result["charset"] = from_none(self.charset)
        if self.filesize is not None:
            result["filesize"] = from_union(
                [
                    lambda x: from_none((lambda x: is_type(type(None), x))(x)),
                    lambda x: from_str(
                        (lambda x: str((lambda x: is_type(int, x))(x)))(x)
                    ),
                ],
                self.filesize,
            )
        if self.width is not None:
            result["width"] = from_union([from_int, from_none], self.width)
        if self.height is not None:
            result["height"] = from_union([from_int, from_none], self.height)
        if self.duration is not None:
            result["duration"] = from_none(self.duration)
        if self.embed is not None:
            result["embed"] = from_none(self.embed)
        if self.description is not None:
            result["description"] = from_none(self.description)
        if self.location is not None:
            result["location"] = from_none(self.location)
        if self.tags is not None:
            result["tags"] = from_none(self.tags)
        if self.metadata is not None:
            result["metadata"] = from_union(
                [lambda x: to_class(FacetStats, x), from_none], self.metadata
            )
        if self.source is not None:
            result["source"] = from_union(
                [lambda x: to_enum(Source, x), from_none], self.source
            )
        if self.credits is not None:
            result["credits"] = from_none(self.credits)
        if self.gradient_color is not None:
            result["gradient_color"] = from_union(
                [from_str, from_none], self.gradient_color
            )
        if self.md5 is not None:
            result["md5"] = from_union([from_str, from_none], self.md5)
        if self.newsbridge_media_id is not None:
            result["newsbridge_media_id"] = from_none(self.newsbridge_media_id)
        if self.newsbridge_metadatas is not None:
            result["newsbridge_metadatas"] = from_none(self.newsbridge_metadatas)
        if self.newsbridge_name is not None:
            result["newsbridge_name"] = from_none(self.newsbridge_name)
        if self.newsbridge_recorded_at is not None:
            result["newsbridge_recorded_at"] = from_none(self.newsbridge_recorded_at)
        if self.focal_point_x is not None:
            result["focal_point_x"] = from_none(self.focal_point_x)
        if self.focal_point_y is not None:
            result["focal_point_y"] = from_none(self.focal_point_y)
        if self.newsbridge_labels is not None:
            result["newsbridge_labels"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none], self.newsbridge_labels
            )
        if self.newsbridge_persons is not None:
            result["newsbridge_persons"] = from_union(
                [lambda x: from_list(lambda x: x, x), from_none],
                self.newsbridge_persons,
            )
        if self.folder is not None:
            result["folder"] = from_union(
                [lambda x: to_class(Folder, x), from_none], self.folder
            )
        if self.uploaded_by is not None:
            result["uploaded_by"] = from_none(self.uploaded_by)
        if self.modified_by is not None:
            result["modified_by"] = from_none(self.modified_by)
        if self.newsbridge_mission is not None:
            result["newsbridge_mission"] = from_none(self.newsbridge_mission)
        return result
