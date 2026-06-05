import pyxel as px
# import core.constants as c


def load_assets():
    px.load("assets/zuma.pyxres")

    load_sprites()
    load_sfx()
    load_bgm()


def load_sprites():
    px.images[0].load(0, 0, "assets/sprite/try.png")


def load_sfx():
    px.sounds[1].pcm("assets/audio/basta.wav")


def load_bgm(): ...
