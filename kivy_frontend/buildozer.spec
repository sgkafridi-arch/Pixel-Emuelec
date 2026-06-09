[app]

title = Pixel Edition
package.name = pixeledition
package.domain = org.pixeledition

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db

version = 0.1.0

requirements = python3,kivy,pyjnius,requests,sqlalchemy,pillow,networkx,pycryptodome

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.png
preloaded_libraries = gl

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 31
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
