#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图形用户界面模块
使用PyQt5创建现代化、简洁的界面
"""

import os
import sys
import datetime
import logging
from typing import List, Dict, Any, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QHeaderView, QSplitter, QFrame,
    QStatusBar, QAction, QMenu, QToolBar, QDialog, QDialogButtonBox,
    QTextEdit, QGroupBox, QFormLayout, QComboBox
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize

from ..utils.calculator import GpaCalculator
from ..utils.data_loader import DataLoader
from ..utils.persistence import DataPersistence
from ..utils.config import VERSION

# 获取日志记录器
logger = logging.getLogger(__name__)

class GUIApplication:
    """
    GUI应用程序类
    负责创建和管理图形用户界面
    """
    
    def __init__(self, calculator, data_loader, data_persistence):
        """
        初始化GUI应用程序
        
        Args:
            calculator: GPA计算器实例
            data_loader: 数据加载器实例
            data_persistence: 数据持久化实例
        """
        logger.info("初始化GUI应用程序")
        self.calculator = calculator
        self.data_loader = data_loader
        self.data_persistence = data_persistence
        self.initial_file = None
        
    def set_initial_file(self, file_path):
        """
        设置初始文件路径
        
        Args:
            file_path: 文件路径
        """
        logger.info(f"设置初始文件: {file_path}")
        self.initial_file = file_path
        
    def run(self):
        """
        运行GUI应用程序
        """
        logger.info("启动GUI应用程序")
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle("Fusion")
        
        # 创建主窗口
        main_window = MainWindow(self.calculator, self.data_loader, self.data_persistence)
        
        # 如果指定了初始文件，则加载它
        if self.initial_file:
            main_window.load_file(self.initial_file)
        
        # 显示主窗口
        main_window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, calculator, data_loader, persistence):
        """
        初始化主窗口
        
        Args:
            calculator: GPA计算器实例
            data_loader: 数据加载器实例
            persistence: 数据持久化实例
        """
        super().__init__()
        
        # 使用传入的实例
        self.calculator = calculator
        self.data_loader = data_loader
        self.persistence = persistence
        
        # 当前加载的课程数据
        self.course_count = 0
        self.course_names = []
        self.course_grades = []
        self.course_credits = []
        
        # 设置窗口属性
        self.setWindowTitle(f"CUPB绩点计算器 {VERSION}")
        self.setMinimumSize(800, 600)
        
        # 创建UI组件
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_widget()
        
        # 加载历史记录
        self._load_history()
        
        # 显示欢迎信息
        self.statusBar().showMessage("欢迎使用CUPB绩点计算器")
        logger.info("主窗口初始化完成")
    
    def load_file(self, file_path):
        """
        加载指定的文件
        
        Args:
            file_path: 文件路径
        """
        logger.info(f"加载文件: {file_path}")
        try:
            # 更新文件路径标签
            self.file_path_label.setText(file_path)
            
            # 加载数据
            self.course_count, self.course_names, self.course_grades, self.course_credits = (
                self.data_loader.load_from_excel(file_path)
            )
            
            # 更新课程表格
            self._update_course_table()
            
            # 启用计算按钮
            self.calculate_button.setEnabled(True)
            
            # 显示状态信息
            self.statusBar().showMessage(f"成功加载 {self.course_count} 门课程")
            logger.info(f"成功加载 {self.course_count} 门课程")
            
        except Exception as e:
            # 显示错误信息
            QMessageBox.critical(self, "错误", f"加载文件失败: {str(e)}")
            logger.error(f"加载文件失败: {str(e)}")
    
    def _create_actions(self):
        """创建动作"""
        # 文件菜单动作
        self.open_action = QAction("打开Excel文件", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self._open_file)
        
        self.save_action = QAction("保存记录", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self._save_record)
        self.save_action.setEnabled(False)  # 初始时禁用
        
        self.exit_action = QAction("退出", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
        # 历史记录菜单动作
        self.clear_history_action = QAction("清空历史记录", self)
        self.clear_history_action.triggered.connect(self._clear_history)
        
        # 帮助菜单动作
        self.about_action = QAction("关于", self)
        self.about_action.triggered.connect(self._show_about)
    
    def _create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # 历史记录菜单
        history_menu = menu_bar.addMenu("历史记录")
        history_menu.addAction(self.clear_history_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction(self.about_action)
    
    def _create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(16, 16))
        self.addToolBar(tool_bar)
        
        tool_bar.addAction(self.open_action)
        tool_bar.addAction(self.save_action)
        tool_bar.addSeparator()
        tool_bar.addAction(self.exit_action)
    
    def _create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
    
    def _create_central_widget(self):
        """创建中央部件"""
        # 创建选项卡部件
        self.tabs = QTabWidget()
        
        # 创建"导入数据"选项卡
        self.import_tab = QWidget()
        self.tabs.addTab(self.import_tab, "导入数据")
        self._setup_import_tab()
        
        # 创建"计算结果"选项卡
        self.result_tab = QWidget()
        self.tabs.addTab(self.result_tab, "计算结果")
        self._setup_result_tab()
        
        # 创建"历史记录"选项卡
        self.history_tab = QWidget()
        self.tabs.addTab(self.history_tab, "历史记录")
        self._setup_history_tab()
        
        # 设置中央部件
        self.setCentralWidget(self.tabs)
    
    def _setup_import_tab(self):
        """设置导入数据选项卡"""
        layout = QVBoxLayout()
        
        # 文件选择部分
        file_group = QGroupBox("选择Excel文件")
        file_layout = QHBoxLayout()
        
        self.file_path_label = QLabel("未选择文件")
        self.file_path_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border-radius: 3px;")
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self._open_file)
        
        file_layout.addWidget(self.file_path_label, 1)
        file_layout.addWidget(self.browse_button, 0)
        
        file_group.setLayout(file_layout)
        
        # 课程数据表格
        self.course_table = QTableWidget(0, 3)
        self.course_table.setHorizontalHeaderLabels(["课程名称", "成绩", "学分"])
        self.course_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.course_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.course_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # 按钮部分
        button_layout = QHBoxLayout()
        
        self.calculate_button = QPushButton("计算绩点")
        self.calculate_button.setEnabled(False)
        self.calculate_button.clicked.connect(self._calculate_gpa)
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.calculate_button)
        
        # 添加到主布局
        layout.addWidget(file_group)
        layout.addWidget(QLabel("课程数据:"))
        layout.addWidget(self.course_table)
        layout.addLayout(button_layout)
        
        self.import_tab.setLayout(layout)
    
    def _setup_result_tab(self):
        """设置计算结果选项卡"""
        layout = QVBoxLayout()
        
        # 结果摘要部分
        summary_group = QGroupBox("计算结果摘要")
        summary_layout = QFormLayout()
        
        self.avg_score_label = QLabel("--")
        self.avg_score_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.overall_gpa_label = QLabel("--")
        self.overall_gpa_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1a73e8;")
        
        summary_layout.addRow("平均学分绩:", self.avg_score_label)
        summary_layout.addRow("平均学分绩点(GPA):", self.overall_gpa_label)
        
        summary_group.setLayout(summary_layout)
        
        # 课程绩点表格
        self.gpa_table = QTableWidget(0, 3)
        self.gpa_table.setHorizontalHeaderLabels(["课程名称", "成绩", "绩点"])
        self.gpa_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.gpa_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.gpa_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # 按钮部分
        button_layout = QHBoxLayout()
        
        self.save_result_button = QPushButton("保存结果")
        self.save_result_button.setEnabled(False)
        self.save_result_button.clicked.connect(self._save_record)
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.save_result_button)
        
        # 添加到主布局
        layout.addWidget(summary_group)
        layout.addWidget(QLabel("各课程绩点:"))
        layout.addWidget(self.gpa_table)
        layout.addLayout(button_layout)
        
        self.result_tab.setLayout(layout)
    
    def _setup_history_tab(self):
        """设置历史记录选项卡"""
        layout = QVBoxLayout()
        
        # 历史记录表格
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["时间", "课程数量", "平均学分绩", "GPA"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.itemDoubleClicked.connect(self._show_history_detail)
        
        # 按钮部分
        button_layout = QHBoxLayout()
        
        self.delete_record_button = QPushButton("删除所选记录")
        self.delete_record_button.clicked.connect(lambda: self._delete_record(self.history_table.currentRow()))
        
        self.clear_all_button = QPushButton("清空所有记录")
        self.clear_all_button.clicked.connect(self._clear_history)
        
        button_layout.addWidget(self.delete_record_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.clear_all_button)
        
        # 添加到主布局
        layout.addWidget(QLabel("历史记录:"))
        layout.addWidget(self.history_table)
        layout.addLayout(button_layout)
        
        self.history_tab.setLayout(layout)
    
    def _open_file(self):
        """打开Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            "",
            "Excel文件 (*.xlsx *.xls)"
        )
        
        if file_path:
            self.load_file(file_path)
    
    def _update_course_table(self):
        """更新课程表格"""
        logger.info("更新课程表格")
        # 清空表格
        self.course_table.setRowCount(0)
        
        # 添加课程数据
        for i in range(self.course_count):
            row_position = self.course_table.rowCount()
            self.course_table.insertRow(row_position)
            
            self.course_table.setItem(row_position, 0, QTableWidgetItem(str(self.course_names[i])))
            self.course_table.setItem(row_position, 1, QTableWidgetItem(str(self.course_grades[i])))
            self.course_table.setItem(row_position, 2, QTableWidgetItem(str(self.course_credits[i])))
    
    def _calculate_gpa(self):
        """计算GPA"""
        logger.info("开始计算GPA")
        try:
            # 加载数据到计算器
            self.calculator.load_data(self.course_names, self.course_grades, self.course_credits)
            
            # 计算平均学分绩
            avg_score = self.calculator.calculate_average_score()
            self.avg_score_label.setText(f"{avg_score:.2f}")
            
            # 计算课程绩点
            course_gpas = self.calculator.calculate_course_gpa()
            self._update_gpa_table(course_gpas)
            
            # 计算平均学分绩点
            overall_gpa = self.calculator.calculate_overall_gpa()
            self.overall_gpa_label.setText(f"{overall_gpa}")
            
            # 启用保存按钮
            self.save_action.setEnabled(True)
            self.save_result_button.setEnabled(True)
            
            # 切换到结果选项卡
            self.tabs.setCurrentWidget(self.result_tab)
            
            # 显示状态信息
            self.statusBar().showMessage("GPA计算完成")
            logger.info(f"GPA计算完成: 平均学分绩={avg_score:.2f}, GPA={overall_gpa}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"计算GPA失败: {str(e)}")
            logger.error(f"计算GPA失败: {str(e)}")
    
    def _update_gpa_table(self, course_gpas):
        """更新绩点表格"""
        logger.info("更新绩点表格")
        # 清空表格
        self.gpa_table.setRowCount(0)
        
        # 添加课程数据
        for i in range(self.course_count):
            row_position = self.gpa_table.rowCount()
            self.gpa_table.insertRow(row_position)
            
            self.gpa_table.setItem(row_position, 0, QTableWidgetItem(str(self.course_names[i])))
            self.gpa_table.setItem(row_position, 1, QTableWidgetItem(str(self.course_grades[i])))
            self.gpa_table.setItem(row_position, 2, QTableWidgetItem(str(course_gpas[i])))
    
    def _save_record(self):
        """保存记录"""
        logger.info("保存记录")
        try:
            # 创建记录数据
            record = {
                "course_names": self.course_names,
                "course_grades": [float(grade) for grade in self.course_grades],
                "course_credits": [float(credit) for credit in self.course_credits],
                "course_count": self.course_count,
                "avg_score": float(self.avg_score_label.text()),
                "overall_gpa": float(self.overall_gpa_label.text())
            }
            
            # 保存记录
            if self.persistence.save_record(record):
                # 刷新历史记录
                self._load_history()
                
                # 显示状态信息
                self.statusBar().showMessage("记录已保存")
                logger.info("记录已保存")
                
                # 切换到历史记录选项卡
                self.tabs.setCurrentWidget(self.history_tab)
            else:
                QMessageBox.warning(self, "警告", "保存记录失败")
                logger.warning("保存记录失败")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存记录失败: {str(e)}")
            logger.error(f"保存记录失败: {str(e)}")
    
    def _load_history(self):
        """加载历史记录"""
        logger.info("加载历史记录")
        try:
            # 获取历史记录
            history = self.persistence.load_history()
            
            # 清空表格
            self.history_table.setRowCount(0)
            
            # 添加历史记录
            for i, record in enumerate(history):
                row_position = self.history_table.rowCount()
                self.history_table.insertRow(row_position)
                
                # 格式化时间戳
                timestamp = datetime.datetime.fromisoformat(record["timestamp"]).strftime("%Y-%m-%d %H:%M")
                
                self.history_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
                self.history_table.setItem(row_position, 1, QTableWidgetItem(str(record["course_count"])))
                self.history_table.setItem(row_position, 2, QTableWidgetItem(f"{record['avg_score']:.2f}"))
                self.history_table.setItem(row_position, 3, QTableWidgetItem(str(record["overall_gpa"])))
            
            logger.info(f"加载了{len(history)}条历史记录")
            
        except Exception as e:
            QMessageBox.warning(self, "警告", f"加载历史记录失败: {str(e)}")
            logger.error(f"加载历史记录失败: {str(e)}")
    
    def _show_history_detail(self, item):
        """显示历史记录详情"""
        # 获取选中的行
        row = item.row()
        
        try:
            # 获取记录
            record = self.persistence.get_record_by_index(row)
            
            if not record:
                return
            
            # 创建详情对话框
            dialog = QDialog(self)
            dialog.setWindowTitle("历史记录详情")
            dialog.setMinimumSize(500, 400)
            
            # 创建布局
            layout = QVBoxLayout()
            
            # 创建表格
            table = QTableWidget(len(record["course_names"]), 3)
            table.setHorizontalHeaderLabels(["课程名称", "成绩", "学分"])
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            
            # 添加课程数据
            for i in range(len(record["course_names"])):
                table.setItem(i, 0, QTableWidgetItem(str(record["course_names"][i])))
                table.setItem(i, 1, QTableWidgetItem(str(record["course_grades"][i])))
                table.setItem(i, 2, QTableWidgetItem(str(record["course_credits"][i])))
            
            # 创建结果显示
            result_layout = QFormLayout()
            avg_score_label = QLabel(f"{record['avg_score']:.2f}")
            overall_gpa_label = QLabel(str(record["overall_gpa"]))
            
            result_layout.addRow("平均学分绩:", avg_score_label)
            result_layout.addRow("平均学分绩点(GPA):", overall_gpa_label)
            
            result_group = QGroupBox("计算结果")
            result_group.setLayout(result_layout)
            
            # 创建按钮
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            
            # 添加删除按钮
            delete_button = QPushButton("删除此记录")
            delete_button.clicked.connect(lambda: self._delete_record(row, dialog))
            button_box.addButton(delete_button, QDialogButtonBox.ActionRole)
            
            # 添加组件到布局
            layout.addWidget(result_group)
            layout.addWidget(QLabel("课程数据:"))
            layout.addWidget(table)
            layout.addWidget(button_box)
            
            # 设置布局
            dialog.setLayout(layout)
            
            # 显示对话框
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"显示历史记录详情失败: {str(e)}")
            logger.error(f"显示历史记录详情失败: {str(e)}")
    
    def _delete_record(self, index, dialog=None):
        """删除记录"""
        logger.info(f"删除记录: 索引={index}")
        try:
            # 确认删除
            reply = QMessageBox.question(
                self,
                "确认删除",
                "确定要删除这条记录吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 删除记录
                if self.persistence.delete_record(index):
                    # 刷新历史记录
                    self._load_history()
                    
                    # 显示状态信息
                    self.statusBar().showMessage("记录已删除")
                    logger.info("记录已删除")
                    
                    # 关闭对话框
                    if dialog:
                        dialog.accept()
                else:
                    QMessageBox.warning(self, "警告", "删除记录失败")
                    logger.warning("删除记录失败")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除记录失败: {str(e)}")
            logger.error(f"删除记录失败: {str(e)}")
    
    def _clear_history(self):
        """清空历史记录"""
        logger.info("清空历史记录")
        try:
            # 确认清空
            reply = QMessageBox.question(
                self,
                "确认清空",
                "确定要清空所有历史记录吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 清空历史记录
                if self.persistence.clear_history():
                    # 刷新历史记录
                    self._load_history()
                    
                    # 显示状态信息
                    self.statusBar().showMessage("历史记录已清空")
                    logger.info("历史记录已清空")
                else:
                    QMessageBox.warning(self, "警告", "清空历史记录失败")
                    logger.warning("清空历史记录失败")
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"清空历史记录失败: {str(e)}")
            logger.error(f"清空历史记录失败: {str(e)}")
    
    def _show_about(self):
        """显示关于对话框"""
        about_text = f"""
        <h2>CUPB绩点计算器 {VERSION}</h2>
        <p>适用于中国石油大学(北京)的GPA计算工具</p>
        <p>支持从Excel表格导入课程数据，计算平均学分绩、课程绩点和平均学分绩点。</p>
        <p>© 2023-2025 All Rights Reserved</p>
        """
        
        QMessageBox.about(self, "关于", about_text) 