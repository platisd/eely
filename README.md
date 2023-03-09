# 🐍 eely

Organize your Markdown-based content into configurable course deliveries.

<img src="https://platis.solutions/assets/images/eely-logo.png" width="500">

## What is `eely`?

`eely` is a tool to help you create course deliveries from Markdown-based content.
The idea is to have a single source of truth for your course content,
and then use `eely` to generate the different course deliveries.<br>
No need to maintain multiple copies/branches for different courses/customers/audiences anymore.
Did you get a new customer who wants to skip some content from one course and add something else?
No need to manually edit the existing course content. Pick and choose the content you want.<br>
You create your Markdown lectures once and then you use YAML to specify what should go into each delivery.

But that's not all `eely` can do. I've listed the reasons that led to its creation below.

## Why `eely`?

I've been teaching programming for a while now, and I could not find a tool that offers
**all** or even most of the following features:
1. **Markdown-based content** - I like to write my content directly in `.md` files.<br>
I don't want to create HTML files, or use any online editors.
I want to author straight up Markdown on my local machine that gets automagically converted to
HTML slides I can show during my classes.<br>
This is because I like to have my content in a version control system, and I don't want
to be tied to any vendor-centric such as Google Slides or Powerpoint.
1. **One lecture per file** - I like to have one lecture per file. Divide and conquer!<br>
I don't want to maintain the whole course or even "chapter" in one file.
Having one file for "everything" is very inflexible and content is hard to find.
1. **Navigateable chapter-based organization** - I like to organize my content into chapters.<br>
I don't want to have a flat list of lectures, I want to be able to organize my content into
chapters. It is more "natural" and resembles a book.
It is easier for the instructor to browse and communicate the content during the classroom
as well as for the students to follow.
1. **Configurable course deliveries** - I like to be able to configure what goes into each course delivery.<br>
I am teaching the same subject for multiple audiences who have somewhat different needs but
there's a lot of overlap. For example, I've got a "beginner", "intermediate" and "advanced" course.
The "intermediate" course is a mix of the "beginner" and "advanced" courses.
Then, there are customers who want to skip some content from one course and add some
material specifically tailored for them.<br>
I want to be able to accomodate the above without maintainting multiple copies/branches
and without having to manually edit existing content for each delivery.
1. **All course material in one PDF** - I like to be able to generate a single PDF file with all the course material and hand it out to the students.<br>
Remember, that doesn't mean I want to have a single Markdown file for the whole course.
Multiple source files, one deliverable PDF. 
1. **Deliverable extra content** - Along with the PDF with all the slides, I need to deliver additional content. Everything packaged into a single archive.<br>
Almost every lecture comes with a "lab" section which is usually some stand-alone exercise for the
students to solve, along with the proposed solution.
Moreover, there could be cheatsheets, manuals, articles etc I want to pass on to the students.
In other words, there's a lot more valuable material that needs to be delivered, not just the slides.<br>
I want to get the PDF with all the slides and all the extra content in one `zip` file.
With one click and the extra material organized in a sensible way.

If you are facing the same issues `eely`'s here to help. 

### Why the name?

Aside of being a [fish a*fish*ionado](https://www.youtube.com/watch?v=tvRkSvmt3Xc),
I also... like to play with words. 🥲<br>
According to [Wiktionary](https://en.wiktionary.org/wiki/eely), `eely` is an adjective meaning:

> Resembling an eel: long, thin and slippery.

It also happens to be a [homophone](https://en.wikipedia.org/wiki/Homophone) of the
[Greek word](https://en.wiktionary.org/wiki/%CF%8D%CE%BB%CE%B7) `ύλη`
which means "material" or "matter". When used in an educational context, it roughly translates to
"course curriculum".
A match made in heaven for this project, if you ask me. 🤷‍♂️

## How does `eely` work?

Before you can use `eely` you need to install its dependencies and create a configuration file.

### Install dependencies

`eely` utilizes [marp-cli](https://github.com/marp-team/marp-cli) to convert your Markdown files
into HTML or PDF slides. So it assumes there's a `marp` binary in your `PATH`. The easiest ways
to install it are:
* `npm install -g @marp-team/marp-cli` if you have `npm` installed
* Download the latest `marp` [binary](https://github.com/marp-team/marp-cli/releases)
  for your platform and place it in your `PATH`. I've tested it with release `v2.4.0` on Ubuntu.

Then you need to install `eely`'s Python dependencies. The easiest way is to use `pip` and
don't forget you can use a [virtual environment](https://docs.python.org/3/library/venv.html):
`pip install -r requirements.txt`

### Markdown slides

`eely` uses [marp](https://marp.app/#get-started) to convert your Markdown files into HTML or PDF slides.
You need to follow the supported syntax of `marp` to create your slides.
We could potentially support other slide generators in the future, as long as they are simple to integrate.
Feel free to open an issue if you have a suggestion.

### Configuration YAML

Next, you need to create a `.yaml` file with the configuration for each of your course deliveries.
In it, you will specify the contents of each delivery, the output directory, the extra content etc.
You can find an example configuration in [beginning-course.yaml](https://github.com/platisd/eely-sample-repository/blob/master/beginning-course.yaml)
that's referring to this [sample repository](https://github.com/platisd/eely-sample-repository).

An overview of the configuration file options:

| Option                        | Description                                                                                                       | Default                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `title`                       | The title of the course delivery.                                                                                 | No                                                           |
| `root`                        | The root directory of the course content.                                                                         | The same directory as the configuration YAML                 |
| `output`                      | The output directory for the course delivery.                                                                     | A subdirectory based on `title` under `output/`              |
| `course_slides`               | The path to the PDF file containing all the slides                                                                | The `title` relative to the config, spaces replaced with `_` |
| `course_archive`              | The path to the ZIP file containing all the slides and extra content                                              | The `title` relative to the config, spaces replaced with `_` |
| `chapters`                    | The keys represent the titles of the chapters                                                                     | No                                                           |
| `chapters.<chapter>.root`     | The root directory of the chapter content                                                                         | The same directory as the configuration YAML                 |
| `chapters.<chapter>.assets`   | The directory containing the assets (e.g. images for the slides) for the chapter                                  | Ignored if not present                                       |
| `chapters.<chapter>.lectures` | The lectures to include in the chapter, keys are the titles and values are the paths to the respective `.md` file | No                                                           |
| `chapters.<chapter>.extras`   | A list with the paths to the extra content to include in the chapter, entire directories can be specified         | Ignored if not present                                       |
| `watermark`                   | The path to another PDF you would like to use as a watermark, more details [here](#watermark)                     | Ignored if not present                                       |

In the above options whenever a path is needed, it can be either absolute or relative to the
configuration YAML file. Relative paths are recommended. An example of a recommended file structure can be found in [test/my-awesome-course](test/my-awesome-course).

Order matters! The order of the chapters and the order of the slides within each chapter is the same as in the configuration file.

### Usage

`eely` can be used in the following ways:
* **Static classroom mode (HTML)** - HTML slides are generated for the entire
  course and the instructor can navigate between them during the classroom.
  * `python3 eely.py --html <path/to/your/config.yaml>`
* **Dynamic classroom mode (links)** - Links to the markdown files are generated
  in the correct order and the instructor can navigate between them during the classroom
  using `marp --server` inside the `output` folder. Any changes to the content during the
  classroom are reflected in the slides.
  * `python3 eely.py --link <path/to/your/config.yaml>`
* **Delivery mode (PDF)** - PDF slides are generated for for each lecture as well as for the
  entire course. Any extra files are packaged along with the slides in a ZIP file.
  * `python3 eely.py --pdf <path/to/your/config.yaml>`

In all modes, an `index.html` file is generated in the `output` directory specified
in the YAML file. It contains links to to all slides organized by chapter.
You can use this during the classroom to navigate between the different lectures.<br>
If the PDF mode is used, it will also contain links to download the single PDF file containing all
slides as well as the ZIP file containing all the slides and the extra content (e.g. labs).
You can then distribute the archive with all course material to the students.

### Watermark

The PDF you specify is applied **on top** of the complete course material so you may need to think about:
1. The opacity of your overlay, if you want your watermark to be underneath the text you need to make it
  less transparent.
2. For the overlay PDF to end up where you want it, you need to ensure that the overlay is smaller or the same
  size as the course material PDF you are overlaying it on.

The reason it is applied on top and not below is that slides typically have some background image and in that
case the watermark would be hidden underneath it. Fixes or suggestions around this are welcome.

### Additional command line arguments

Aside of the `--html`, `--link` and `--pdf` arguments, `eely` also supports some helpful arguments that
allow you to override some configuration file options. This allows you to use the same configuration file
for multiple course deliveries and just override the (few) options that are different for each delivery.

Run `--help` to explore the different options.
