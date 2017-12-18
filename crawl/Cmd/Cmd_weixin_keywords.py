# -*- coding: utf-8 -*-
import sys, logging
reload(sys)
sys.setdefaultencoding('utf-8')
from crawl.Common.Util import session_scope
from crawl.Common.RobitUtil import RobitUtil
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, func
from crawl.models.util import db_connect, create_news_table
from crawl.models.crawl_weixin_article_detail import CrawlWeixinArticleDetail
from crawl.models.crawl_weixin_search import Crawl_Weixin_Search
from crawl.models.crawl_keywords_map import Crawl_keywords_map

class CmdWeixinKeywords:
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.util = RobitUtil()

    def start(self):
        self.readbody()
        self.readinfo()

    def readbody(self):
        logging.info("This is test log")
        with session_scope(self.sess) as session:
            query = session.query(CrawlWeixinArticleDetail.id, CrawlWeixinArticleDetail.body).filter(
                CrawlWeixinArticleDetail.key_state == 0
            ).limit(200).all()

            handled_body = []
            key_map = {}

            for i in query:
                try:
                    handled_body.append(i[0])
                    keywords = self.util.keywords_analyse(i[1], topK=5, strip_tag=True)
                    key_map[i[0]] = keywords
                    for key in keywords:
                        print key
                except Exception, e:
                    logging.error(e)

            if len(handled_body) > 0:
                session.query(CrawlWeixinArticleDetail).filter(
                    CrawlWeixinArticleDetail.id.in_(handled_body)
                ).update({"key_state": 1}, synchronize_session=False)

                all_keywords_map = []
                for id in key_map:
                    for word in key_map[id]:
                        model = Crawl_keywords_map()
                        model.s_id = id
                        model.keyword = word
                        model.tb = Crawl_Weixin_Search.__tablename__

                        qu = session.query(Crawl_keywords_map).filter(
                            and_(
                                Crawl_keywords_map.s_id == id,
                                Crawl_keywords_map.keyword == word
                            )
                        ).one_or_none()

                        if not qu:
                            all_keywords_map.append(model)

                if len(all_keywords_map) > 0:
                    session.add_all(all_keywords_map)

    def readinfo(self):
        with session_scope(self.sess) as session:
            query = session.query(Crawl_Weixin_Search.id, Crawl_Weixin_Search.title).filter(
                Crawl_Weixin_Search.key_state == 0
            ).limit(200).all()

            handled_title = []
            key_map = {}

            for i in query:
                try:
                    handled_title.append(i[0])
                    keywords = self.util.keywords_analyse(i[1], topK=5)
                    key_map[i[0]] = keywords
                    for key in keywords:
                        print key
                except Exception, e:
                    logging.error(e)

            if len(handled_title) > 0:
                session.query(Crawl_Weixin_Search).filter(
                    Crawl_Weixin_Search.id.in_(handled_title)
                ).update({"key_state": 1}, synchronize_session=False)

                all_keywords_map = []
                for id in key_map:
                    for word in key_map[id]:
                        model = Crawl_keywords_map()
                        model.s_id = id
                        model.keyword = word
                        model.tb = Crawl_Weixin_Search.__tablename__

                        qu = session.query(Crawl_keywords_map).filter(
                            and_(
                                Crawl_keywords_map.s_id == id,
                                Crawl_keywords_map.keyword == word
                            )
                        ).one_or_none()

                        if not qu:
                            all_keywords_map.append(model)

                if len(all_keywords_map) > 0:
                    session.add_all(all_keywords_map)

