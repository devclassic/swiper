import os
import webview
import shutil
import uuid

os.path.exists("./data/images") or os.makedirs("./data/images")

basepath = os.path.abspath(".")
ui = os.path.join(basepath, "data", "index.html")

window = webview.create_window("端点轮播", ui, width=800, height=600)


def fullscreen():
    window.toggle_fullscreen()


def openfile():
    file_types = ("图片文件 (*.jpeg;*.jpg;*.png;*.gif)", "所有文件 (*.*)")
    result = window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
    )
    files = []
    if result:
        for file in result:
            _, ext = os.path.splitext(file)
            filename = f"{uuid.uuid4()}{ext}"
            shutil.copy(file, f"./data/images/{filename}")
            files.append(filename)
    return files


def removefile(filename):
    path = f"./data/images/{filename}"
    if os.path.exists(path):
        os.remove(path)


def getconfig():
    if not os.path.exists("./data/config.json"):
        return '{"delay": 1, "images": []}'
    with open("./data/config.json", "r", encoding="utf-8") as f:
        return f.read()


def saveconfig(config):
    with open("./data/config.json", "w", encoding="utf-8") as f:
        f.write(config)


window.expose(fullscreen)
window.expose(openfile)
window.expose(removefile)
window.expose(getconfig)
window.expose(saveconfig)


webview.start()
