import os
import shutil
import markdown
from datetime import datetime

# Define input and public_html directories
input_dir = "input"
public_html_dir = "public_html"
static_dir = "static"

# Create public_html directories if they don't exist
if not os.path.exists(public_html_dir):
    os.mkdir(public_html_dir)
if not os.path.exists(os.path.join(public_html_dir, "writings")):
    os.mkdir(os.path.join(public_html_dir, "writings"))
if not os.path.exists(os.path.join(public_html_dir, "writings", "images")):
    os.mkdir(os.path.join(public_html_dir, "writings", "images"))

# Read the content of the input directory
articles = []
for filename in os.listdir(input_dir):
    if filename.endswith(".md"):
        with open(os.path.join(input_dir, filename), "r") as f:
            content = f.read()
            title = filename[:-3]
            date = datetime.fromtimestamp(os.path.getmtime(os.path.join(input_dir, filename))).strftime("%Y-%d-%B")
            html = markdown.markdown(content)
            # Prepend HTML boilerplate to output files
            html = "<!DOCTYPE html>\n<html lang=\"en\">\n<meta charset=\"utf-8\">\n" + html + "\n</html>"
            articles.append((title, date, html))
            # Save the converted articles to the public_html directory
            with open(os.path.join(public_html_dir, "writings", f"{title}.html"), "w") as f:
                f.write(html)
            # Copy images used in the articles to the public_html/writings/images directory
            images_dir = os.path.join(input_dir, "images")
            if os.path.exists(images_dir):
                for image in os.listdir(images_dir):
                    shutil.copyfile(os.path.join(images_dir, image), os.path.join(public_html_dir, "writings", "images", image))

# Create or update articlelist.html file
articles.sort(key=lambda x: x[1], reverse=True)
with open(os.path.join(public_html_dir, "articlelist.html"), "w") as f:
    f.write("<table>\n")
    f.write("<tr><th>Title</th><th>Date</th></tr>\n")
    for article in articles:
        f.write(f"<tr><td><a href='writings/{article[0]}.html'>{article[0]}</a></td><td>{article[1]}</td></tr>\n")
    f.write("</table>")

# Copy index.html file from the static directory to the public_html directory
shutil.copyfile(os.path.join(static_dir, "index.html"), os.path.join(public_html_dir, "index.html"))
