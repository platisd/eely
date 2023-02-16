import argparse
import sys
import yaml
import subprocess

from yattag import Doc, indent
from pathlib import Path
from pypdf import PdfWriter

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
        content: counters(item, ".") ". ";
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
        all_slides_link = False
        config_path = args.link
        output_format = "md"
        action = create_links
    elif args.html:
        all_slides_link = False
        config_path = args.html
        output_format = "html"
        action = create_html
    elif args.pdf:
        all_slides_link = True
        config_path = args.pdf
        output_format = "pdf"
        action = create_pdf
    else:
        raise RuntimeError("Action missing, we should not get here")

    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    table_of_contents, output_dir = create_filetree(
        config, config_path, output_format, action
    )
    generate_index_page(table_of_contents, output_dir, config, all_slides_link)


def create_filetree(config, config_path, output_format, action):
    config_dir = Path(config_path).parent
    root_path = Path(config["root"])
    root_dir = root_path if root_path.is_absolute() else Path(config_dir, root_path)
    output_path = Path(config["output"])
    output_dir = (
        output_path if output_path.is_absolute() else Path(config_dir, output_path)
    )
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
        slide_number = 0  # Number the slides to appear ordered when using marp --server
        for slide_title, slide_path in chapter["slides"].items():
            slide_src = Path(chapter_root, slide_path)
            assert slide_src.is_file(), f"Slide {slide_src} does not exist"
            dest_filename = Path(f"{slide_number:03}-{Path(slide_path).name}")
            slide_dest = Path(
                chapter_output, dest_filename.with_suffix(f".{output_format}")
            )
            slide_dest.parent.mkdir(parents=True, exist_ok=True)
            action(slide_src, slide_dest, config)
            chapter_slides.append((slide_title, slide_dest))
            slide_number += 1

        table_of_contents[chapter_title] = chapter_slides

    return table_of_contents, output_dir


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


def generate_index_page(table_of_contents, output_dir, config, all_slides_link):
    with open(Path(output_dir, "index.html"), "w") as index_file:
        doc, tag, text = Doc().tagtext()
        with tag("html"):
            with tag("head"):
                with tag("title"):
                    text(config["title"])
                with tag("style"):
                    text(TABLE_OF_CONTENTS_CSS)
            with tag("body"):
                # Title
                with tag("h1"):
                    text(config["title"])
                # Table of contents
                with tag("ol", type="1"):
                    for chapter_title, chapter_slides in table_of_contents.items():
                        with tag("li"):
                            text(chapter_title)
                            with tag("ol", type="1"):
                                for slide_title, slide_path in chapter_slides:
                                    with tag("li"):
                                        with tag("a", href=f"{slide_path}"):
                                            text(slide_title)
                if all_slides_link:
                    with PdfWriter() as merger:
                        for chapter_slides in table_of_contents.values():
                            for _, slide_path in chapter_slides:
                                merger.append(slide_path)
                        all_slides_path = (
                            f'{config["title"].replace(" ", "_")}.pdf'
                            if "all_slides" not in config
                            else config["all_slides"]
                        )
                        merger.write(Path(output_dir, all_slides_path))

                    doc.stag("hr")
                    with tag("a", href=f"{all_slides_path}", style="font-size: 24pt"):
                        text("All slides")
        index_file.write(indent(doc.getvalue(), indent_text=True))


if __name__ == "__main__":
    sys.exit(main())
