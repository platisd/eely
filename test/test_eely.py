import sys
from pathlib import Path

# Add the parent folder where the SUT is located to the PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
import eely


def test_create_filetree(tmp_path):
    config = {
        "title": "Company X delivery",
        "root": "lectures",
        "output": tmp_path,
        "all_lectures": "company-x-course.pdf",
        "chapters": {
            "Hello world": {
                "root": "hello-world",
                "assets": "resources",
                "lectures": {
                    "Hello world": "hello-world.md",
                    "Setting up the environment": "environment.md",
                    "Variables": "variables.md",
                    "Functions": "functions.md",
                },
            },
            "Data types": {
                "root": "data-types",
                "lectures": {
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
    action = eely.create_links
    table_of_contents, output_dir, _ = eely.create_filetree(
        config, config_dir, output_format, action
    )
    assert output_dir == tmp_path
    assert "Hello world" in table_of_contents
    assert "Data types" in table_of_contents
    chapter_contents = {}
    lectures_per_chapter = {}
    for chapter_title, chapter_lectures in table_of_contents.items():
        lecture_titles = []
        lecture_paths = []
        for lecture_title, lecture_path in chapter_lectures:
            assert lecture_path.is_symlink()
            assert lecture_path.exists()
            lecture_titles.append(lecture_title)
            lecture_paths.append(lecture_path)
        chapter_contents[chapter_title] = lecture_titles
        lectures_per_chapter[chapter_title] = lecture_paths

    for chapter in config["chapters"].keys():
        assert (
            list(config["chapters"][chapter]["lectures"].keys())
            == chapter_contents[chapter]
        )
        for original_lecture, linked_lecture in zip(
            config["chapters"][chapter]["lectures"].values(),
            lectures_per_chapter[chapter],
        ):
            path_to_original_lecture = Path(
                config_dir,
                config["root"],
                config["chapters"][chapter]["root"],
                original_lecture,
            )
            assert path_to_original_lecture == linked_lecture.readlink()
