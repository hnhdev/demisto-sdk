import logging
from typing import List, Set

from demisto_sdk.commands.common.constants import MarketplaceVersions
from demisto_sdk.commands.content_graph.common import ContentType
from demisto_sdk.commands.content_graph.objects.integration_script import (
    IntegrationScript,
)

logger = logging.getLogger("demisto-sdk")


class Script(IntegrationScript, content_type=ContentType.SCRIPT):  # type: ignore[call-arg]
    tags: List[str]

    def metadata_fields(self) -> Set[str]:
        return {"name", "description", "tags"}

    def prepare_for_upload(
        self, marketplace: MarketplaceVersions = MarketplaceVersions.XSOAR, **kwargs
    ) -> dict:
        data = super().prepare_for_upload(marketplace, **kwargs)

        if supported_native_images := self.get_supported_native_images(
            marketplace=marketplace,
            ignore_native_image=kwargs.get("ignore_native_image") or False,
        ):
            logger.debug(
                f"Adding the following native images {supported_native_images} to script {self.object_id}"
            )
            data["nativeimage"] = supported_native_images

        return data
