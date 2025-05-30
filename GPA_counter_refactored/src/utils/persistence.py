#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据持久化模块
负责保存和加载历史记录
"""

import os
import json
import logging
import datetime
import sys
import tempfile
from typing import List, Dict, Any, Optional, Union

# 配置日志
logger = logging.getLogger(__name__)

class DataPersistence:
    """
    数据持久化类
    负责将计算结果保存为JSON文件，并加载历史记录
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        """
        初始化数据持久化类
        
        Args:
            storage_dir: 存储目录，默认为程序所在目录下的data目录
            
        Raises:
            PermissionError: 如果无法创建存储目录
        """
        if storage_dir is None:
            # 获取应用程序的基础路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的可执行文件
                base_dir = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            self.storage_dir = os.path.join(base_dir, 'data')
            
            # 如果无法在应用程序目录创建data目录，则使用临时目录
            if not os.access(base_dir, os.W_OK):
                temp_dir = os.path.join(tempfile.gettempdir(), 'CUPB_GPA_Calculator')
                self.storage_dir = os.path.join(temp_dir, 'data')
                logger.warning(f"无法在应用程序目录创建data目录，将使用临时目录: {self.storage_dir}")
        else:
            # 检查参数类型
            if not isinstance(storage_dir, str):
                raise TypeError("存储目录路径必须是字符串类型")
            self.storage_dir = storage_dir
            
        # 确保存储目录存在
        try:
            if not os.path.exists(self.storage_dir):
                os.makedirs(self.storage_dir)
                logger.info(f"已创建存储目录: {self.storage_dir}")
        except PermissionError as e:
            # 如果无法创建存储目录，则使用临时目录
            temp_dir = os.path.join(tempfile.gettempdir(), 'CUPB_GPA_Calculator', 'data')
            logger.warning(f"无法创建存储目录，将使用临时目录: {temp_dir}")
            
            try:
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                self.storage_dir = temp_dir
                logger.info(f"已创建临时存储目录: {self.storage_dir}")
            except Exception as e2:
                logger.error(f"无法创建临时存储目录: {str(e2)}")
                raise PermissionError(f"无法创建存储目录: {str(e)}")
        except Exception as e:
            logger.error(f"创建存储目录时出错: {str(e)}")
            raise
            
        # 历史记录文件路径
        self.history_file = os.path.join(self.storage_dir, 'history.json')
        logger.info(f"历史记录将保存在: {self.history_file}")
    
    def save_record(self, record_data: Dict[str, Any]) -> bool:
        """
        保存一条计算记录
        
        Args:
            record_data: 记录数据，包含课程信息和计算结果
            
        Returns:
            bool: 保存成功返回True，否则返回False
            
        Raises:
            TypeError: 如果record_data不是字典类型
            ValueError: 如果record_data缺少必要的键
        """
        # 检查参数类型
        if not isinstance(record_data, dict):
            raise TypeError("记录数据必须是字典类型")
        
        # 检查必要字段
        required_keys = ['course_names', 'course_grades', 'course_credits', 'course_count']
        missing_keys = [key for key in required_keys if key not in record_data]
        if missing_keys:
            raise ValueError(f"记录数据缺少必要的键: {', '.join(missing_keys)}")
        
        try:
            # 添加时间戳
            record_data['timestamp'] = datetime.datetime.now().isoformat()
            
            # 处理数据，确保可以被JSON序列化
            self._prepare_record_for_json(record_data)
            
            # 读取现有历史记录
            history = self.load_history()
            
            # 添加新记录
            history.append(record_data)
            
            # 保存到文件
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
            logger.info(f"成功保存记录，当前共有{len(history)}条历史记录")
            return True
        except PermissionError as e:
            logger.error(f"保存记录失败，无权限写入文件: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"保存记录失败: {str(e)}")
            return False
    
    def _prepare_record_for_json(self, record: Dict[str, Any]) -> None:
        """
        处理记录数据，确保可以被JSON序列化
        
        Args:
            record: 需要处理的记录数据
        """
        # 确保所有值都可以被JSON序列化
        for key, value in record.items():
            if isinstance(value, list):
                # 处理列表中的元素
                for i, item in enumerate(value):
                    if isinstance(item, (datetime.date, datetime.datetime)):
                        value[i] = item.isoformat()
                    elif isinstance(item, complex):
                        value[i] = str(item)
                    elif not isinstance(item, (str, int, float, bool, type(None))):
                        value[i] = str(item)
            elif isinstance(value, (datetime.date, datetime.datetime)):
                record[key] = value.isoformat()
            elif isinstance(value, complex):
                record[key] = str(value)
            elif not isinstance(value, (str, int, float, bool, type(None), dict, list)):
                record[key] = str(value)
    
    def load_history(self) -> List[Dict[str, Any]]:
        """
        加载历史记录
        
        Returns:
            List[Dict[str, Any]]: 历史记录列表
        """
        if not os.path.exists(self.history_file):
            logger.info(f"历史记录文件不存在，将返回空列表")
            return []
            
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                logger.info(f"成功加载{len(history)}条历史记录")
                return history
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON文件失败: {str(e)}")
            return []
        except PermissionError as e:
            logger.error(f"无权限读取历史记录文件: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
            return []
    
    def get_record_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        根据索引获取历史记录
        
        Args:
            index: 记录索引
            
        Returns:
            Dict[str, Any] or None: 记录数据，如果不存在则返回None
            
        Raises:
            TypeError: 如果index不是整数类型
        """
        # 检查参数类型
        if not isinstance(index, int):
            raise TypeError("索引必须是整数类型")
        
        history = self.load_history()
        
        if 0 <= index < len(history):
            return history[index]
        else:
            logger.warning(f"请求的索引 {index} 超出范围 [0, {len(history)-1 if history else -1}]")
            return None
    
    def delete_record(self, index: int) -> bool:
        """
        删除指定索引的历史记录
        
        Args:
            index: 记录索引
            
        Returns:
            bool: 删除成功返回True，否则返回False
            
        Raises:
            TypeError: 如果index不是整数类型
        """
        # 检查参数类型
        if not isinstance(index, int):
            raise TypeError("索引必须是整数类型")
        
        try:
            history = self.load_history()
            
            if not history:
                logger.warning("没有历史记录可删除")
                return False
            
            if 0 <= index < len(history):
                del history[index]
                
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                    
                logger.info(f"成功删除索引为 {index} 的记录，当前共有 {len(history)} 条记录")
                return True
            else:
                logger.warning(f"删除失败：索引 {index} 超出范围 [0, {len(history)-1}]")
                return False
        except PermissionError as e:
            logger.error(f"删除记录失败，无权限写入文件: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"删除记录失败: {str(e)}")
            return False
    
    def clear_history(self) -> bool:
        """
        清空历史记录
        
        Returns:
            bool: 清空成功返回True，否则返回False
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            logger.info("已清空所有历史记录")
            return True
        except PermissionError as e:
            logger.error(f"清空历史记录失败，无权限写入文件: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"清空历史记录失败: {str(e)}")
            return False 