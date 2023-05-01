from flask import Flask, render_template, request, redirect, url_for
from stories import Story
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'madlibs_app_template'
toolbar = DebugToolbarExtension(app)

stories = {
    "story1": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
        """Once upon a time in a long-ago {place}, there lived a
           large {adjective} {noun}. It loved to {verb} {plural_noun}."""
    ),
    "story2": Story(
        ["animal", "verb", "adjective", "food"],
        """The {animal} loved to {verb} while eating {adjective} {food}."""
    )
}

@app.route("/", methods=["GET"])
def story_selection():
    return render_template("story_selection.html", stories=stories)

@app.route("/form", methods=["GET"])
def story_form():
    story_id = request.args.get("story_id")
    prompts = stories[story_id].prompts
    return render_template("form.html", prompts=prompts, story_id=story_id)

@app.route("/story", methods=["POST"])
def generate_story():
    story_id = request.form["story_id"]
    answers = {key: request.form[key] for key in stories[story_id].prompts}
    result = stories[story_id].generate(answers)
    return render_template("story.html", result=result)
