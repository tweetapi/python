"""Response types for TweetAPI.

Uses TypedDict for lightweight, JSON-compatible type hints.
All types mirror the API's JSON response shapes exactly.
"""

from __future__ import annotations

from typing import Any, List as TypingList, Optional, TypedDict


# ─── Response Wrappers ───────────────────────────────────────────────────────


class ApiResponse(TypedDict):
    data: Any


class Pagination(TypedDict):
    nextCursor: Optional[str]
    prevCursor: Optional[str]


class PaginatedResponse(TypedDict):
    data: list[Any]
    pagination: Pagination


class SearchMeta(TypedDict):
    query: str
    resultType: str
    resultCount: int
    completedIn: int


class SearchResponse(TypedDict):
    data: list[Any]
    pagination: Pagination
    meta: SearchMeta


class ActionData(TypedDict, total=False):
    id: str
    action: str
    timestamp: str
    success: bool
    message: str
    metadata: dict[str, Any]


class ActionResponse(TypedDict):
    data: ActionData


# ─── User ────────────────────────────────────────────────────────────────────


class Professional(TypedDict, total=False):
    type: Optional[str]
    category: list[str]
    restId: Optional[str]


class BusinessAccount(TypedDict):
    affiliatesCount: int


class HighlightsInfo(TypedDict):
    canHighlight: bool
    highlightedTweetsCount: str


class User(TypedDict, total=False):
    id: str
    username: str
    name: str
    bio: str
    location: Optional[str]
    website: Optional[str]
    pinnedTweetIds: list[str]
    avatar: Optional[str]
    banner: Optional[str]
    profileImageShape: Optional[str]
    verified: bool
    isBlueVerified: bool
    verifiedType: Optional[str]
    verifiedSince: Optional[str]
    isIdentityVerified: bool
    isProtected: bool
    possiblySensitive: bool
    profileInterstitialType: Optional[str]
    withheldInCountries: list[str]
    professional: Optional[Professional]
    businessAccount: Optional[BusinessAccount]
    creatorSubscriptionsCount: int
    hasHiddenSubscriptions: bool
    highlightsInfo: Optional[HighlightsInfo]
    hasGraduatedAccess: bool
    isProfileTranslatable: bool
    hasCustomTimelines: bool
    isTranslator: bool
    affiliatesHighlightedLabel: Optional[dict[str, Any]]
    defaultProfile: bool
    defaultProfileImage: bool
    followerCount: int
    followingCount: int
    tweetCount: int
    listedCount: int
    mediaCount: int
    favoritesCount: int
    createdAt: Optional[str]


class UserRelationship(TypedDict, total=False):
    sourceId: str
    targetId: str
    following: bool
    followedBy: bool
    blocking: bool
    blockedBy: bool
    muting: bool
    notificationsEnabled: bool
    canDm: bool
    canMediaTag: bool
    wantRetweets: bool
    markedSpam: bool
    followRequestSent: bool
    followRequestReceived: bool
    allReplies: bool


class UserAnalytics(TypedDict, total=False):
    userId: str
    period: str
    impressions: int
    engagements: int
    engagementRate: float
    linkClicks: int
    profileVisits: int
    mentions: int
    newFollowers: int
    topTweet: Optional[str]
    detailedMetrics: dict[str, int]


# ─── Media ───────────────────────────────────────────────────────────────────


class MediaSize(TypedDict, total=False):
    width: int
    height: int
    resize: str
    url: str


class VideoVariant(TypedDict, total=False):
    bitrate: Optional[int]
    contentType: str
    url: str


class MediaAvailability(TypedDict):
    status: str
    reason: Optional[str]


class Media(TypedDict, total=False):
    id: str
    key: str
    type: str  # "photo" | "video" | "animated_gif"
    url: str
    displayUrl: str
    expandedUrl: str
    thumbnailUrl: Optional[str]
    width: int
    height: int
    aspectRatio: list[int]
    sizes: dict[str, MediaSize]
    duration: Optional[float]
    bitrate: Optional[int]
    videoInfo: Optional[dict[str, Any]]
    altText: Optional[str]
    sensitiveMedia: bool
    mediaAvailability: MediaAvailability
    allowDownload: bool
    mediaStats: Optional[dict[str, int]]
    sourceStatusId: Optional[str]
    sourceUserId: Optional[str]


# ─── Poll ────────────────────────────────────────────────────────────────────


class PollOption(TypedDict):
    position: int
    label: str
    voteCount: int
    percentage: float


class Poll(TypedDict, total=False):
    id: str
    options: list[PollOption]
    endDatetime: str
    durationMinutes: int
    votingStatus: str
    totalVotes: int


# ─── Card ────────────────────────────────────────────────────────────────────


class CardBindingValues(TypedDict, total=False):
    title: str
    description: str
    domain: str
    thumbnailImageUrl: Optional[str]
    thumbnailImageColor: Optional[str]
    playerUrl: Optional[str]
    playerWidth: Optional[int]
    playerHeight: Optional[int]
    appId: Optional[str]
    appName: Optional[str]


class Card(TypedDict, total=False):
    name: str
    url: str
    cardType: str
    type: str
    bindingValues: CardBindingValues
    vanityUrl: Optional[str]


# ─── Place ───────────────────────────────────────────────────────────────────


class Place(TypedDict, total=False):
    id: str
    fullName: str
    name: str
    country: str
    countryCode: str
    placeType: str
    url: str


# ─── Tweet ───────────────────────────────────────────────────────────────────


class ReplyTo(TypedDict):
    tweetId: str
    userId: str
    username: str


class Mention(TypedDict):
    id: str
    username: str
    name: str


class EditControl(TypedDict, total=False):
    editTweetIds: list[str]
    editableUntil: str
    isEditEligible: bool
    editsRemaining: int


class BirdwatchPivot(TypedDict, total=False):
    calloutText: str
    shortTitle: str
    noteId: str
    iconType: str
    destinationUrl: str


class ConversationControl(TypedDict, total=False):
    policy: str
    allowedUserIds: list[str]


class Tweet(TypedDict, total=False):
    id: str
    conversationId: Optional[str]
    text: str
    displayTextRange: list[int]
    author: User
    source: Optional[str]
    type: str  # "tweet" | "reply" | "quote" | "retweet" | "thread"
    replyTo: Optional[ReplyTo]
    quotedTweet: Optional[Any]  # recursive Tweet
    retweetedTweet: Optional[Any]
    likeCount: int
    retweetCount: int
    replyCount: int
    quoteCount: int
    bookmarkCount: int
    viewCount: Optional[int]
    media: Optional[list[Media]]
    poll: Optional[Poll]
    card: Optional[Card]
    hashtags: list[str]
    mentions: list[Mention]
    urls: list[str]
    symbols: list[str]
    possiblySensitive: bool
    limitedActions: Optional[str]
    hasAIGeneratedMedia: bool
    isPaidPromotion: bool
    isEdited: bool
    editControl: Optional[EditControl]
    isTranslatable: bool
    lang: str
    translatedText: Optional[str]
    hasBirdwatchNotes: bool
    birdwatchPivot: Optional[BirdwatchPivot]
    conversationControl: Optional[ConversationControl]
    isPromoted: bool
    communityId: Optional[str]
    createdAt: Optional[str]
    place: Optional[Place]


class TweetTranslation(TypedDict):
    text: str
    lang: str
    sourceLanguage: str
    destinationLanguage: str
    translationSource: str


# ─── List ────────────────────────────────────────────────────────────────────


class List(TypedDict, total=False):
    id: str
    name: str
    description: str
    mode: str  # "public" | "private"
    owner: User
    bannerUrl: Optional[str]
    facepileUrls: list[str]
    memberCount: int
    subscriberCount: int
    createdAt: Optional[str]
    slug: str
    uri: str


# ─── Community ───────────────────────────────────────────────────────────────


class CommunityRule(TypedDict):
    id: str
    name: str
    description: str
    order: int
    createdAt: str


class Community(TypedDict, total=False):
    id: str
    name: str
    description: str
    bannerUrl: Optional[str]
    avatarUrl: Optional[str]
    rules: list[CommunityRule]
    memberCount: int
    moderatorCount: int
    adminCount: int
    isPrivate: bool
    pinnedTweetId: Optional[str]
    createdAt: Optional[str]
    isMember: bool
    isAdmin: bool
    isModerator: bool
    canPost: bool


class CommunityMember(TypedDict, total=False):
    user: User
    role: str  # "member" | "moderator" | "admin"
    joinedAt: str


class CommunitySearchResult(TypedDict, total=False):
    id: str
    name: str
    memberCount: int
    topic: Optional[str]
    isNsfw: bool
    bannerUrl: Optional[str]
    defaultBannerUrl: Optional[str]
    membersFacepile: list[str]


# ─── Space ───────────────────────────────────────────────────────────────────


class SpaceParticipant(TypedDict, total=False):
    periscopeUserId: str
    twitterUserId: str
    username: str
    displayName: str
    avatarUrl: str
    isVerified: bool
    isBlueVerified: bool


class SpaceTopic(TypedDict):
    id: str
    name: str


class SpaceParticipants(TypedDict, total=False):
    admins: list[SpaceParticipant]
    speakers: list[SpaceParticipant]
    listeners: list[SpaceParticipant]
    total: int


class Space(TypedDict, total=False):
    id: str
    title: str
    state: str  # "Running" | "Ended" | "Scheduled" | "Canceled"
    mediaKey: str
    createdAt: int
    scheduledStart: Optional[int]
    startedAt: Optional[int]
    endedAt: Optional[int]
    updatedAt: Optional[int]
    creator: Optional[User]
    totalLiveListeners: int
    totalReplayWatched: int
    participants: SpaceParticipants
    isAvailableForReplay: bool
    topics: list[SpaceTopic]
    tweetId: Optional[str]


class SpaceStreamInfo(TypedDict, total=False):
    hlsUrl: str
    status: str
    streamType: str
    shareUrl: Optional[str]


# ─── Notification ────────────────────────────────────────────────────────────


class Notification(TypedDict, total=False):
    id: str
    type: str
    createdAt: str
    message: str
    icon: str
    fromUsers: list[str]
    targetTweetId: Optional[str]
    targetUserId: Optional[str]
    seen: bool


# ─── Auth ────────────────────────────────────────────────────────────────────


class LoginCookies(TypedDict):
    auth_token: str
    ct0: str
    twid: str
    kdt: str
    __cf_bm: str


class LoginUser(TypedDict):
    id: str
    username: str
    name: str


class LoginResponse(TypedDict):
    cookies: LoginCookies
    user: LoginUser
    timestamp: str


# ─── Typed Response Wrappers ────────────────────────────────────────────────
# Specific wrappers that give better IDE autocomplete than the generic
# ``ApiResponse`` / ``PaginatedResponse`` with ``data: Any``.


class UserResponse(TypedDict):
    data: User


class UsersResponse(TypedDict):
    data: list[User]


class UserPaginatedResponse(TypedDict):
    data: list[User]
    pagination: Pagination


class TweetResponse(TypedDict):
    data: Tweet


class TweetsPaginatedResponse(TypedDict):
    data: list[Tweet]
    pagination: Pagination


class TweetTranslationResponse(TypedDict):
    data: TweetTranslation


class UserRelationshipResponse(TypedDict):
    data: UserRelationship


class UserAnalyticsResponse(TypedDict):
    data: UserAnalytics


class ListResponse(TypedDict):
    data: List


class ListPaginatedResponse(TypedDict):
    data: list[Any]
    pagination: Pagination


class CommunityResponse(TypedDict):
    data: Community


class CommunityMemberPaginatedResponse(TypedDict):
    data: list[CommunityMember]
    pagination: Pagination


class CommunitySearchPaginatedResponse(TypedDict):
    data: list[CommunitySearchResult]
    pagination: Pagination


class SpaceResponse(TypedDict):
    data: Space


class SpaceStreamResponse(TypedDict):
    data: SpaceStreamInfo


class NotificationPaginatedResponse(TypedDict):
    data: list[Notification]
    pagination: Pagination


class LoginApiResponse(TypedDict):
    data: LoginResponse
