import dateutil.parser

from hakubooru.dataset.db import (
    Post,
)
from hakubooru.metainfo import (
    rating_map,
    fav_count_percentile_full,
)
from datetime import datetime, timezone


def year_tag(
    post: Post, keep_tags: list[str], general_tags: list[str]
) -> tuple[list[str], list[str]]:
    year = 0
    try:
        date = dateutil.parser.parse(post.created_at)
        year = date.year
    except:
        pass
    if 2005 <= year <= 2010:
        year_tag = "old"
    elif year <= 2014:
        year_tag = "early"
    elif year <= 2017:
        year_tag = "mid"
    elif year <= 2020:
        year_tag = "recent"
    elif year <= 2024:
        year_tag = "newest"
    else:
        return keep_tags, general_tags
    general_tags.append(year_tag)
    return keep_tags, general_tags


def rating_tag(
    post: Post, keep_tags: list[str], general_tags: list[str]
) -> tuple[list[str], list[str]]:
    if (tag := rating_map.get(post.rating, None)) is not None:
        general_tags += tag
    return keep_tags, general_tags


def quality_tag(
    post: Post,
    keep_tags: list[str],
    general_tags: list[str],
    percentile_map: dict[str, dict[int, int]] = fav_count_percentile_full,
) -> tuple[list[str], list[str]]:
    # 为了能返回判断值，我们不再从这里截断函数
    if post.id < 5021000:
        # id=5021000为2022年1月1日最新一张图片
        score = post.fav_count
    rating = post.rating
    percentile = percentile_map[rating]

    year = 0
    start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    try:
        date = dateutil.parser.parse(post.created_at).replace(tzinfo=timezone.utc)
        year = date.year
        if year >= 2022:
            score = post.fav_count
            days_since_start = (date - start_date).total_seconds() / (24 * 60 * 60)
            score = (40 / (-0.034 * days_since_start + 48.3426)) * score
    except:
        pass

    if score > percentile[85]:
        quality_tag = "best quality"
    elif score > percentile[65]:
        quality_tag = "normal quality"
    elif score > percentile[35]:
        quality_tag = "low quality"
    else:
        quality_tag = "worst quality"

    general_tags.append(quality_tag)

    return keep_tags, general_tags


def quality_tag_new(
    post: Post,
    keep_tags: list[str],
    general_tags: list[str],
    percentile_map: dict[str, dict[int, int]] = fav_count_percentile_full,
) -> tuple[list[str], list[str]]:
    if post.id < 5021000:
        # Don't add quality tag for posts which are new.
        score = post.fav_count

    start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    rating = post.rating
    percentile = percentile_map[rating]

    try:
        date = dateutil.parser.parse(post.created_at).replace(tzinfo=timezone.utc)
        year = date.year
        if year >= 2022:
            score = post.fav_count
            days_since_start = (date - start_date).total_seconds() / (24 * 60 * 60)
            score = round((40 / (-0.034 * days_since_start + 48.3426)) * score, 1)
    except:
        pass

    if score > percentile[85]:
        quality_tag = "best quality"
    elif score > percentile[65]:
        quality_tag = "normal quality"
    elif score > percentile[35]:
        quality_tag = "low quality"
    else:
        quality_tag = "worst quality"
    general_tags.append(quality_tag)
    # general_tags.append(str(score))

    return keep_tags, general_tags
