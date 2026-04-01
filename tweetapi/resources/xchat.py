from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI


class XChatResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def setup(self, *, auth_token: str, user_id: str, pin: str, proxy: Optional[str] = None) -> dict[str, Any]:
        """Initialize X Chat (encrypted DMs) for your account."""
        return self._client._post("/tw-v2/xchat/setup", {
            "authToken": auth_token, "userId": user_id, "pin": pin, "proxy": proxy,
        })

    def get_conversations(self, *, auth_token: str, cursor: Optional[str] = None, graph_snapshot_id: Optional[str] = None, limit: Optional[int] = None, proxy: Optional[str] = None) -> dict[str, Any]:
        """List encrypted DM conversations."""
        return self._client._post("/tw-v2/xchat/conversations", {
            "authToken": auth_token, "cursor": cursor,
            "graphSnapshotId": graph_snapshot_id, "limit": limit, "proxy": proxy,
        })

    def send(self, *, auth_token: str, recipient_id: str, message: str, proxy: Optional[str] = None) -> dict[str, Any]:
        """Send an encrypted message."""
        return self._client._post("/tw-v2/xchat/send", {
            "authToken": auth_token, "recipientId": recipient_id,
            "message": message, "proxy": proxy,
        })

    def get_history(self, *, auth_token: str, conversation_id: str, cursor: Optional[str] = None, limit: Optional[int] = None, proxy: Optional[str] = None) -> dict[str, Any]:
        """Get encrypted conversation history."""
        return self._client._post("/tw-v2/xchat/history", {
            "authToken": auth_token, "conversationId": conversation_id,
            "cursor": cursor, "limit": limit, "proxy": proxy,
        })

    def can_dm(self, *, auth_token: str, user_ids: list[str], proxy: Optional[str] = None) -> dict[str, Any]:
        """Check if you can send encrypted DMs to users."""
        return self._client._post("/tw-v2/xchat/can-dm", {
            "authToken": auth_token, "userIds": user_ids, "proxy": proxy,
        })
