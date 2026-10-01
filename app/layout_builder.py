def build_comic_layout(story):

    comic = []

    for panel in story["panels"]:

        comic.append({
            "panel": panel["panel"],
            "title": panel["title"],
            "narration": panel["narration"],
            "dialogue": panel["dialogue"],
            "image_prompt": panel["image_prompt"]
        })

    return comic