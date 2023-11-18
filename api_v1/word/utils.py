def get_meanings_from_word_info(json_data) -> list[str]:
    meanings_list = []

    if "meanings" in json_data:
        meanings = json_data["meanings"]

        meanings_list = [x["meaning"] for x in meanings]
    return meanings_list
