import json
import os.path
import subprocess
import sys
import threading
from base64 import b64decode as b64
from json import JSONDecodeError

from PySide6 import QtGui
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut, QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from qdarktheme import load_stylesheet, setup_theme

import apsat_core.consts
from apsat_core.download import DownloadEngine
from apsat_core.get_profile import get_profile, resolve_textures
from apsat_core.types import NameList, ProfileList, ProfileType, TextureUrlList
from deswatts_tools.logutil import remove_logs, setup_logger

icon_data = "AAABAAEAICAAAAAAIAA6AgAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAgAAAAIAgGAAAAc3p69AAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L/GEFAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABz0lEQVRYR+2VPUsDQRCGFysRBJVEjWCwSBptBLWw8IOARVqtLIyKnRYBG7EUK7Ww1KBWmkbsLPwxCkJAsLC2zHkzNxNm9zYb73JnGl94CLe3O8+bbU79p1PmCsOeZGU664T3zeQHERoTP1IO2KQS3pdYgcJ4vwfIEkA7sflMY+Kn5wX4Km/2ysjzcQV5OT1A+PnxcBPhffPFEYTGxE/PC/BAFrDQFJvwORoTPz0vwAM560tniCnidQ6/pzHxw4M4UQtsv49N7TZG8ZdGRgsLeCCzvzqrYb7ncyBnaKQ7Xk15nUitQEtSd0B7jkoLGqXJAeSysoycbCwi0Qs8CFk7LCWSK2AT2vD3Nq9VS1wuDiEs5iLJF5A3RDfhQhbwC+dIZQ8ekrJO3FvWDGQBmN+sqW/ShRO5gMHXU59Xfctoa1oBWIMSt2pip5H93PrI5UkdpJsCIGeRLBEqcKe86mumtUbqIN3egJRxCbkGz7Au10gdpNsCgBxuypxySBIFAClpByn1JFUAsEkZ8JBST5IFAKsc3v1VASAkB5wFfvMtiIgmh/nOAincggY5SBkObkjhFhDXv+c0r9Qat0wDmE8qd/yPxrltQFz8L+EFjRZR6gfk2FIi3EGOXAAAAABJRU5ErkJggg=="


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(__name__)

        self.load_config()
        self.load_stylesheet()
        self.setup_widgets()
        self.setup_layout()
        self.init_window()

        self.show()
        self.logger.info(f"Created window, size:({self.width()}x{self.height()})")
        self.update_button_timer.start()


    def closeEvent(self, a0: QtGui.QCloseEvent | None) -> None:
        self.logger.info("Closed window")

        def delete_dir(dir_name):
            clear_list = os.listdir(dir_name)
            for i in clear_list:
                if os.path.isdir(os.path.join(dir_name, i)):
                    delete_dir(os.path.join(dir_name, i))
                else:
                    try:
                        os.remove(os.path.join(dir_name, i))
                    except FileNotFoundError:
                        pass

            os.removedirs(dir_name)

        self.logger.info("Clear templete files")

        delete_dir("tmp")

        self.logger.info("Save config")

        self.save_config()

        a0.accept()


    def init_window(self):
        self.logger.info("Init window")
        self.setWindowTitle("Apsat")
        self.resize(720, 380)
        window_icon = b64(icon_data)

        try:
            os.mkdir("tmp")
        except FileExistsError:
            pass
        with open("tmp/icon.ico", "wb+") as f:
            f.write(window_icon)
        window_icon = QIcon("tmp/icon.ico")
        self.setWindowIcon(window_icon)

        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        fullscreen_shortcut.activated.connect(lambda: self.showNormal() if self.isFullScreen() else self.showFullScreen())

        self.start_work = False


    def setup_layout(self):
        mid_right_layout = QVBoxLayout()
        mid_right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mid_right_layout.setSpacing(10)
        mid_right_layout.addWidget(self.select_profile_from)
        mid_right_layout.addWidget(self.uinput_url)
        mid_right_layout.addWidget(self.placeholder_1)
        mid_right_layout.addWidget(self.select_profile_type)
        mid_right_layout.addWidget(self.placeholder_2)
        mid_right_layout.addWidget(self.uinput_download)


        mid_right_out_layout = QVBoxLayout()
        mid_right_out_layout.addLayout(mid_right_layout)
        mid_right_out_layout.addWidget(self.confirm_buttom)


        mid_layout = QHBoxLayout()
        mid_layout.addWidget(self.uinput_edit)
        mid_layout.addLayout(mid_right_out_layout)


        layout = QVBoxLayout()
        layout.addWidget(self.get_start)
        layout.addLayout(mid_layout)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


    def setup_widgets(self):
        self.logger.info("Setup widgets")


        self.get_start = QLabel("欢迎使用Apsat")
        label_font = QLabel().font()
        label_font.setPointSize(28)
        self.get_start.setFont(label_font)
        self.get_start.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.get_start.setMaximumHeight(60)


        self.uinput_edit = QPlainTextEdit()
        uinput_font = QLabel().font()
        uinput_font.setPointSize(12)
        uinput_font.setFamily("Microsoft YaHei")
        uinput_font.setItalic(False)
        self.uinput_edit.setFont(uinput_font)
        self.uinput_edit.setPlaceholderText("在此输入玩家名")
        self.uinput_edit.textChanged.connect(self.judge_button_enable)


        self.select_profile_from = QComboBox()
        self.select_profile_from.setPlaceholderText("选择档案来源")
        self.select_profile_from.addItems(["Microsoft", "Yggdrasil"])
        self.select_profile_from.setFont(uinput_font)
        self.select_profile_from.currentIndexChanged.connect(
            lambda: self.uinput_url.setDisabled(False) if self.select_profile_from.currentText() == "Yggdrasil" else self.uinput_url.setDisabled(True)
        )
        self.select_profile_from.setMaximumWidth(220)


        self.uinput_url = QLineEdit(self.config['yggdrasil_link'])
        self.uinput_url.setFont(uinput_font)
        self.uinput_url.setPlaceholderText("在此输入YggdrasilApi链接")
        self.uinput_url.setMaximumWidth(220)
        self.uinput_url.setDisabled(True)


        self.placeholder_1 = QWidget()
        self.placeholder_1.setMaximumHeight(50)


        self.select_profile_type = QComboBox()
        self.select_profile_type.setPlaceholderText("请选择档案类型")
        self.select_profile_type.addItems(["皮肤", "披风", "完整档案", "全部"])
        self.select_profile_type.setFont(uinput_font)
        self.select_profile_type.setMaximumWidth(220)


        self.placeholder_2 = QWidget()
        self.placeholder_2.setMaximumHeight(50)


        self.uinput_download = QLineEdit(self.config['download_folder'])
        self.uinput_download.setFont(uinput_font)
        self.uinput_download.setPlaceholderText("在此输入下载路径")
        self.uinput_download.setMaximumWidth(220)
        self.uinput_download.setMaximumWidth(220)


        self.confirm_buttom = QPushButton("确认")
        self.confirm_buttom.setFont(uinput_font)
        self.confirm_buttom.setDisabled(True)
        self.confirm_buttom.clicked.connect(
            lambda: (
                threading.Thread(target=self.complete_work, name="WorkThread").start()
            )
        )
        self.confirm_buttom.setMaximumWidth(220)


        self.update_button_timer = QTimer()
        self.update_button_timer.timeout.connect(lambda: (self.judge_button_enable(), self.update()))
        self.update_button_timer.start(32)


        self.status_bar = self.statusBar()
        self.status_bar.setFont(uinput_font)
        self.status_bar.showMessage("在此显示状态", 5000)
        self.setStatusBar(self.status_bar)


        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("文件")
        self.edit_menu = self.menu_bar.addMenu("编辑")
        self.support_menu = self.menu_bar.addMenu("帮助")

        open_folder = QAction("打开下载文件夹", self)
        open_folder.setFont(uinput_font)
        open_folder.triggered.connect(
            lambda: threading.Thread(target=self.open_download_folder).start()
        )

        remove_folder = QAction("删除日志文件", self)
        remove_folder.setFont(uinput_font)
        remove_folder.triggered.connect(
            lambda: threading.Thread(target=remove_logs).start()
        )

        help_link = QAction("帮助", self)
        help_link.setFont(uinput_font)
        help_link.triggered.connect(
            lambda: QDesktopServices.openUrl("https://deswatts.github.io/DeswattsDocs")
        )

        github_link = QAction("GitHub主页", self)
        github_link.setFont(uinput_font)
        github_link.triggered.connect(
            lambda: QDesktopServices.openUrl("https://github.com/Deswatts/Apsat")
        )

        license_link = QAction("许可证链接", self)
        license_link.setFont(uinput_font)
        license_link.triggered.connect(
            lambda: QDesktopServices.openUrl("https://www.gnu.org/licenses/gpl-3.0.html")
        )

        toggle_theme = self.edit_menu.addMenu("切换主题")
        toggle_dark_theme = QAction("深色", self)
        toggle_dark_theme.setFont(uinput_font)
        toggle_dark_theme.triggered.connect(
            lambda: self.load_stylesheet("dark")
        )

        toggle_light_theme = QAction("浅色", self)
        toggle_light_theme.setFont(uinput_font)
        toggle_light_theme.triggered.connect(
            lambda: self.load_stylesheet("light")
        )

        toggle_system_theme = QAction("跟随系统", self)
        toggle_system_theme.setFont(uinput_font)
        toggle_system_theme.triggered.connect(
            lambda: self.load_stylesheet("auto")
        )

        toggle_theme.addActions([toggle_dark_theme, toggle_light_theme, toggle_system_theme])

        self.menu_bar.setFont(uinput_font)
        self.file_menu.addActions([open_folder, remove_folder])
        self.support_menu.addActions([help_link, github_link, license_link])

        self.setMenuBar(self.menu_bar)


    def open_download_folder(self):
        self.status_bar.showMessage("打开中")
        try:
            if sys.platform.startswith("win32"):
                os.startfile(os.path.abspath(self.config['download_folder']))
            else:
                of = subprocess.Popen(["xdg-open", os.path.abspath(self.uinput_download.text())])
                if of.returncode != 0:
                    raise FileNotFoundError
            self.status_bar.showMessage("打开成功")

        except FileNotFoundError:
            self.status_bar.showMessage("打开失败")


    def judge_button_enable(self):
        self.confirm_buttom.setEnabled(not ((self.uinput_edit.toPlainText() == "") or (self.select_profile_from.currentText() == "") or (self.uinput_url.text() == "" and self.uinput_url.isEnabled()) or (self.select_profile_type.currentText() == "") or (self.uinput_download.text() == "") or self.start_work))


    def complete_work(self):
        self.start_work = True
        self.status_bar.showMessage("开始获取")
        self.config['yggdrasil_link'] = self.uinput_url.text()
        self.config['download_folder'] = self.uinput_download.text()

        def count_special_char(chars: list[str | bytes], string: str | bytes):
            counter = {}

            for i in chars:
                counter[i] = 0

            for i in string:
                if i in chars:
                    counter[chars[chars.index(i)]] += 1

            return counter

        def process_uinput(uinput: str | bytes):
            try:
                uinput = uinput.replace(" ", "")
            except ValueError:
                pass
            count = count_special_char(["[", "]", "{", "}"], uinput)
            if (count['['] == count[']'] != 0) and (count['{'] == count['}']):
                try:
                    uinput_result = json.loads(uinput)
                except JSONDecodeError:
                    pass
                else:
                    return uinput_result

            if '\n' in uinput:
                uinput_result = uinput.split("\n")
                if uinput_result != uinput:
                    return uinput_result

            uinput = uinput.replace("\n", "")

            if ';' in uinput:
                uinput_result = uinput.split(";")
                if uinput_result != uinput:
                    return uinput_result

            return [uinput]

        uinput = process_uinput(self.uinput_edit.toPlainText())

        uinput = NameList(uinput)

        self.logger.info(f"User inputed: ({uinput}, {self.select_profile_from.currentText()}, {self.select_profile_type.currentText()}, {self.uinput_url.text()}, {self.uinput_download.text()})")

        if self.select_profile_from.currentIndex() == 1:
            profile_from = apsat_core.consts.TYPE_YGGDRASIL
        else:
            profile_from = apsat_core.consts.TYPE_MICROSOFT

        if self.select_profile_type.currentIndex() == 3:
            profile_type = apsat_core.consts.TYPE_ALL
        elif self.select_profile_type.currentIndex() == 2:
            profile_type = apsat_core.consts.TYPE_PROFILE
        elif self.select_profile_type.currentIndex() == 1:
            profile_type = apsat_core.consts.TYPE_CAPE
        elif self.select_profile_type.currentIndex() == 0:
            profile_type = apsat_core.consts.TYPE_SKIN
        else:
            profile_type = 0

        if profile_type == apsat_core.consts.TYPE_ALL:
            for i in [apsat_core.consts.TYPE_SKIN, apsat_core.consts.TYPE_CAPE, apsat_core.consts.TYPE_PROFILE]:
                self._download_profile(uinput, profile_from, i)
        else:
            self._download_profile(uinput, profile_from, profile_type)
        self.start_work = False

    def _download_profile(self, uinput: NameList, profile_from: int, profile_type: int):
        profiles = get_profile(
            ProfileType(
                profile_from | profile_type
            ),
            uinput,
            self.uinput_url.text()
        )

        if len(profiles) == 0:
            self.status_bar.showMessage("获取失败")
        else:
            try:
                os.mkdir(self.uinput_download.text())
            except FileExistsError:
                pass

            if isinstance(profiles, ProfileList):
                for i in profiles:
                    try:
                        os.mkdir(os.path.join(self.uinput_download.text(), i['name']))
                    except FileExistsError:
                        pass
                    with open(os.path.join(self.uinput_download.text(), i['name'], 'profile.json'), 'w+') as f:
                        f.write(json.dumps(i, indent=4))
            elif isinstance(profiles, TextureUrlList):
                textures = resolve_textures(profiles, ProfileType(profile_type), self.uinput_download.text())
                for i in textures:
                    if 'filename' in i:
                        try:
                            os.mkdir(os.path.dirname(i['filename']))
                        except FileExistsError:
                            pass
                    else:
                        try:
                            os.mkdir(os.path.dirname(i['file_name']))
                        except FileExistsError:
                            pass
                DownloadEngine(textures)
            else:
                self.status_bar.showMessage("获取失败")

            self.status_bar.showMessage(f"获取成功，已保存至{self.uinput_download.text()}目录下", 5000)


    def load_config(self):
        try:
            os.mkdir("config")
        except FileExistsError:
            pass

        try:
            with open("config/window.json", "r", encoding="utf-8") as window_config:
                wc = json.loads(window_config.read())

            if 'theme' in wc:
                theme = wc['theme']
            else:
                theme = "auto"

            if 'yggdrasil_link' in wc:
                yggdrasil_link = wc['yggdrasil_link']
            else:
                yggdrasil_link = ""

            if 'download_folder' in wc:
                download_folder = wc['download_folder']
            else:
                download_folder = "downloads"
        except FileNotFoundError:
            theme = "auto"
            yggdrasil_link = ""
            download_folder = "downloads"

        self.config = {
            "theme": theme,
            "yggdrasil_link": yggdrasil_link,
            "download_folder": download_folder
        }


    def save_config(self):
        with open("config/window.json", "w+", encoding='utf-8') as window_config:
            window_config.write(
                json.dumps(
                    self.config,
                    indent=4
                )
            )


    def load_stylesheet(self, theme: str = None):
        self.config['theme'] = theme if not theme is None else self.config['theme']
        self.setStyleSheet(load_stylesheet(self.config['theme']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())