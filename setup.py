from setuptools import setup

setup(
    name="Bulletin",
    version="0.1.0",
    packages=["boards", "boards.migrations", "Bulletin"],
    url="",
    license="",
    author="Dmitry Schigolev",
    author_email="monkaster@gmail.com",
    description="Bulletin board for MMORPG",
    install_requires=[
        "Django==4.2.7",
        "django-allauth==0.58.2",
        "django-ckeditor==6.7.0",
        "django-js-asset==2.1.0",
        "Pillow==9.5.0",
        "python3-openid==3.2.0",
        "pytz==2023.3",
        "requests==2.31.0",
        "ckeditor==6.5.1",
        "ckeditor_uploader==0.6.2",
    ],
)
