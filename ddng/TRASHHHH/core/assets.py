import pyxel as px
import core.constants as c


def init_assets():
    slot = c.SPRITE_ATLAS_TILE
    center = slot // 2

    px.images[0].rect(0, 0, slot, slot, 0)
    # Normal (0,0)
    px.images[0].circ(center, center, 6, 7)
    # Regenerator (16,0) - '+'
    px.images[0].circ(slot + center, center, 6, 7)
    px.images[0].line(slot + center, center - 3, slot + center, center + 3, 0)
    px.images[0].line(slot + center - 3, center, slot + center + 3, center, 0)
    # Chameleon (32,0) - '?'
    px.images[0].circ(2 * slot + center, center, 6, 7)
    px.images[0].text(2 * slot + center - 2, center - 3, "?", 0)

    # Tower (48, 0)
    px.images[0].rect(3 * slot, 0, slot, slot, 13)
    px.images[0].circ(3 * slot + center, center, 4, 1)

    # Sounds
    px.sounds[0].set("a2", "p", "6", "n", 10)  # Shoot
    px.sounds[1].pcm("assets/audio/basta.wav")
    px.sounds[2].set("c3e3g3", "s", "4", "n", 30)  # BGM
