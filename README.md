# 🐍 eely

Organize your Markdown-based content into configurable course deliveries.

<img src="https://platis.solutions/assets/images/eely-square.png" width="500">

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

