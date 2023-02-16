import sys
from pathlib import Path

# Add the parent folder where the SUT is located to the PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
import generate_marp_course as generator


def test_create_filetree(tmp_path):
    config = {
        "title": "Company X delivery",
        "root": "slides",
        "output": tmp_path,
        "all_slides": "company-x-course.pdf",
        "assets": "resources",
        "chapters": {
            "Hello world": {
                "root": "hello-world",
                "slides": {
                    "Hello world": "hello-world.md",
                    "Setting up the environment": "environment.md",
                    "Variables": "variables.md",
                    "Functions": "functions.md",
                },
            },
            "Data types": {
                "root": "data-types",
                "slides": {
                    "Data types": "data-types.md",
                    "Strings": "strings.md",
                    "Numbers": "numbers.md",
                    "Booleans": "booleans.md",
                    "Arrays": "arrays.md",
                    "Objects": "objects/objects.md",
                },
            },
        },
    }
    config_dir = Path(Path().absolute(), "my-awesome-course")
    output_format = "md"
    action = generator.create_links
    table_of_contents, output_dir, _ = generator.create_filetree(
        config, config_dir, output_format, action
    )
    assert output_dir == tmp_path
    assert "Hello world" in table_of_contents
    assert "Data types" in table_of_contents
    chapter_contents = {}
    slides_per_chapter = {}
    for chapter_title, chapter_slides in table_of_contents.items():
        slide_titles = []
        slide_paths = []
        for slide_title, slide_path in chapter_slides:
            assert slide_path.is_symlink()
            assert slide_path.exists()
            slide_titles.append(slide_title)
            slide_paths.append(slide_path)
        chapter_contents[chapter_title] = slide_titles
        slides_per_chapter[chapter_title] = slide_paths

    for chapter in config["chapters"].keys():
        assert (
            list(config["chapters"][chapter]["slides"].keys())
            == chapter_contents[chapter]
        )
        for original_slide, linked_slide in zip(
            config["chapters"][chapter]["slides"].values(),
            slides_per_chapter[chapter],
        ):
            path_to_original_slide = Path(
                config_dir,
                config["root"],
                config["chapters"][chapter]["root"],
                original_slide,
            )
            assert path_to_original_slide == linked_slide.readlink()
