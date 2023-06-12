import os

from kanji_colorize.kanjicolorizer.colorizer import KanjiColorizer

if __name__ == "__main__":
    kanji_string = "日無渦巻"
    output_dir = os.path.join("output", "colorized_kanji")
    args = " ".join(["--characters", kanji_string, "--output", output_dir])
    kc = KanjiColorizer(args)
    kc.write_all()
