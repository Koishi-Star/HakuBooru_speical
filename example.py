import logging

from hakubooru.caption import KohakuCaptioner
from hakubooru.dataset import load_db, Post
from hakubooru.dataset.utils import (
    select_post_by_tags,
    select_post_by_required_tags,
    get_tag_by_name,
    get_all_posts,
)
from hakubooru.export import Exporter, FileSaver
from hakubooru.logging import logger
from hakubooru.source import TarSource

if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    logger.info("Loading danbooru2023.db")
    load_db("./data/danbooru2023.db")

    logger.info("Build exporter")
    exporter = Exporter(
        source=TarSource("./images"),
        saver=FileSaver("./out/example"),
        captioner=KohakuCaptioner(),
        process_batch_size=1000,
        process_threads=8,
    )

    logger.info("Querying posts")
    # Querying posts for:
    # * whose tag_list have all the following tags:
    #   * multiple_girls
    #   * 2girls
    #   * swimsuit
    # * whose tag_list have any of the following tags:
    #   * rice_shower_(umamusume)
    #   * mejiro_mcqueen_(umamusume)
    #   * daiwa_scarlet_(umamusume)
    #   * amiya_(arknights)
    #   * texas_(arknights)
    #   * skadi_(arknights)
    # * whose rating < 3 (avoid explicit images)
    # * whose score > 10 (better preference)

    # Use multiple tag as requirements
    # required_tags = [
    #     get_tag_by_name(tag) for tag in ["swimsuit", "multiple_girls", "2girls"]
    # ]
    #
    # target_characters = [
    #     get_tag_by_name(tag)
    #     for tag in [
    #         "rice_shower_(umamusume)",
    #         "mejiro_mcqueen_(umamusume)",
    #         "daiwa_scarlet_(umamusume)",
    #         "amiya_(arknights)",
    #         "texas_(arknights)",
    #         "skadi_(arknights)",
    #     ]
    # ]

    # choosed_post_characters = select_post_by_tags(target_characters)

    # .where(Post.id << ..., Post.rating<3, Post.fav_count >= 10)
    # .where(Post.rating<3, Post.fav_count >= 10)
    # 用于按照质量和涩情程度筛选post

    # choosed_post_required = select_post_by_required_tags(required_tags)
    # choosed_post = choosed_post_required.where(Post.id << choosed_post_characters)
    # limit_100_post = get_all_posts(5000)
    all_posts = get_all_posts(5000)

    # logger.info(f"Found {len(choosed_post_characters)} posts for characters")
    # logger.info(f"Found {len(choosed_post_required)} posts for required tags")
    # logger.info(f"Found {len(choosed_post)} posts")
    logger.info(f"Found {len(all_posts)} posts")

    # logger.info("Exporting images")
    exporter.export_posts(all_posts)
