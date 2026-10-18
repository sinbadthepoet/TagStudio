# SPDX-FileCopyrightText: (c) TagStudio Contributors
# SPDX-License-Identifier: GPL-3.0-only


from pathlib import Path
from typing import override

import structlog
from PIL.Image import Image

from tagstudio.core.enums import Theme
from tagstudio.core.media_types import MediaTypes
from tagstudio.previews.base_preview import RENDER, BasePreview
from tagstudio.previews.renderers.archive import first_image_in_archive, open_archive

logger = structlog.get_logger(__name__)


class EbookPreview(BasePreview):
    media_type_name = "ebook"
    priority = 40

    @override
    @classmethod
    def register_types(cls) -> None:
        MediaTypes.register("ebook", ".azw", RENDER)
        MediaTypes.register("ebook", ".azw3", RENDER)
        MediaTypes.register("ebook", ".djvu", RENDER)
        MediaTypes.register("ebook", ".epub", RENDER)
        MediaTypes.register("ebook", ".fb2", RENDER)
        MediaTypes.register("ebook", ".ibook", RENDER)
        MediaTypes.register("ebook", ".kfx", RENDER)
        MediaTypes.register("ebook", ".lit", RENDER)
        MediaTypes.register("ebook", ".mobi", RENDER)
        MediaTypes.register("ebook", ".prc", RENDER)

    @override
    @classmethod
    def render(
        cls,
        filepath: Path,
        is_small: bool,
        theme: Theme,
        size: tuple[int, int],
        dpi_scale: float,
    ) -> Image | None:
        return epub_thumb(filepath, size)


def epub_thumb(filepath: Path, size: tuple[int, int] | None = None) -> Image | None:
    """Extracts the first image found in the ePub file.

    Args:
        filepath (Path): The path to the ePub file.
        size (tuple[int, int] | None): The size of the thumbnail, if known.

    Returns:
        Image: The first image found in the ePub file, or None by default.
    """
    im: Image | None = None
    try:
        with open_archive(filepath) as archive:
            im = first_image_in_archive(archive, size)
    except Exception as e:
        logger.error("Couldn't render thumbnail", filepath=filepath, error=type(e).__name__)

    return im
