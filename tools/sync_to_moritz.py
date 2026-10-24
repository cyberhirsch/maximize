"""Copy the keymap (`maximize/keymap_max.py`) into a Moritz source tree, where the Max and Moritz
keymap presets read it as `scripts/presets/keyconfig/keymap_data/moritz_max_data.py`.

Run: python tools/sync_to_moritz.py <moritz source> [<moritz install scripts folder>]
"""
import os
import sys

HEADER = """\
# Moritz: a copy of `maximize/keymap_max.py` from the Maximize add-on
# (github.com/cyberhirsch/maximize), the single source of the Max and Moritz keys. Keep the two
# in sync; bindings to Maximize's operators are skipped while the add-on is not enabled.
"""
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(args):
    if not args:
        sys.exit(__doc__)
    with open(os.path.join(ROOT, "maximize", "keymap_max.py"), encoding="utf-8") as fh:
        text = HEADER + fh.read()
    targets = [os.path.join(args[0], "scripts", "presets", "keyconfig", "keymap_data")]
    if len(args) > 1:
        targets.append(os.path.join(args[1], "presets", "keyconfig", "keymap_data"))
    for folder in targets:
        path = os.path.join(folder, "moritz_max_data.py")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1:])
