import argparse
import sys
import yaml
import subprocess

from yattag import Doc, indent
from pathlib import Path

TABLE_OF_CONTENTS_CSS = """
    ol {
        counter-reset: item;
        font-size: 28pt;
    }

    ol ol {
        font-size: 24pt;
    }

    ol li {
        display: block;
    }

    ol li:before {
        content: counters(item, ". ") ". ";
        counter-increment: item;
    }
"""


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--link",
        metavar="CONFIG",
        help="Create links to slides in a directory structure for delivery",
    )
    group.add_argument(
        "--html",
        metavar="CONFIG",
        help="Create HTML pages for slides in a directory structure for delivery",
    )
    group.add_argument(
        "--pdf",
        metavar="CONFIG",
        help="Create PDFs for slides in a directory structure for delivery",
    )
    args = parser.parse_args()

    if args.link:
        return run_action(args.link, "md", create_links)
    if args.html:
        return run_action(args.html, "html", create_html)
    if args.pdf:
        return run_action(args.pdf, "pdf", create_pdf)

    print("No action specified")

    return 1


def run_action(config_path, output_format, action):
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    config_dir = Path(config_path).parent
    root_dir = Path(Path(config_path).parent, config["root"])
    output_dir = Path(Path(config_path).parent, config["output"])
    assets = Path("" if "assets" not in config else config["assets"])

    table_of_contents = {}
    for chapter_title, chapter in config["chapters"].items():
        chapter_root = Path(root_dir, "" if "root" not in chapter else chapter["root"])
        chapter_output = Path(output_dir, chapter_title.replace(" ", "_"))
        chapter_output.mkdir(parents=True, exist_ok=True)

        chapter_assets_dest = Path(chapter_output, assets)
        chapter_assets_dest.unlink(missing_ok=True)
        chapter_assets_dest.symlink_to(
            Path(config_dir, assets), target_is_directory=True
        )

        chapter_slides = []
        for slide_title, slide_path in chapter["slides"].items():
            slide_src = Path(chapter_root, slide_path)
            assert slide_src.is_file(), f"Slide {slide_src} does not exist"
            slide_dest = Path(chapter_output, Path(slide_path).name).with_suffix(
                f".{output_format}"
            )
            slide_dest.parent.mkdir(parents=True, exist_ok=True)
            action(slide_src, slide_dest, config)
            chapter_slides.append((slide_title, slide_dest))

        table_of_contents[chapter_title] = chapter_slides

    generate_table_of_contents(table_of_contents, output_dir, config)

    return 0


def create_links(slide_src, slide_dest, _):
    slide_dest.unlink(missing_ok=True)
    slide_dest.symlink_to(slide_src)
    assert slide_dest.exists(), f"Link is wrong: {slide_dest}"


def create_html(slide_src, slide_dest, config):
    run_marp(slide_src, slide_dest, config, "--html")


def create_pdf(slide_src, slide_dest, config):
    run_marp(slide_src, slide_dest, config, "--pdf")


def run_marp(slide_src, slide_dest, config, output_type_flag):
    marp = Path("marp" if "marp" not in config else config["marp-cli"])
    subprocess.check_call([marp, slide_src, output_type_flag, "-o", slide_dest])


def generate_table_of_contents(table_of_contents, output_dir, config):
    with open(Path(output_dir, "index.html"), "w") as index_file:
        doc, tag, text = Doc().tagtext()
        with tag("html"):
            with tag("head"):
                with tag("title"):
                    text(config["title"])
                with tag("style"):
                    text(TABLE_OF_CONTENTS_CSS)
            with tag("body"):
                with tag("ol", type="1"):
                    for chapter_title, chapter_slides in table_of_contents.items():
                        with tag("li"):
                            text(chapter_title)
                            with tag("ol", type="1"):
                                for slide_title, slide_path in chapter_slides:
                                    with tag("li"):
                                        with tag("a", href=f"{slide_path}"):
                                            text(slide_title)
        index_file.write(indent(doc.getvalue(), indent_text=True))


if __name__ == "__main__":
    sys.exit(main())
