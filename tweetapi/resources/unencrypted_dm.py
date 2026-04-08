from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import ActionResponse, ApiResponse, PaginatedResponse


class UnencryptedDMResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def send_dm(self, *, auth_token: str, conversation_id: str, text: str, proxy: str, request_id: Optional[str] = None, media: Optional[list[Any]] = None) -> ActionResponse:
        """Send an unencrypted direct message."""
        return self._client._post("/tw-v2/interaction/send-dm", {
            "authToken": auth_token, "conversationId": conversation_id,
            "text": text, "proxy": proxy, "requestId": request_id, "media": media,
        })

    def get_dm_permissions(self, *, auth_token: str, recipient_ids: str, proxy: Optional[str] = None) -> ApiResponse:
        """Check DM permissions for recipients."""
        return self._client._get("/tw-v2/interaction/dm-permissions", {
            "authToken": auth_token, "recipientIds": recipient_ids, "proxy": proxy,
        })

    def get_inbox_initial_state(self, *, auth_token: str, proxy: Optional[str] = None) -> ApiResponse:
        """Get initial inbox state."""
        return self._client._get("/tw-v2/interaction/inbox-initial-state", {
            "authToken": auth_token, "proxy": proxy,
        })

    def get_inbox_trusted(self, *, auth_token: str, cursor: str, filter_low_quality: Optional[bool] = None, proxy: Optional[str] = None) -> PaginatedResponse:
        """Get trusted inbox conversations."""
        return self._client._get("/tw-v2/interaction/inbox-timeline-trusted", {
            "authToken": auth_token, "cursor": cursor,
            "filterLowQuality": filter_low_quality, "proxy": proxy,
        })

    def get_inbox_untrusted(self, *, auth_token: str, cursor: str, filter_low_quality: Optional[bool] = None, proxy: Optional[str] = None) -> PaginatedResponse:
        """Get untrusted (message requests) inbox conversations."""
        return self._client._get("/tw-v2/interaction/inbox-timeline-untrusted", {
            "authToken": auth_token, "cursor": cursor,
            "filterLowQuality": filter_low_quality, "proxy": proxy,
        })

    def get_conversation(self, *, auth_token: str, conversation_id: str, cursor: Optional[str] = None, proxy: Optional[str] = None) -> PaginatedResponse:
        """Get messages in a conversation."""
        return self._client._get("/tw-v2/interaction/conversation", {
            "authToken": auth_token, "conversationId": conversation_id,
            "cursor": cursor, "proxy": proxy,
        })

    def get_dm_user_updates(self, *, auth_token: str, cursor: str, proxy: Optional[str] = None) -> PaginatedResponse:
        """Get DM user updates."""
        return self._client._get("/tw-v2/interaction/dm-user-updates", {
            "authToken": auth_token, "cursor": cursor, "proxy": proxy,
        })

    def accept_conversation(self, *, auth_token: str, conversation_id: str, proxy: Optional[str] = None) -> ActionResponse:
        """Accept a conversation request."""
        return self._client._post("/tw-v2/interaction/accept-conversation", {
            "authToken": auth_token, "conversationId": conversation_id, "proxy": proxy,
        })
