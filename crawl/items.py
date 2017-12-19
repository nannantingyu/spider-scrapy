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

class ChinaTimeItem(scrapy.Item):
    """中国平均时间"""
    value = scrapy.Field()
    type = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class ErrorTopItem(scrapy.Item):
    """故障统计"""
    monitor_name = scrapy.Field()
    type = scrapy.Field()
    value = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class MonitorAreaStasticItem(scrapy.Item):
    """监控地区统计"""
    monitor_name = scrapy.Field()
    type = scrapy.Field()
    province = scrapy.Field()
    area = scrapy.Field()
    mid = scrapy.Field()
    site = scrapy.Field()
    day = scrapy.Field()

class MonitorChartItem(scrapy.Item):
    """监控图表数据"""
    monitor_name = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    value = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class MonitorProvinceItem(scrapy.Item):
    """监控省份统计"""
    monitor_name = scrapy.Field()
    monitor_province = scrapy.Field()
    value = scrapy.Field()
    type = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class MonitorStasticItem(scrapy.Item):
    """监控统计"""
    mid = scrapy.Field()
    day = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    avg = scrapy.Field()
    time_st = scrapy.Field()
    all_time = scrapy.Field()
    site = scrapy.Field()

class MonitorTypeItem(scrapy.Item):
    """监控类型统计"""
    monitor_name = scrapy.Field()
    province = scrapy.Field()
    rate = scrapy.Field()
    catname = scrapy.Field()
    type_name = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class ProvinceTimeItem(scrapy.Item):
    """监控省份响应时间"""
    province_name = scrapy.Field()
    value = scrapy.Field()
    type = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class TypeTimeItem(scrapy.Item):
    """监控运营商响应时间"""
    type_name = scrapy.Field()
    value = scrapy.Field()
    type = scrapy.Field()
    day = scrapy.Field()
    site = scrapy.Field()

class BaiduTongjiItem(scrapy.Item):
    """百度统计"""
    access_time = scrapy.Field()
    area = scrapy.Field()
    keywords = scrapy.Field()
    entry_page = scrapy.Field()
    ip = scrapy.Field()
    user_id = scrapy.Field()
    visit_time = scrapy.Field()
    visit_pages = scrapy.Field()
    visitorType = scrapy.Field()
    visitorFrequency = scrapy.Field()
    lastVisitTime = scrapy.Field()
    endPage = scrapy.Field()
    deviceType = scrapy.Field()
    fromType = scrapy.Field()
    fromurl = scrapy.Field()
    fromAccount = scrapy.Field()
    isp = scrapy.Field()
    os = scrapy.Field()
    osType = scrapy.Field()
    browser = scrapy.Field()
    browserType = scrapy.Field()
    language = scrapy.Field()
    resolution = scrapy.Field()
    color = scrapy.Field()
    accessPage = scrapy.Field()
    antiCode = scrapy.Field()
    site = scrapy.Field()

class CrawlEconomicCalendarItem(scrapy.Item):
    """金10财经日历"""
    country = scrapy.Field()
    quota_name = scrapy.Field()
    pub_time = scrapy.Field()
    importance = scrapy.Field()
    former_value = scrapy.Field()
    predicted_value = scrapy.Field()
    published_value = scrapy.Field()
    influence = scrapy.Field()
    source_id = scrapy.Field()
    dataname = scrapy.Field()
    datename = scrapy.Field()
    dataname_id = scrapy.Field()
    unit = scrapy.Field()

class CrawlEconomicEventItem(scrapy.Item):
    """金10财经事件"""
    time = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    importance = scrapy.Field()
    event = scrapy.Field()
    date = scrapy.Field()
    source_id = scrapy.Field()

class CrawlEconomicHolidayItem(scrapy.Item):
    """金10财经假期"""
    time = scrapy.Field()
    country = scrapy.Field()
    market = scrapy.Field()
    holiday_name = scrapy.Field()
    detail = scrapy.Field()
    date = scrapy.Field()
    source_id = scrapy.Field()

class ZhanzhangItem(scrapy.Item):
    """站长之家seo"""
    keywords = scrapy.Field()
    total_index = scrapy.Field()
    pc_index = scrapy.Field()
    mobile_index = scrapy.Field()
    baidu_index = scrapy.Field()
    shoulu_count = scrapy.Field()
    shoulu_page = scrapy.Field()
    shoulu_title = scrapy.Field()
    site = scrapy.Field()

class IbrebatesItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    spread_type = scrapy.Field()
    om_spread = scrapy.Field()
    gold_spread = scrapy.Field()
    offshore = scrapy.Field()
    a_share = scrapy.Field()
    regulatory_authority = scrapy.Field()
    trading_varieties = scrapy.Field()
    platform_type = scrapy.Field()
    account_type = scrapy.Field()
    scalp = scrapy.Field()
    hedging = scrapy.Field()
    min_transaction = scrapy.Field()
    least_entry = scrapy.Field()
    maximum_leverage = scrapy.Field()
    maximum_trading = scrapy.Field()
    deposit_method = scrapy.Field()
    entry_method = scrapy.Field()
    commission_fee = scrapy.Field()
    entry_fee = scrapy.Field()
    account_currency = scrapy.Field()
    rollovers = scrapy.Field()
    explosion_proportion = scrapy.Field()
    renminbi = scrapy.Field()

class SsiTrendsItem(scrapy.Item):
    time = scrapy.Field()
    platform = scrapy.Field()
    type = scrapy.Field()
    long_position = scrapy.Field()

class CrawlEconomicJieduItem(scrapy.Item):
    next_pub_time = scrapy.Field()
    pub_agent = scrapy.Field()
    pub_frequency = scrapy.Field()
    count_way = scrapy.Field()
    data_influence = scrapy.Field()
    data_define = scrapy.Field()
    funny_read = scrapy.Field()
    dataname_id = scrapy.Field()

class CrawlFx678EconomicCalendarItem(scrapy.Item):
    """Fx678财经日历"""
    country = scrapy.Field()
    quota_name = scrapy.Field()
    pub_time = scrapy.Field()
    importance = scrapy.Field()
    former_value = scrapy.Field()
    predicted_value = scrapy.Field()
    published_value = scrapy.Field()
    influence = scrapy.Field()
    source_id = scrapy.Field()
    next_pub_time = scrapy.Field()
    pub_agent = scrapy.Field()
    pub_frequency = scrapy.Field()
    count_way = scrapy.Field()
    data_influence = scrapy.Field()
    data_define = scrapy.Field()
    funny_read = scrapy.Field()
    dataname = scrapy.Field()
    datename = scrapy.Field()
    position = scrapy.Field()
    dataname_id = scrapy.Field()
    unit = scrapy.Field()

class CrawlCgseItem(scrapy.Item):
    """Cgse"""
    no = scrapy.Field()
    name = scrapy.Field()
    idr = scrapy.Field()
    executive_manager = scrapy.Field()
    executive_manager_ex = scrapy.Field()
    register_number = scrapy.Field()
    company_number = scrapy.Field()
    business_status = scrapy.Field()
    registe_address = scrapy.Field()
    website = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()

class CrawlBaiduRateItem(scrapy.Item):
    show_count = scrapy.Field()
    clk_count = scrapy.Field()
    cost_count = scrapy.Field()
    ctr = scrapy.Field()
    cpm = scrapy.Field()
    pv_count = scrapy.Field()
    visit_count = scrapy.Field()
    visitor_count = scrapy.Field()
    new_visitor_count = scrapy.Field()
    new_visitor_ratio = scrapy.Field()
    in_visit_count = scrapy.Field()
    bounce_ratio = scrapy.Field()
    avg_visit_time = scrapy.Field()
    avg_visit_pages = scrapy.Field()
    arrival_ratio = scrapy.Field()
    trans_count = scrapy.Field()
    trans_ratio = scrapy.Field()
    avg_trans_cost = scrapy.Field()
    income = scrapy.Field()
    profit = scrapy.Field()
    roi = scrapy.Field()
    ctime = scrapy.Field()
    site = scrapy.Field()
    source_id = scrapy.Field()

class CrawlWexinArticleItem(scrapy.Item):
    title = scrapy.Field()
    source_url = scrapy.Field()
    source_id = scrapy.Field()
    type = scrapy.Field()
    publish_time = scrapy.Field()
    author = scrapy.Field()
    favor = scrapy.Field()
    disfavor = scrapy.Field()
    image = scrapy.Field()
    state = scrapy.Field()
    hits = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()

class CrawlArticleDetailItem(scrapy.Item):
    source_id = scrapy.Field()
    body = scrapy.Field()
    keywords = scrapy.Field()

class CrawlHotkey(scrapy.Item):
    time = scrapy.Field()
    keyword = scrapy.Field()
    order = scrapy.Field()
    source_id = scrapy.Field()

class CrawlWeibo(scrapy.Item):
    pub_time = scrapy.Field()
    content = scrapy.Field()
    author_name = scrapy.Field()
    author_link = scrapy.Field()
    author_img = scrapy.Field()
    source_id = scrapy.Field()
    images = scrapy.Field()