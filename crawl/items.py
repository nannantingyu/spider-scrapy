# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    type = scrapy.Field()
    keywords = scrapy.Field()
    source_id = scrapy.Field()
    source_url = scrapy.Field()
    source_site = scrapy.Field()

class LianjiaHouseItem(scrapy.Item):
    house_id = scrapy.Field()
    title = scrapy.Field()
    followed = scrapy.Field()
    residential = scrapy.Field()
    layout = scrapy.Field()
    area = scrapy.Field()
    img_desc = scrapy.Field()
    residential_id = scrapy.Field()
    direction = scrapy.Field()
    renovation = scrapy.Field()
    elevator = scrapy.Field()
    flood = scrapy.Field()
    related_name = scrapy.Field()
    related_href = scrapy.Field()
    visited = scrapy.Field()
    pub_time = scrapy.Field()
    tag = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()
    images = scrapy.Field()
    district = scrapy.Field()
    apartment_structure = scrapy.Field()
    street = scrapy.Field()
    address = scrapy.Field()
    building_type = scrapy.Field()
    ladder = scrapy.Field()
    heating = scrapy.Field()
    property_term = scrapy.Field()
    list_time = scrapy.Field()
    ownership = scrapy.Field()
    last_trade = scrapy.Field()
    purpose = scrapy.Field()
    hold_years = scrapy.Field()
    mortgage = scrapy.Field()
    house_register = scrapy.Field()
    core_point = scrapy.Field()
    periphery = scrapy.Field()
    traffic = scrapy.Field()
    residential_desc = scrapy.Field()
    layout_desc = scrapy.Field()
    img_layout = scrapy.Field()
    layout_datas = scrapy.Field()
    state = scrapy.Field()
    source_id = scrapy.Field()
    source_url = scrapy.Field()

class LianjiaResidentialItem(scrapy.Item):
    residential_id = scrapy.Field()
    name = scrapy.Field()
    build_year = scrapy.Field()
    build_num = scrapy.Field()
    build_type = scrapy.Field()
    unit_price = scrapy.Field()
    sell_num = scrapy.Field()
    rent_num = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()

class LianjiaAgentItem(scrapy.Item):
    name = scrapy.Field()
    agent_id = scrapy.Field()
    reason = scrapy.Field()
    agent_url = scrapy.Field()
    agent_level = scrapy.Field()
    agent_photo = scrapy.Field()
    feedback_good_rate = scrapy.Field()
    comment_count = scrapy.Field()
    total_comment_score = scrapy.Field()
    agent_phone = scrapy.Field()

class LianjiaFeedbackItem(scrapy.Item):
    house_id = scrapy.Field()
    comment = scrapy.Field()
    agent_id = scrapy.Field()

class LianjiaVisitedItem(scrapy.Item):
    house_id = scrapy.Field()
    visited_time = scrapy.Field()
    agent_id = scrapy.Field()
    see_count = scrapy.Field()