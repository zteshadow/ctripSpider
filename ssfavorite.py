#!/usr/bin/env python3
#-*- coding=utf8 -*-

#手动列出要查询的酒店和机票目的地

class ssfavorite:

  #返回喜欢的酒店列表
  @staticmethod
  def hotels():
    return ['长白山万达假日度假酒店', '长白山万达喜来登度假酒店', '青岛武胜关度假酒店', '上海和平饭店', '上海大厦', '北京天安瑞嘉酒店']

  #返回(酒店, 机票目的地, 人数)
  @staticmethod
  def travels():
    return [\
            #滑雪我和蛋蛋两人
            ('长白山万达假日度假酒店', '长白山', 2), \
            ('长白山万达喜来登度假酒店', '长白山', 2), \

            #带妈妈3人
            ('青岛武胜关度假酒店', '青岛', 3), \
            ('上海和平饭店', '上海' , 3), \
            ('上海大厦', '上海' , 3), \
            ('北京天安瑞嘉酒店', '北京', 3)\
            
            ]

  @staticmethod
  def home():
    return '上海'
